"""Exercise ledger workflows and failure boundaries in isolated temporary folders."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).parent


class StateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root / '_work/run/任务状态.json'
        self.call('init', '--run-id', 'run')
        self.call('actor', '--id', 'w', '--identity', '/writer')
        self.call('actor', '--id', 'r', '--identity', '/reviewer')
        self.put('01.md', 'first chapter')
        self.register()

    def put(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')

    def put_json(self, name, value):
        self.put(name, json.dumps(value, ensure_ascii=False))

    def call(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'state.py'),
                                 '--root', str(self.root), '--state', str(self.state), *args],
                                capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
        return result

    def register(self, *args, ok=True):
        return self.call('register', '--id', 'ch', '--path', '01.md',
                         '--kind', 'chapter', '--actor', 'w', *args, ok=ok)

    def data(self):
        return json.loads(self.state.read_text(encoding='utf-8'))

    def review(self, rid='v1', kind='content', actor='r', status='通过', inputs=None, ok=True):
        bundle = inputs or ('_work/run/' + rid + '-inputs.json')
        if inputs is None:
            self.call('freeze', '--files', 'ch', '--output', bundle)
        self.put(rid + '.md', 'Actual review report for ' + rid)
        self.put_json(rid + '.json', {'id': rid, 'kind': kind, 'actor': actor,
                                      'report': rid + '.md', 'inputs': bundle,
                                      'coverage': [{'target': 'ch', 'status': status,
                                                    'scope': 'full chapter', 'issues': []}]})
        self.call('review', '--spec', rid + '.json', ok=ok)

    def test_full_delivery_and_invalidation(self):
        self.review()
        self.review('reader', kind='reader', status='已完成')
        self.call('reading', '--status', '已完成', '--reason', 'full route', '--reviews', 'reader')
        result = subprocess.run([sys.executable, str(SCRIPTS / 'check-state.py'),
                                 '--root', str(self.root), '--state', str(self.state), '--final'],
                                capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.put('01.md', 'revised chapter')
        self.put('fix.md', 'I1 fixed with evidence and before/after versions')
        self.register('--revision', 'fix1', '--record', 'fix.md')
        state = self.data()
        self.assertEqual(state['reading']['status'], '未完成')
        self.assertTrue(all(r['coverage'][0]['applicability'] == 'pending' for r in state['reviews']))
        self.review('v2')
        state = self.data()
        self.assertEqual(state['reviews'][0]['coverage'][0]['applicability'], 'historical')
        self.assertEqual(len(state['files']['ch']['revisions']), 1)
        self.assertEqual(len(state['files']['ch']['contributors']), 2)
        old = self.root / state['reviews'][0]['coverage'][0]['inputs'][0]['snapshot']
        self.assertEqual(old.read_text(encoding='utf-8'), 'first chapter')

    def test_rejected_commands_leave_ledger_unchanged(self):
        before = self.state.read_bytes()
        self.review('self', actor='w', ok=False)
        self.assertEqual(before, self.state.read_bytes())
        self.call('init', '--run-id', 'overwrite', ok=False)
        self.call('actor', '--id', 'w', '--identity', '/other', ok=False)
        self.call('register', '--id', 'escape', '--path', '../outside.md',
                  '--kind', 'chapter', '--actor', 'w', ok=False)
        self.assertEqual(before, self.state.read_bytes())

    def test_shared_dependency_and_batch_registration(self):
        self.put('shared.md', 'shared assumptions')
        self.call('register', '--id', 'shared', '--path', 'shared.md', '--kind', 'shared', '--actor', 'w')
        self.call('freeze', '--files', 'ch', 'shared', '--output', '_work/run/deps.json')
        self.review(inputs='_work/run/deps.json')
        self.put('shared.md', 'changed assumptions')
        self.call('register', '--id', 'shared', '--path', 'shared.md', '--kind', 'shared', '--actor', 'w')
        self.assertEqual(self.data()['reviews'][0]['coverage'][0]['applicability'], 'pending')
        self.review('stale', inputs='_work/run/deps.json')
        self.assertEqual(self.data()['reviews'][-1]['coverage'][0]['applicability'], 'pending')
        self.put('01.md', 'new chapter')
        self.put('shared.md', 'new shared')
        self.put_json('batch.json', [{'id': 'ch', 'path': '01.md', 'kind': 'chapter', 'actor': 'w'},
                                     {'id': 'shared', 'path': 'shared.md', 'kind': 'shared', 'actor': 'w'}])
        self.call('register-batch', '--spec', 'batch.json')

    def test_budget_and_continuation(self):
        self.put('fix.md', 'problem resolution')
        for text, rid in [('a', 'one'), ('b', 'one'), ('c', 'two')]:
            self.put('01.md', text)
            self.register('--revision', rid, '--record', 'fix.md')
        self.assertEqual(len(self.data()['files']['ch']['revisions']), 2)
        before = self.state.read_bytes()
        self.put('01.md', 'third repair')
        self.register('--revision', 'three', '--record', 'fix.md', ok=False)
        self.assertEqual(before, self.state.read_bytes())

    def test_snapshot_tampering_and_partial_reading(self):
        self.call('freeze', '--files', 'ch', '--output', '_work/run/frozen.json')
        self.call('freeze', '--files', 'ch', '--output', '_work/run/frozen.json', ok=False)
        bundle = json.loads((self.root / '_work/run/frozen.json').read_text(encoding='utf-8'))
        self.put(bundle['inputs'][0]['snapshot'], 'tampered')
        before = self.state.read_bytes()
        self.review('bad', inputs='_work/run/frozen.json', ok=False)
        self.assertEqual(before, self.state.read_bytes())
        self.put(bundle['inputs'][0]['snapshot'], 'first chapter')
        self.review('partial', kind='reader', status='部分覆盖')
        self.call('reading', '--status', '已完成', '--reason', 'claim full', '--reviews', 'partial', ok=False)


class MergeTest(unittest.TestCase):
    """合并方案 v11 的验收用例（T1–T6、T8、T9、T10）。"""

    def setUp(self):
        self.reset()

    def reset(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work = self.root / '_work/run'
        self.work.mkdir(parents=True)
        self.state = self.work / '任务状态.json'

    # ---------- helpers ----------
    def state_cmd(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'state.py'),
                                 '--root', str(self.root), '--state', str(self.state), *args],
                                capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
        return result.stdout

    def check_cmd(self, final=False):
        args = [sys.executable, str(SCRIPTS / 'check-state.py'),
                '--root', str(self.root), '--state', str(self.state)]
        if final:
            args.append('--final')
        result = subprocess.run(args, capture_output=True, encoding='utf-8')
        return result.returncode, json.loads(result.stdout)

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def init_ledger(self, with_reviewer=True):
        self.state_cmd('init', '--run-id', 'run')
        self.state_cmd('actor', '--id', 'w', '--identity', '/writer')
        if with_reviewer:
            self.state_cmd('actor', '--id', 'rv', '--identity', '/reviewer')

    def register_file(self, fid='ch', path='01.md', kind='chapter', body='chapter body'):
        self.put(path, body)
        self.state_cmd('register', '--id', fid, '--path', path, '--kind', kind, '--actor', 'w')

    def submit_review(self, targets, rid='v1', status='通过', kind='content', ok=True):
        self.state_cmd('freeze', '--files', *targets, '--output', '_work/run/%s-in.json' % rid)
        self.put('_work/run/%s.md' % rid, 'report for ' + rid)
        spec = {'id': rid, 'kind': kind, 'actor': 'rv', 'report': '_work/run/%s.md' % rid,
                'inputs': '_work/run/%s-in.json' % rid,
                'coverage': [{'target': t, 'status': status, 'scope': 'scope', 'issues': []}
                             for t in targets]}
        self.put('_work/run/%s.json' % rid, json.dumps(spec, ensure_ascii=False))
        self.state_cmd('review', '--spec', '_work/run/%s.json' % rid, ok=ok)

    def ledger(self):
        return json.loads(self.state.read_text(encoding='utf-8'))

    def write_ledger(self, value):
        self.state.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def hand_ledger(self, schema=2, path='01.md', body='chapter body', identity='/writer',
                    owner='w', contributors=None):
        self.put(path, body)
        digest = __import__('hashlib').sha256((self.root / path).read_bytes()).hexdigest()
        entry = {'path': path, 'kind': 'chapter', 'sha256': digest, 'owner': owner,
                 'contributors': contributors if contributors is not None
                 else [{'actor': 'w', 'sha256': digest}], 'revisions': []}
        value = {'run_id': 'run', 'next_action': 'go', 'revision_limit': 2,
                 'actors': {'w': {'identity': identity}, 'rv': {'identity': '/reviewer'}},
                 'files': {'ch': entry}, 'reviews': [],
                 'reading': {'status': '跳过', 'reason': 'skip', 'review_ids': []}}
        if schema is not None:
            value['schema_version'] = schema
        self.write_ledger(value)
        return digest

    # ---------- T1 / V2 ----------
    def test_t1_init_ledger_scope(self):
        self.init_ledger()
        rc, body = self.check_cmd()
        self.assertEqual(rc, 1)
        self.assertEqual([(f['at'], f['message']) for f in body['failed']],
                         [('files', '没有登记文件')])
        self.assertIn('"saved": true', self.state_cmd('next', '--text', 'next step'))

    # ---------- T2 / V3 ----------
    def test_t2_version_gate(self):
        base = {'run_id': 'run', 'next_action': 'go', 'revision_limit': 2,
                'actors': {'w': {'identity': '/writer'}}, 'files': {}, 'reviews': [],
                'reading': {'status': '跳过', 'reason': 'skip', 'review_ids': []}}
        for value in (None, 1, 3, "2", 2.0, True):
            data = dict(base)
            if value is not None:
                data['schema_version'] = value
            self.write_ledger(data)
            rc, body = self.check_cmd()
            self.assertEqual(rc, 1, 'value=%r' % (value,))
            self.assertTrue(any(f['at'] == 'schema_version' for f in body['failed']),
                            'value=%r' % (value,))
            self.state_cmd('next', '--text', 'x', ok=False)
        self.write_ledger(dict(base, schema_version=2))
        rc, body = self.check_cmd()
        self.assertFalse(any(f['at'] == 'schema_version' for f in body['failed']))

    # ---------- T3 / V4a ----------
    def test_t3_delivery_requires_review(self):
        self.init_ledger()
        self.register_file()
        self.state_cmd('reading', '--status', '跳过', '--reason', 'skip')
        rc, body = self.check_cmd(final=True)
        self.assertEqual(rc, 2)
        self.assertEqual(body['failed'], [])
        self.assertIn('files.ch :: 缺少当前内容通过记录',
                      ['%s :: %s' % (x['at'], x['message']) for x in body['unchecked']])

    # ---------- T4 / V4b ----------
    def test_t4_shared_and_source_are_not_deliverable(self):
        self.init_ledger()
        self.register_file(fid='sh', path='sh.md', kind='shared', body='shared')
        self.state_cmd('reading', '--status', '跳过', '--reason', 'skip')
        rc_plain, body_plain = self.check_cmd()
        rc_final, body = self.check_cmd(final=True)
        self.assertEqual((rc_plain, body_plain['failed'], body_plain['unchecked']), (0, [], []))
        self.assertEqual(rc_final, 1)
        self.assertTrue(any('没有可交付内容' in f['message'] for f in body['failed']))
        self.register_file()                       # 补一个 chapter
        rc_after, body_after = self.check_cmd(final=True)
        self.assertFalse(any('没有可交付内容' in f['message'] for f in body_after['failed']))

        self.reset()                               # source-only 且全部通过
        self.init_ledger()
        self.register_file(fid='s1', path='a.md', kind='source', body='source a')
        self.register_file(fid='s2', path='b.md', kind='source', body='source b')
        self.submit_review(['s1', 's2'])
        self.state_cmd('reading', '--status', '跳过', '--reason', 'skip')
        rc, body = self.check_cmd(final=True)
        self.assertEqual(rc, 1)
        self.assertTrue(any('没有可交付内容' in f['message'] for f in body['failed']))

    # ---------- T5 / V4c ----------
    def test_t5_deliverable_and_pending_residue(self):
        self.init_ledger()
        self.register_file(fid='ch1', path='01.md', body='one')
        self.register_file(fid='ch2', path='02.md', body='two')
        self.submit_review(['ch1', 'ch2'])
        self.state_cmd('reading', '--status', '跳过', '--reason', 'skip')
        self.assertEqual(self.check_cmd(final=True)[0], 0)          # 正常交付

        self.put('02.md', 'two revised')                             # pending 残留
        self.state_cmd('register', '--id', 'ch2', '--path', '02.md', '--kind', 'chapter', '--actor', 'w')
        self.submit_review(['ch2'], rid='v2')
        rc, body = self.check_cmd(final=True)
        self.assertEqual(rc, 2)
        self.assertIn('评审适用性待确认',
                      [x['message'] for x in body['unchecked']])
        self.submit_review(['ch1'], rid='v3')                        # 补齐旧目标
        self.assertEqual(self.check_cmd(final=True)[0], 0)

        self.reset()                                                 # 同目标先通过后待修订
        self.init_ledger()
        self.register_file()
        self.submit_review(['ch'])
        self.submit_review(['ch'], rid='v2', status='待修订')
        rc, body = self.check_cmd(final=True)
        self.assertEqual(rc, 2)
        self.assertIn('当前内容尚无通过结论', [x['message'] for x in body['unchecked']])

    # ---------- T6 / V5 ----------
    def test_t6_structure_guards(self):
        self.init_ledger()
        base = self.ledger()
        for label, mutate in (('missing', lambda d: d.pop('files')),
                              ('list', lambda d: d.__setitem__('files', [])),
                              ('null', lambda d: d.__setitem__('files', None)),
                              ('zero', lambda d: d.__setitem__('files', 0)),
                              ('empty-string', lambda d: d.__setitem__('files', ''))):
            data = json.loads(json.dumps(base))
            mutate(data)
            self.write_ledger(data)
            before = self.state.read_bytes()
            for args in (('next', '--text', 'x'),
                         ('reading', '--status', '跳过', '--reason', 's'),
                         ('actor', '--id', 'w', '--identity', '/writer'),
                         ('register', '--id', 'ch', '--path', '01.md',
                          '--kind', 'chapter', '--actor', 'w')):
                self.state_cmd(*args, ok=False)
            self.assertEqual(before, self.state.read_bytes(), label)

        data = json.loads(json.dumps(base))
        data['files'] = {'ch': 'not-an-object'}
        self.write_ledger(data)
        self.assertIn('必须为对象', self.state_cmd('next', '--text', 'x', ok=False))

        self.write_ledger(base)
        for payload in ('[]', '{}'):
            self.put('_work/run/batch.json', payload)
            self.assertIn('非空数组',
                          self.state_cmd('register-batch', '--spec', '_work/run/batch.json', ok=False))

        self.reset()                                                 # init → register 回归
        self.init_ledger()
        self.register_file()
        self.assertEqual(list(self.ledger()['files']), ['ch'])

    # ---------- T8 / V6 ----------
    def test_t8_identity_and_hash_states(self):
        self.hand_ledger(identity=None)
        self.assertEqual(self.state_cmd('next', '--text', 'x').count('"saved": true'), 1)
        self.state_cmd('reading', '--status', '跳过', '--reason', 's')
        rc, body = self.check_cmd(final=True)
        self.assertEqual(rc, 2)
        self.assertTrue(any('实体身份未知' in x['message'] for x in body['unchecked']))
        self.put('_work/run/rv.md', 'report')
        self.put('_work/run/spec.json', json.dumps({'id': 'v1', 'kind': 'content', 'actor': 'rv',
                                          'report': '_work/run/rv.md', 'inputs': '_work/run/none.json',
                                          'coverage': [{'target': 'ch', 'status': '通过',
                                                        'scope': 's', 'issues': []}]},
                                         ensure_ascii=False))
        self.assertIn('冻结凭据', self.state_cmd('review', '--spec', '_work/run/spec.json', ok=False))

        self.reset()                                                 # sha256: null
        data = self.hand_ledger()
        value = self.ledger()
        value['files']['ch']['sha256'] = None
        self.write_ledger(value)
        self.assertEqual(self.state_cmd('next', '--text', 'y').count('"saved": true'), 1)
        rc, body = self.check_cmd()
        self.assertEqual(rc, 2)
        self.assertTrue(any('尚未产出或登记版本' in x['message'] for x in body['unchecked']))

        self.reset()                                                 # 贡献者缺当前 sha
        self.hand_ledger(contributors=[])
        rc, body = self.check_cmd()
        self.assertEqual(rc, 1)
        self.assertTrue(any('当前版本缺少作者或修改者登记' in f['message'] for f in body['failed']))

    # ---------- T9 / V8 V10 V11 ----------
    def test_t9_legacy_handwritten_and_malformed(self):
        self.hand_ledger()                                           # 手写 v2 账本
        for args in (('actor', '--id', 'b', '--identity', '/b'),
                     ('register', '--id', 'ch', '--path', '01.md',
                      '--kind', 'chapter', '--actor', 'w'),
                     ('freeze', '--files', 'ch', '--output', '_work/run/in.json'),
                     ('reading', '--status', '跳过', '--reason', 's'),
                     ('next', '--text', 'z')):
            self.state_cmd(*args)
        self.put('_work/run/batch.json', json.dumps([{'id': 'ch', 'path': '01.md',
                                            'kind': 'chapter', 'actor': 'w'}], ensure_ascii=False))
        self.state_cmd('register-batch', '--spec', '_work/run/batch.json')
        self.put('_work/run/rv.md', 'report')
        self.put('_work/run/spec.json', json.dumps({'id': 'v1', 'kind': 'content', 'actor': 'rv',
                                          'report': '_work/run/rv.md', 'inputs': '_work/run/in.json',
                                          'coverage': [{'target': 'ch', 'status': '通过',
                                                        'scope': 's', 'issues': []}]},
                                        ensure_ascii=False))
        self.state_cmd('review', '--spec', '_work/run/spec.json')
        self.assertEqual(self.ledger()['schema_version'], 2)

        self.reset()                                                 # v1 账本被门拒绝
        self.hand_ledger(schema=None)
        before = self.state.read_bytes()
        for args in (('actor', '--id', 'w', '--identity', '/writer'),
                     ('register', '--id', 'ch', '--path', '01.md',
                      '--kind', 'chapter', '--actor', 'w'),
                     ('freeze', '--files', 'ch', '--output', '_work/run/in.json'),
                     ('next', '--text', 'x'),
                     ('reading', '--status', '跳过', '--reason', 's')):
            self.assertIn('需要版本2', self.state_cmd(*args, ok=False))
        self.assertEqual(before, self.state.read_bytes())
        self.assertFalse((self.work / '版本').exists())

        for raw in ('null', '[]'):                                   # 畸形账本
            self.reset()
            self.state.write_text(raw, encoding='utf-8')
            before = self.state.read_bytes()
            self.assertIn('已存在', self.state_cmd('init', '--run-id', 'run', ok=False))
            self.assertEqual(before, self.state.read_bytes())
            self.assertIn('必须是 JSON 对象', self.state_cmd('next', '--text', 'x', ok=False))
            rc, _ = self.check_cmd()
            self.assertEqual(rc, 1)

    # ---------- T10 / V12 与内层键 ----------
    def test_t10_inner_keys_and_identity_projection(self):
        self.init_ledger()
        self.register_file()
        self.put('_work/run/rv.md', 'report')
        base_spec = {'id': 'v1', 'kind': 'content', 'actor': 'rv', 'report': '_work/run/rv.md',
                     'inputs': '_work/run/in.json',
                     'coverage': [{'target': 'ch', 'status': '通过', 'scope': 's', 'issues': []}]}
        self.put('_work/run/spec.json', json.dumps(base_spec, ensure_ascii=False))
        self.assertIn('冻结凭据', self.state_cmd('review', '--spec', '_work/run/spec.json', ok=False))

        self.state_cmd('freeze', '--files', 'ch', '--output', '_work/run/in.json')
        spec = dict(base_spec)
        spec['coverage'] = [{'target': 'ghost', 'status': '通过', 'scope': 's', 'issues': []}]
        self.put('_work/run/spec2.json', json.dumps(spec, ensure_ascii=False))
        self.assertIn('评审目标未登记',
                      self.state_cmd('review', '--spec', '_work/run/spec2.json', ok=False))
        self.assertIn('未登记', self.state_cmd('freeze', '--files', 'ghost',
                                              '--output', '_work/run/i2.json', ok=False))

        self.submit_review(['ch'])
        self.state_cmd('reading', '--status', '跳过', '--reason', 's')
        self.assertEqual(self.check_cmd(final=True)[0], 0)

        value = self.ledger()                                        # P10：手工改身份 → 门变 0
        value['actors']['rv']['identity'] = 'placeholder-reviewer'
        value['actors']['w']['identity'] = 'placeholder-author'
        self.write_ledger(value)
        self.assertEqual(self.check_cmd(final=True)[0], 0,
                         'P10 盲区：手工改写身份投影可让 --final 归 0（已知，须披露）')


if __name__ == '__main__':
    unittest.main()
