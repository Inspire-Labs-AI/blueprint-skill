#!/usr/bin/env node
// Installs the blueprint skill set + `/blueprint` command into Claude Code, Cursor,
// and OpenCode — wherever each is present. Cross-platform (Windows/mac/Linux).
// Usage:  npx blueprint-skills install   (or: node bin/install.js)
//
// Copies ALL skills, not just the entry one: `blueprint` routes to bp-mandate,
// bp-manifest, bp-evidence and one bp-* skill per stage. Installing only the entry
// skill leaves it pointing at skills that aren't there.
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdirSync, copyFileSync, readdirSync, statSync } from 'node:fs';

const pkg = join(dirname(fileURLToPath(import.meta.url)), '..');
const HOME = homedir();

// [label, skillsRoot, commandDir] per platform. Directory names differ per tool.
const TARGETS = [
  ['Claude Code', join(HOME, '.claude', 'skills'), join(HOME, '.claude', 'commands')],
  ['Cursor',      join(HOME, '.cursor', 'skills-cursor'), join(HOME, '.cursor', 'commands')],
  ['OpenCode',    join(HOME, '.config', 'opencode', 'skills'), join(HOME, '.config', 'opencode', 'command')],
];

function copyDir(src, dst) {
  mkdirSync(dst, { recursive: true });
  for (const f of readdirSync(src)) {
    const s = join(src, f), d = join(dst, f);
    if (statSync(s).isDirectory()) copyDir(s, d);
    else copyFileSync(s, d);
  }
}

const skills = readdirSync(join(pkg, 'skills'));
console.log(`Installing ${skills.length} blueprint skills + /blueprint command...\n`);

let done = 0;
for (const [label, skillsRoot, cmdDir] of TARGETS) {
  try {
    for (const name of skills) copyDir(join(pkg, 'skills', name), join(skillsRoot, name));
    mkdirSync(cmdDir, { recursive: true });
    copyFileSync(join(pkg, 'commands', 'blueprint.md'), join(cmdDir, 'blueprint.md'));
    console.log(`  ✓ ${label}`);
    console.log(`      skills  → ${skillsRoot}${' '}(${skills.length} skills)`);
    console.log(`      command → ${join(cmdDir, 'blueprint.md')}`);
    done++;
  } catch (e) {
    console.log(`  ✗ ${label}: ${e.message}`);
  }
}

console.log(`\nInstalled into ${done}/${TARGETS.length} platforms.`);
console.log('Restart each tool, then run:  /blueprint <url>');
console.log('Modes: explore · research · prd · build · ask — just say what you want.');
