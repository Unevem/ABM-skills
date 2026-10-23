#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const PACKAGE_ROOT = path.resolve(__dirname, '..');

function printUsage() {
  console.log(`
ABMforAI CLI - Setup and Governance for AI Coding Assistants

Usage:
  npx abmforai setup [options]     Install skills, rules, and tools into a project
  npx abmforai doctor [options]    Verify that ABMforAI is correctly configured
  npx abmforai --help              Show this help message

Options:
  --target <dir>    Target directory for installation (default: current directory)
  --dry-run         Preview what files would be copied without making changes
`);
}

function copyDirectory(src, dest, dryRun) {
  if (!fs.existsSync(src)) return;
  if (!dryRun) {
    fs.mkdirSync(dest, { recursive: true });
    fs.cpSync(src, dest, { recursive: true });
  }
}

function copyFile(src, dest, dryRun) {
  if (!fs.existsSync(src)) return;
  if (!dryRun) {
    const parent = path.dirname(dest);
    fs.mkdirSync(parent, { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function runSetup(args) {
  const dryRun = args.includes('--dry-run');
  const targetIndex = args.indexOf('--target');
  const targetDir = targetIndex !== -1 && args[targetIndex + 1]
    ? path.resolve(process.cwd(), args[targetIndex + 1])
    : process.cwd();

  console.log(`\nABMforAI Setup`);
  console.log('='.repeat(60));
  console.log(`Target directory: ${targetDir}`);
  if (dryRun) console.log(`Mode: DRY-RUN (no files will be written)`);
  console.log('');

  const items = [
    { type: 'dir', src: path.join(PACKAGE_ROOT, '.agents'), dest: path.join(targetDir, '.agents'), label: '.agents/ (rules and skills)' },
    { type: 'file', src: path.join(PACKAGE_ROOT, 'AGENTS.md'), dest: path.join(targetDir, 'AGENTS.md'), label: 'AGENTS.md (AI assistant governance)' },
    { type: 'dir', src: path.join(PACKAGE_ROOT, 'tools'), dest: path.join(targetDir, 'tools'), label: 'tools/ (validation and scaffolding CLIs)' }
  ];

  for (const item of items) {
    if (item.type === 'dir') {
      copyDirectory(item.src, item.dest, dryRun);
    } else {
      copyFile(item.src, item.dest, dryRun);
    }
    console.log(`  [+] Installed: ${item.label}`);
  }

  console.log('='.repeat(60));
  console.log(dryRun ? 'Dry-run preview completed.' : 'Setup completed successfully.');
  console.log('\nNext steps:');
  console.log('1. Open your AI coding assistant (Antigravity, Cursor, Claude Code, Copilot) in this project.');
  console.log('2. Start with prompt:');
  console.log('   "I want to build an agent-based model to study [phenomenon].');
  console.log('    Follow the ABMforAI methodology in .agents/skills/abm-modeler/."\n');
}

function runDoctor(args) {
  const targetIndex = args.indexOf('--target');
  const targetDir = targetIndex !== -1 && args[targetIndex + 1]
    ? path.resolve(process.cwd(), args[targetIndex + 1])
    : process.cwd();

  console.log(`\nABMforAI Doctor`);
  console.log('='.repeat(60));
  console.log(`Inspecting workspace: ${targetDir}\n`);

  const required = [
    { path: path.join(targetDir, 'AGENTS.md'), label: 'AGENTS.md governance file' },
    { path: path.join(targetDir, '.agents', 'rules', 'human-review.md'), label: '.agents/rules/human-review.md' },
    { path: path.join(targetDir, '.agents', 'rules', 'no-undocumented-assumptions.md'), label: '.agents/rules/no-undocumented-assumptions.md' },
    { path: path.join(targetDir, '.agents', 'skills', 'abm-modeler', 'SKILL.md'), label: '.agents/skills/abm-modeler/SKILL.md' },
    { path: path.join(targetDir, '.agents', 'skills', 'abm-reviewer', 'SKILL.md'), label: '.agents/skills/abm-reviewer/SKILL.md' },
    { path: path.join(targetDir, 'tools', 'tasks.py'), label: 'tools/tasks.py' },
    { path: path.join(targetDir, 'tools', 'odd_validator.py'), label: 'tools/odd_validator.py' },
    { path: path.join(targetDir, 'tools', 'verify_model.py'), label: 'tools/verify_model.py' },
    { path: path.join(targetDir, 'tools', 'scaffold_abm.py'), label: 'tools/scaffold_abm.py' }
  ];

  let missing = 0;
  for (const req of required) {
    if (fs.existsSync(req.path)) {
      console.log(`  [OK] ${req.label}`);
    } else {
      console.log(`  [MISSING] ${req.label}`);
      missing++;
    }
  }

  console.log('='.repeat(60));
  if (missing === 0) {
    console.log('Verdict: HEALTHY - All ABMforAI components are present and ready.\n');
  } else {
    console.log(`Verdict: INCOMPLETE - ${missing} component(s) missing. Run 'npx abmforai setup' to install.\n`);
    process.exit(1);
  }
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'setup';

  if (command === '--help' || command === '-h' || command === 'help') {
    printUsage();
    return;
  }

  if (command === 'setup') {
    runSetup(args.slice(1));
    return;
  }

  if (command === 'doctor') {
    runDoctor(args.slice(1));
    return;
  }

  if (command.startsWith('-')) {
    runSetup(args);
    return;
  }

  console.error(`Unknown command: ${command}`);
  printUsage();
  process.exit(1);
}

main();
