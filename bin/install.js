#!/usr/bin/env node
// Installs the `blueprint` skill + `/blueprint` command into Claude Code, Cursor,
// and OpenCode — wherever each is present. Cross-platform (Windows/mac/Linux).
// Usage:  npx blueprint-skills install   (or: node bin/install.js)
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdirSync, copyFileSync, existsSync, readdirSync } from 'node:fs';

const pkg = join(dirname(fileURLToPath(import.meta.url)), '..');
const HOME = homedir();

// [label, skillDir, commandDir] per platform. Command dir names differ per tool.
const TARGETS = [
  ['Claude Code', join(HOME, '.claude', 'skills', 'blueprint'), join(HOME, '.claude', 'commands')],
  ['Cursor',      join(HOME, '.cursor', 'skills-cursor', 'blueprint'), join(HOME, '.cursor', 'commands')],
  ['OpenCode',    join(HOME, '.config', 'opencode', 'skills', 'blueprint'), join(HOME, '.config', 'opencode', 'command')],
];

function copyDir(src, dst) {
  mkdirSync(dst, { recursive: true });
  for (const f of readdirSync(src)) copyFileSync(join(src, f), join(dst, f));
}

console.log('Installing blueprint skill + /blueprint command...\n');
let done = 0;
for (const [label, skillDir, cmdDir] of TARGETS) {
  try {
    copyDir(join(pkg, 'skills', 'blueprint'), skillDir);        // SKILL.md + recon.mjs
    mkdirSync(cmdDir, { recursive: true });
    copyFileSync(join(pkg, 'commands', 'blueprint.md'), join(cmdDir, 'blueprint.md'));
    console.log(`  ✓ ${label}`);
    console.log(`      skill   → ${skillDir}`);
    console.log(`      command → ${join(cmdDir, 'blueprint.md')}`);
    done++;
  } catch (e) {
    console.log(`  ✗ ${label}: ${e.message}`);
  }
}
console.log(`\nInstalled into ${done}/${TARGETS.length} platforms.`);
console.log('Restart each tool, then run:  /blueprint <url>   (or say "clone this site")');
