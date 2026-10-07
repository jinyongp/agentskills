#!/usr/bin/env node
'use strict';

// No runtime dependencies. npm ships the skill directories alongside this file.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const readline = require('node:readline/promises');

const ROOT = __dirname;
const START = '<!-- agentskills:rules:start -->';
const END = '<!-- agentskills:rules:end -->';
const NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const AGENTS = {
  codex: { project: '.agents/skills', global: '.codex/skills', rules: 'AGENTS.md', globalRules: '.codex/AGENTS.md' },
  claude: { project: '.claude/skills', global: '.claude/skills', rules: 'CLAUDE.md', globalRules: '.claude/CLAUDE.md' },
};
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const fail = message => { throw new Error(message); };

function help() {
  console.log(`Usage: agentskills <add|update|remove|list> [options]

  -a, --agent codex|claude  Target agent (add prompts; update/remove use saved targets)
  -g, --global            Install for the current user instead of this project
  --project PATH          Target project (default: current directory)
  -s, --skill NAME ...     Select skills; '*' selects all available skills on add
  --rules-only            Manage only the shared rules
  --no-rules              Manage only skills
  -y, --yes               Accept the selected changes without prompting
  -h, --help              Show this help

add defaults to all bundled skills plus shared rules. update reuses installed selections.
list shows the bundled catalog and installations in the selected scope.
Local edits, existing unowned skills, and symbolic links are never overwritten.`);
}

function parse(args) {
  const opts = { command: args.shift() || 'help', names: [], agent: null, global: false, project: process.cwd(), rules: true, skills: true, yes: false };
  while (args.length) {
    const arg = args.shift();
    if (arg === '--help' || arg === '-h') opts.command = 'help';
    else if (arg === '--global' || arg === '-g') opts.global = true;
    else if (arg === '--yes' || arg === '-y') opts.yes = true;
    else if (arg === '--rules-only') opts.skills = false;
    else if (arg === '--no-rules') opts.rules = false;
    else if (arg === '--agent' || arg === '-a' || arg === '--project') {
      const value = args.shift();
      if (!value || value.startsWith('-')) fail(`Missing value for ${arg}`);
      opts[arg === '--project' ? 'project' : 'agent'] = value;
      if (arg === '--project') opts.projectExplicit = true;
    } else if (arg === '--skill' || arg === '-s') {
      const before = opts.names.length;
      while (args.length && !args[0].startsWith('-')) opts.names.push(args.shift());
      if (opts.names.length === before) fail(`Missing value for ${arg}`);
    } else fail(`Unknown option: ${arg}`);
  }
  if (opts.command === '-h' || opts.command === '--help') opts.command = 'help';
  if (!['help', 'list', 'add', 'update', 'remove'].includes(opts.command)) fail(`Unknown command: ${opts.command}`);
  if (opts.agent && !Object.hasOwn(AGENTS, opts.agent)) fail('Agent must be codex or claude');
  if (!opts.rules && !opts.skills) fail('--rules-only and --no-rules cannot be combined');
  if (!opts.skills && opts.names.length) fail('--rules-only cannot select skills');
  if (opts.global && opts.projectExplicit) fail('--global and --project cannot be combined');
  for (const name of opts.names) if (name !== '*' && !NAME.test(name)) fail(`Invalid skill name: ${name}`);
  return opts;
}

// Walk without following symlinks, including parent directories of managed paths.
function safe(base, relative) {
  const parts = relative.split(/[\\/]/);
  if (path.isAbsolute(relative) || parts.some(p => !p || p === '.' || p === '..')) fail(`Invalid managed path: ${relative}`);
  let target = base;
  for (const part of parts) {
    target = path.join(target, part);
    if (fs.existsSync(target) || (() => { try { return fs.lstatSync(target).isSymbolicLink(); } catch { return false; } })()) {
      if (fs.lstatSync(target).isSymbolicLink()) fail(`Symbolic link at ${target}; left untouched`);
    }
  }
  return target;
}

