#!/usr/bin/env node
import { readFile, readdir, cp, mkdir, rename, symlink, access } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_SKILLS = path.resolve(HERE, '..', 'skills');

const die = (msg) => {
  console.error(`[skills] ${msg}`);
  process.exit(1);
};
const exists = async (p) => {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
};
const stamp = () => new Date().toISOString().replace(/[:.]/g, '-');

// 允许 --dir ~/xxx；PowerShell 不保证替原生命令展开 ~
const expandHome = (p) =>
  p === '~' || p.startsWith('~/') || p.startsWith('~\\') ? path.join(os.homedir(), p.slice(1)) : p;

function parseArgs(argv) {
  const opts = { force: false, link: false, all: false, dir: null };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--force' || a === '-f') opts.force = true;
    else if (a === '--link') opts.link = true;
    else if (a === '--all') opts.all = true;
    else if (a === '--project') opts.dir = path.join(process.cwd(), '.agents', 'skills');
    else if (a === '--global') opts.dir = path.join(os.homedir(), '.agents', 'skills');
    else if (a === '--dir') {
      const v = argv[++i];
      if (!v) die('--dir 需要一个路径');
      opts.dir = path.resolve(expandHome(v));
    } else if (a === '-h' || a === '--help') {
      printHelp();
      process.exit(0);
    } else if (a.startsWith('-')) {
      die(`未知参数 ${a}`);
    } else {
      positional.push(a);
    }
  }
  return { opts, positional };
}

const resolveTarget = (opts) => opts.dir ?? path.join(os.homedir(), '.agents', 'skills');

async function metaOf(dir) {
  const file = path.join(dir, 'SKILL.md');
  if (!(await exists(file))) return null;
  const text = await readFile(file, 'utf8');
  const fm = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fm) return { name: path.basename(dir), description: '(缺 frontmatter)' };
  const pick = (key) => {
    const m = fm[1].match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
    return m ? m[1].trim().replace(/^["']|["']$/g, '') : '';
  };
  return { name: pick('name') || path.basename(dir), description: pick('description') };
}

async function available() {
  const entries = await readdir(REPO_SKILLS, { withFileTypes: true });
  return entries.filter((e) => e.isDirectory()).map((e) => e.name).sort();
}

async function cmdList() {
  const names = await available();
  if (!names.length) {
    console.log('仓库里还没有 skill。在 skills/ 下建一个目录并放入 SKILL.md。');
    return;
  }
  const rows = [];
  for (const n of names) {
    const m = (await metaOf(path.join(REPO_SKILLS, n))) ?? { name: n, description: '(缺 SKILL.md)' };
    rows.push([m.name, m.description]);
  }
  const width = Math.max(...rows.map((r) => r[0].length));
  for (const [n, d] of rows) console.log(`${n.padEnd(width)}  ${d}`);
}

async function cmdAdd(names, opts) {
  const have = await available();
  const picked = opts.all ? have : names;
  if (!picked.length) die('用法: add <skill...> 或 add --all（--help 看全部参数）');

  const missing = picked.filter((n) => !have.includes(n));
  if (missing.length) {
    die(`仓库里没有: ${missing.join(', ')}\n可用: ${have.join(', ') || '(空)'}`);
  }

  const destRoot = resolveTarget(opts);
  await mkdir(destRoot, { recursive: true });

  for (const name of picked) {
    const src = path.join(REPO_SKILLS, name);
    const dest = path.join(destRoot, name);

    if (await exists(dest)) {
      if (!opts.force) {
        die(`${dest} 已存在。确认覆盖请加 --force（旧版本会先移到 ${path.join(destRoot, '.trash')}）`);
      }
      const trash = path.join(destRoot, '.trash', `${name}-${stamp()}`);
      await mkdir(path.dirname(trash), { recursive: true });
      await rename(dest, trash);
      console.log(`旧版本已移到 ${trash}`);
    }

    if (opts.link) {
      await symlink(src, dest, 'junction');
      console.log(`✓ ${name} -> ${dest}（junction，指向仓库）`);
    } else {
      await cp(src, dest, { recursive: true, errorOnExist: true, force: false });
      console.log(`✓ ${name} -> ${dest}`);
    }

    if (!(await exists(path.join(dest, 'SKILL.md')))) {
      console.warn(`  警告: ${name} 安装后没有 SKILL.md，agent 可能无法识别。`);
    }
  }

  console.log(`\n完成，共 ${picked.length} 个。目标目录: ${destRoot}`);
}

function printHelp() {
  console.log(`skills — 安装本仓库的 agent skill

用法:
  skills list                     列出仓库里的 skill
  skills add <name...>            安装指定 skill
  skills add --all                安装全部
  skills where                    打印默认安装目录

选项:
  --dir <path>                    装到指定目录
  --project                       装到 ./.agents/skills
  --global                        装到 ~/.agents/skills（默认）
  --force, -f                     目标已存在时覆盖（旧版本移入 .trash/）
  --link                          用 junction 指向仓库，不复制文件
  -h, --help                      显示本帮助

示例:
  npx github:GavinMo1/skills-repo add plan-review-loop
  npx github:GavinMo1/skills-repo add --all --project
  node bin/cli.mjs add plan-review-loop --dir C:\\tmp\\skills-test`);
}

const { opts, positional } = parseArgs(process.argv.slice(2));
const [cmd, ...rest] = positional;

if (!cmd || cmd === 'help') {
  printHelp();
} else if (cmd === 'list') {
  await cmdList();
} else if (cmd === 'add' || cmd === 'install') {
  await cmdAdd(rest, opts);
} else if (cmd === 'where') {
  console.log(resolveTarget(opts));
} else {
  die(`未知命令 ${cmd}，用 --help 看用法`);
}