function snapshot(directory) {
  const files = {};
  function walk(current, relative = '') {
    for (const entry of fs.readdirSync(current, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const key = relative ? `${relative}/${entry.name}` : entry.name;
      const target = path.join(current, entry.name);
      if (entry.isSymbolicLink()) fail(`Symbolic link at ${target}; left untouched`);
      if (entry.isDirectory()) walk(target, key);
      else if (entry.isFile()) files[key] = hash(fs.readFileSync(target));
      else fail(`Unsupported file at ${target}`);
    }
  }
  walk(directory);
  return files;
}

function equalFiles(left, right) {
  const keys = Object.keys(left);
  return keys.length === Object.keys(right).length && keys.every(key => left[key] === right[key]);
}

function catalog() {
  const result = {};
  for (const category of fs.readdirSync(path.join(ROOT, 'skills'), { withFileTypes: true })) {
    if (!category.isDirectory()) continue;
    const directory = path.join(ROOT, 'skills', category.name);
    for (const skill of fs.readdirSync(directory, { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const source = path.join(directory, skill.name);
      if (!fs.existsSync(path.join(source, 'SKILL.md'))) continue;
      if (!NAME.test(skill.name) || result[skill.name]) fail(`Invalid or duplicate skill: ${skill.name}`);
      result[skill.name] = { source, category: category.name };
    }
  }
  return result;
}

function loadState(file) {
  if (!fs.existsSync(file)) return { version: 1, agents: {} };
  const state = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (state.version !== 1 || !state.agents || typeof state.agents !== 'object' || Array.isArray(state.agents)) fail(`Invalid installation record: ${file}`);
  for (const [agent, record] of Object.entries(state.agents)) {
    if (!Object.hasOwn(AGENTS, agent) || !record || typeof record.skills !== 'object' || !record.skills || Array.isArray(record.skills)) fail(`Invalid agent record: ${agent}`);
    for (const [name, files] of Object.entries(record.skills)) {
      if (!NAME.test(name) || !files || typeof files !== 'object' || Array.isArray(files)) fail(`Invalid skill record: ${name}`);
      for (const [key, digest] of Object.entries(files)) {
        if (key.split(/[\\/]/).some(p => !p || p === '.' || p === '..') || path.isAbsolute(key) || !/^[a-f0-9]{64}$/.test(digest)) fail(`Invalid file record: ${key}`);
      }
    }
    if (record.rules && (typeof record.rules !== 'object' || !/^[a-f0-9]{64}$/.test(record.rules.hash))) fail('Invalid rules record');
  }
  return state;
}

function atomicWrite(file, content) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(temporary, content, { mode: fs.existsSync(file) ? fs.statSync(file).mode : 0o600, flag: 'wx' });
    fs.renameSync(temporary, file);
  } finally { if (fs.existsSync(temporary)) fs.unlinkSync(temporary); }
}

function rulesBlock(text, file) {
  const starts = text.split(START).length - 1;
  const ends = text.split(END).length - 1;
  if (!starts && !ends) return null;
  const start = text.indexOf(START), end = text.indexOf(END) + END.length;
  if (starts !== 1 || ends !== 1 || end <= start || (start && text[start - 1] !== '\n') || (end < text.length && !['\n', '\r'].includes(text[end]))) fail(`Damaged rules markers in ${file}; left untouched`);
  return { start, end, text: text.slice(start, end) };
}

async function main() {
  const opts = parse(process.argv.slice(2));
  if (opts.command === 'help') return help();
  const base = fs.realpathSync(opts.global ? os.homedir() : path.resolve(opts.project));
  const stateFile = safe(base, opts.global ? '.local/share/agentskills/install.json' : '.agents/agentskills.json');
  const available = catalog();
  if (opts.command === 'list') {
    const state = loadState(stateFile);
    for (const name of Object.keys(available).sort()) console.log(`${available[name].category}/${name}`);
    console.log(`\nInstalled (${opts.global ? 'global' : base}):`);
    for (const [agent, record] of Object.entries(state.agents)) {
      if (!opts.agent || opts.agent === agent) console.log(`${agent}: ${Object.keys(record.skills).sort().join(', ') || 'no skills'}${record.rules ? '; shared rules' : ''}`);
    }
    return;
  }
  let prompt;
  try {
    if (!opts.yes) {
      if (!process.stdin.isTTY) fail('Non-interactive input: select --agent for add and pass --yes');
      prompt = readline.createInterface({ input: process.stdin, output: process.stdout });
    }
    if (opts.command === 'add' && !opts.agent) {
      if (!prompt) fail('add requires --agent codex|claude with --yes');
      opts.agent = (await prompt.question('Agent [codex/claude] (codex): ')).trim() || 'codex';
      if (!Object.hasOwn(AGENTS, opts.agent)) fail('Agent must be codex or claude');
      if (!opts.global && opts.project === process.cwd()) opts.global = (await prompt.question('Scope [project/global] (project): ')).trim() === 'global';
      if (opts.skills && !opts.names.length) {
        console.log(Object.keys(available).sort().join(', '));
        opts.names = (await prompt.question("Skills (space-separated names, '*' for all) (*): ")).trim().split(/\s+/).filter(Boolean);
      }
      // Scope selection changes the base and installation record; restart with explicit choices.
      const args = ['add', '--agent', opts.agent, ...(opts.global ? ['--global'] : ['--project', opts.project]), ...(opts.names.length ? ['--skill', ...opts.names] : []), ...(!opts.rules ? ['--no-rules'] : []), ...(!opts.skills ? ['--rules-only'] : [])];
      prompt.close(); prompt = null;
      process.argv = [...process.argv.slice(0, 2), ...args];
      return main();
    }
    fs.mkdirSync(path.dirname(stateFile), { recursive: true });
    const lock = safe(base, path.relative(base, stateFile) + '.lock');
    let handle;
    try { handle = fs.openSync(lock, 'wx'); } catch (error) {
      if (error.code === 'EEXIST') fail(`Another operation may be running; inspect ${lock} before removing a stale lock`);
      throw error;
    }
    try {
      const state = loadState(stateFile);
      const targets = opts.agent ? [opts.agent] : Object.keys(state.agents);
      if (!targets.length) fail('No recorded installations in this scope; use add first');
      const operations = [];
      const requested = [...new Set(opts.names)];
      const all = requested.includes('*') || !requested.length;
      for (const name of requested.filter(n => n !== '*')) {
        if (opts.command === 'add' && !available[name]) fail(`Unknown skill: ${name}`);
        if (opts.command !== 'add' && !targets.some(a => state.agents[a]?.skills[name])) fail(`Skill is not installed in the selected scope: ${name}`);
      }
      for (const agent of targets) {
        const config = AGENTS[agent];
        const record = state.agents[agent] || { skills: {} };
        const names = !opts.skills ? [] : (opts.command === 'add' && all ? Object.keys(available) : opts.command === 'add' ? requested : Object.keys(record.skills).filter(n => all || requested.includes(n)));
        for (const name of names.sort()) {
          const target = safe(base, `${opts.global ? config.global : config.project}/${name}`);
          if (fs.existsSync(target)) {
            if (!fs.statSync(target).isDirectory()) fail(`Not a skill directory: ${target}`);
            if (!record.skills[name]) fail(`Existing unowned skill: ${target}; left untouched`);
            if (!equalFiles(snapshot(target), record.skills[name])) fail(`Locally modified skill: ${target}; left untouched`);
          } else if (record.skills[name] && opts.command !== 'remove') fail(`Installed skill is missing: ${target}; restore it or remove its record first`);
          if (opts.command !== 'remove' && !available[name]) fail(`Skill no longer bundled: ${name}; remove explicitly`);
          const files = opts.command === 'remove' ? null : snapshot(available[name].source);
          operations.push({ label: `${opts.command} ${agent}/${name}`, apply() {
            if (opts.command === 'remove') {
              fs.rmSync(target, { recursive: true, force: true }); delete record.skills[name];
            } else {
              fs.mkdirSync(path.dirname(target), { recursive: true });
              const temporary = `${target}.${crypto.randomUUID()}.tmp`, backup = `${target}.${crypto.randomUUID()}.bak`;
              try {
                fs.cpSync(available[name].source, temporary, { recursive: true, verbatimSymlinks: true });
                if (fs.existsSync(target)) fs.renameSync(target, backup);
                try { fs.renameSync(temporary, target); } catch (error) { if (fs.existsSync(backup)) fs.renameSync(backup, target); throw error; }
                fs.rmSync(backup, { recursive: true, force: true }); record.skills[name] = files;
              } finally { fs.rmSync(temporary, { recursive: true, force: true }); }
            }
            state.agents[agent] = record;
          } });
        }
        if (opts.rules && (opts.command === 'add' || record.rules)) {
          const file = safe(base, opts.global ? config.globalRules : config.rules);
          const existed = fs.existsSync(file);
          const text = existed ? fs.readFileSync(file, 'utf8') : '';
          const previous = rulesBlock(text, file);
          if (previous && !record.rules) fail(`Existing unowned rules block in ${file}; left untouched`);
          if (record.rules && (!previous || hash(previous.text) !== record.rules.hash)) fail(`Locally modified or missing rules block in ${file}; left untouched`);
          const next = `${START}\n${fs.readFileSync(path.join(ROOT, 'rules/base.md'), 'utf8').trimEnd()}\n${END}`;
          const replacement = opts.command === 'remove' ? '' : next;
          // Prepend a newline-terminated block so removing it restores existing prose byte-for-byte.
          const content = previous ? text.slice(0, previous.start) + replacement + text.slice(previous.end) : `${next}\n${text}`;
          const removing = opts.command === 'remove';
          const final = removing && previous ? text.slice(0, previous.start) + text.slice(previous.end + (text[previous.end] === '\n' ? 1 : 0)) : content;
          operations.push({ label: `${opts.command} ${agent}/shared-rules`, apply() {
            if (removing && record.rules.created && final === '') fs.unlinkSync(file);
            else atomicWrite(file, final);
            if (removing) delete record.rules;
            else record.rules = { hash: hash(next), created: record.rules?.created ?? !existed };
            state.agents[agent] = record;
          } });
        }
      }
      if (!operations.length) fail('No matching installed items');
      console.log(`${opts.global ? 'Global' : 'Project'}: ${base}\n${operations.map(o => o.label).join('\n')}`);
      if (prompt && !/^y(es)?$/i.test((await prompt.question('Apply? [y/N] ')).trim())) { console.log('Cancelled.'); return; }
      for (const operation of operations) {
        operation.apply();
        atomicWrite(stateFile, JSON.stringify(state, null, 2) + '\n');
      }
      console.log(`Done. Installation record: ${stateFile}`);
    } finally { fs.closeSync(handle); fs.unlinkSync(lock); }
  } finally { prompt?.close(); }
}

main().catch(error => { console.error(`Error: ${error.message}`); process.exitCode = 1; });
