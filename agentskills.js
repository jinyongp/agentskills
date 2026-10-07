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
const COMMANDS = {
  add: 'Install selected skills and shared rules; prompt for unspecified choices.',
  update: 'Refresh recorded installations; new skills require add.',
  remove: 'Remove recorded skills and rules; no selection means all in this scope.',
  list: 'Show available skills and recorded installations in this scope.',
};
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const fail = message => { throw new Error(message); };

function help(topic) {
  const examples = {
    add: 'agentskills add\n  agentskills add --agent codex --skill review-loop verify --yes\n  agentskills add --agent claude --global --rules-only --yes',
    update: 'agentskills update\n  agentskills update --global --yes\n  agentskills update --skill verify --no-rules --yes',
    remove: 'agentskills remove --skill verify --no-rules\n  agentskills remove --global',
    list: 'agentskills list\n  agentskills list --global --agent codex',
  };
  console.log(`Usage: agentskills ${topic || '<command>'} [options]

${topic ? COMMANDS[topic] : 'Commands:\n' + Object.entries(COMMANDS).map(([name, description]) => `  ${name.padEnd(8)} ${description}`).join('\n')}

  -a, --agent codex|claude  Target agent (add prompts; update/remove use saved targets)
  -g, --global             Use the current user's global installation
      --project PATH       Use an existing project directory (default: current directory)
${topic === 'list' ? '' : `  -s, --skill NAME ...     Select skills; '*' means all (quote it in your shell)
      --rules-only         Manage shared rules without skills
      --no-rules           Manage skills without shared rules
  -y, --yes                Apply without prompts; add also requires --agent
`}  -h, --help               Show help; also accepts help <command>

Scope defaults to the current project. Use --global again for global updates/removal.
${topic === 'list' ? '' : `Without --skill, add selects all bundled skills; update/remove select recorded skills.
Shared rules are included unless --no-rules is passed, even with --skill.
Rules are managed in AGENTS.md (Codex) or CLAUDE.md (Claude); other prose is preserved.
`}
Examples:
  ${examples[topic] || 'agentskills add\n  agentskills update --global\n  agentskills help remove'}

Run with npx @jinyongp/agentskills@latest <command> after npm publication,
or node /path/to/agentskills/agentskills.js <command> from a checkout.`);
}

function parse(args) {
  if (!args.length || args.includes('--help') || args.includes('-h') || args[0] === 'help') {
    const topic = args[0] === 'help' ? (args[1]?.startsWith('-') ? undefined : args[1]) : Object.hasOwn(COMMANDS, args[0]) ? args[0] : undefined;
    if (topic && !Object.hasOwn(COMMANDS, topic)) fail(`Unknown command: ${topic}. Run agentskills --help for available commands.`);
    return { command: 'help', topic };
  }
  const opts = { command: args.shift() || 'help', names: [], agent: null, global: false, project: process.cwd(), rules: true, skills: true, yes: false };
  while (args.length) {
    const arg = args.shift();
    if (arg === '--global' || arg === '-g') opts.global = true;
    else if (arg === '--yes' || arg === '-y') opts.yes = true;
    else if (arg === '--rules-only') { opts.skills = false; opts.rulesExplicit = true; }
    else if (arg === '--no-rules') { opts.rules = false; opts.rulesExplicit = true; }
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
  if (!Object.hasOwn(COMMANDS, opts.command)) fail(`Unknown command: ${opts.command}`);
  if (opts.agent && !Object.hasOwn(AGENTS, opts.agent)) fail('Agent must be codex or claude');
  if (!opts.rules && !opts.skills) fail('--rules-only and --no-rules cannot be combined');
  if (opts.command === 'list' && (opts.names.length || !opts.rules || !opts.skills)) fail('list does not accept skill/rule selections. Use --agent, --global, or --project to select installations.');
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
  const files = Object.create(null);
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

function bytes(file) {
  return fs.existsSync(file) ? fs.readFileSync(file) : null;
}

function sameBytes(left, right) {
  return left === null || right === null ? left === right : left.equals(right);
}

function utf8(data, file) {
  try { return new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(data); }
  catch { fail(`Rules document must be UTF-8: ${file}; left untouched. Convert it to UTF-8 before retrying, or pass --no-rules to manage skills.`); }
}

function catalog() {
  const result = Object.create(null);
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
  let state;
  try { state = JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { fail(`Cannot read installation record: ${file}. ${error.message}. Restore a valid record from backup before retrying.`); }
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

function atomicWrite(file, content, mode) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${crypto.randomUUID()}.tmp`;
  try {
    fs.writeFileSync(temporary, content, { mode: mode ?? (fs.existsSync(file) ? fs.statSync(file).mode : 0o600), flag: 'wx' });
    fs.renameSync(temporary, file);
  } finally { if (fs.existsSync(temporary)) fs.unlinkSync(temporary); }
}

function rulesBlock(text, file) {
  const starts = text.split(START).length - 1;
  const ends = text.split(END).length - 1;
  if (!starts && !ends) return null;
  const start = text.indexOf(START), end = text.indexOf(END) + END.length;
  if (starts !== 1 || ends !== 1 || end <= start || (start && text[start - 1] !== '\n') || (end < text.length && !['\n', '\r'].includes(text[end]))) fail(`Damaged rules markers in ${file}; left untouched. Repair the managed markers, or pass --no-rules to manage skills.`);
  return { start, end, text: text.slice(start, end) };
}

async function main() {
  const opts = parse(process.argv.slice(2));
  if (opts.command === 'help') return help(opts.topic);
  const available = catalog();
  let prompt;
  const cancellation = new AbortController();
  const ask = question => prompt.question(question, { signal: cancellation.signal });
  try {
    if (opts.command !== 'list' && !opts.yes) {
      if (!process.stdin.isTTY) fail(`Non-interactive input. Retry ${opts.command} with --yes${opts.command === 'add' ? ' and --agent codex (or --agent claude)' : ''}, or run in a terminal to review changes.`);
      prompt = readline.createInterface({ input: process.stdin, output: process.stdout });
      prompt.on('SIGINT', () => cancellation.abort());
      prompt.on('close', () => cancellation.abort());
    }
    if (opts.command === 'add') {
      if (!opts.agent) {
        if (!prompt) fail('add with --yes requires --agent codex or --agent claude. See agentskills add --help.');
        opts.agent = (await ask('Agent [codex/claude] (codex): ')).trim() || 'codex';
        if (!Object.hasOwn(AGENTS, opts.agent)) fail('Choose codex or claude for the agent.');
      }
      if (prompt && !opts.global && !opts.projectExplicit) {
        const scope = (await ask('Scope [project/global] (project): ')).trim() || 'project';
        if (!['project', 'global'].includes(scope)) fail('Choose project or global for the scope; no installation was started.');
        opts.global = scope === 'global';
      }
      if (prompt && opts.skills && !opts.names.length) {
        console.log(`Available skills (${Object.keys(available).length}):\n${Object.keys(available).sort().join(', ')}`);
        opts.names = (await ask("Skills (space-separated names, '*' for all) (*): ")).trim().split(/\s+/).filter(Boolean);
      }
      if (prompt && opts.rules && !opts.rulesExplicit) {
        const choice = (await ask(`Include shared rules in ${AGENTS[opts.agent].rules}? [Y/n] `)).trim().toLowerCase();
        if (!['', 'y', 'yes', 'n', 'no'].includes(choice)) fail('Choose yes or no for shared rules; no installation was started.');
        opts.rules = !['n', 'no'].includes(choice);
      }
    }
    const destination = opts.global ? os.homedir() : path.resolve(opts.project);
    if (!fs.existsSync(destination) || !fs.statSync(destination).isDirectory()) fail(`Target directory does not exist or is not a directory: ${destination}. Choose an existing directory with --project.`);
    const base = fs.realpathSync(destination);
    const stateFile = safe(base, opts.global ? '.local/share/agentskills/install.json' : '.agents/agentskills.json');
    if (opts.command === 'list') {
      const state = loadState(stateFile);
      console.log(`Available skills (${Object.keys(available).length}):`);
      for (const name of Object.keys(available).sort()) console.log(`  ${available[name].category}/${name}`);
      const targets = Object.entries(state.agents).filter(([agent]) => !opts.agent || agent === opts.agent).filter(([, record]) => Object.keys(record.skills).length || record.rules);
      console.log(`\nInstalled (${opts.global ? 'global' : 'project'}: ${base}):`);
      if (!targets.length) console.log(opts.global ? '  None recorded. Use add --global to install for this user.' : '  None recorded. Use add to install here; use list --global to check global installations.');
      for (const [agent, record] of targets) {
        console.log(`  ${agent}: ${Object.keys(record.skills).sort().join(', ') || 'no skills'}${record.rules ? '; shared rules' : ''}`);
        console.log(`    Skills: ${path.join(base, opts.global ? AGENTS[agent].global : AGENTS[agent].project)}`);
        if (record.rules) console.log(`    Rules: ${path.join(base, opts.global ? AGENTS[agent].globalRules : AGENTS[agent].rules)}`);
      }
      return;
    }
    fs.mkdirSync(path.dirname(stateFile), { recursive: true });
    const lock = safe(base, path.relative(base, stateFile) + '.lock');
    let handle;
    try {
      const originalState = bytes(stateFile);
      const state = loadState(stateFile);
      const targets = opts.agent ? [opts.agent] : Object.keys(state.agents);
      if (!targets.length) fail(`No recorded installations at ${stateFile}. Use add first, or select the installed scope with --global or --project.`);
      const operations = [];
      const requested = [...new Set(opts.names)];
      const all = requested.includes('*') || !requested.length;
      for (const name of requested.filter(n => n !== '*')) {
        if (opts.command === 'add' && !Object.hasOwn(available, name)) fail(`Unknown skill: ${name}. Run agentskills list to see available names.`);
        if (opts.command !== 'add' && !targets.some(a => state.agents[a] && Object.hasOwn(state.agents[a].skills, name))) fail(`Skill is not installed in the selected scope: ${name}. Run list with the same scope options to check installations.`);
      }
      for (const agent of targets) {
        const config = AGENTS[agent];
        const record = state.agents[agent] || { skills: {} };
        const names = !opts.skills ? [] : (opts.command === 'add' && all ? Object.keys(available) : opts.command === 'add' ? requested : Object.keys(record.skills).filter(n => all || requested.includes(n)));
        for (const name of names.sort()) {
          const target = safe(base, `${opts.global ? config.global : config.project}/${name}`);
          if (fs.existsSync(target)) {
            if (!fs.statSync(target).isDirectory()) fail(`Not a skill directory: ${target}`);
            if (!Object.hasOwn(record.skills, name)) fail(`Existing unowned skill: ${target}; left untouched. Manage it with its original installer, or choose another skill or target.`);
            if (!equalFiles(snapshot(target), record.skills[name])) fail(`Locally modified skill: ${target}; left untouched. Back up edits and restore the installed content before retrying. To replace it, move the directory aside, remove its record with remove --agent ${agent} --skill ${name} --no-rules in this scope, then add it again.`);
          } else if (Object.hasOwn(record.skills, name) && opts.command !== 'remove') fail(`Installed skill is missing: ${target}. Restore it, or use remove --agent ${agent} --skill ${name} --no-rules in this scope to clear its record, then add it again.`);
          if (opts.command !== 'remove' && !available[name]) fail(`Skill no longer bundled: ${name}; remove explicitly`);
          const files = opts.command === 'remove' ? null : snapshot(available[name].source);
          const before = fs.existsSync(target) ? snapshot(target) : null;
          operations.push({ label: `${opts.command} ${agent}/${name}`, destination: target, check() {
            safe(base, path.relative(base, target));
            const current = fs.existsSync(target) ? snapshot(target) : null;
            if (before === null ? current !== null : current === null || !equalFiles(current, before)) fail(`Skill changed after inspection: ${target}; retry to inspect the new state`);
          }, apply() {
            fs.mkdirSync(path.dirname(target), { recursive: true });
            const temporary = `${target}.${crypto.randomUUID()}.tmp`, backup = `${target}.${crypto.randomUUID()}.bak`;
            let replaced = false;
            const rollback = () => {
              if (replaced) fs.rmSync(target, { recursive: true, force: true });
              if (fs.existsSync(backup)) fs.renameSync(backup, target);
            };
            try {
              if (opts.command !== 'remove') {
                fs.cpSync(available[name].source, temporary, { recursive: true, verbatimSymlinks: true });
                if (!equalFiles(snapshot(temporary), files)) fail(`Bundled skill changed during copying: ${name}`);
              }
              if (fs.existsSync(target)) fs.renameSync(target, backup);
              if (opts.command === 'remove') delete record.skills[name];
              else { fs.renameSync(temporary, target); replaced = true; record.skills[name] = files; }
              state.agents[agent] = record;
              return { rollback, finish: () => fs.rmSync(backup, { recursive: true, force: true }), backup };
            } catch (error) { rollback(); throw error; }
            finally { fs.rmSync(temporary, { recursive: true, force: true }); }
          } });
        }
        if (opts.rules && (opts.command === 'add' || record.rules)) {
          const file = safe(base, opts.global ? config.globalRules : config.rules);
          const existed = fs.existsSync(file);
          const mode = existed ? fs.statSync(file).mode : 0o600;
          const original = bytes(file);
          const text = existed ? utf8(original, file) : '';
          const previous = rulesBlock(text, file);
          if (previous && !record.rules) fail(`Existing unowned rules block in ${file}; left untouched. Pass --no-rules to manage skills without this block.`);
          if (record.rules && (!previous || hash(previous.text) !== record.rules.hash)) fail(`Locally modified or missing rules block in ${file}; left untouched. Restore the managed block, or pass --no-rules to manage skills without changing rules.`);
          const next = `${START}\n${fs.readFileSync(path.join(ROOT, 'rules/base.md'), 'utf8').trimEnd()}\n${END}`;
          const replacement = opts.command === 'remove' ? '' : next;
          // Prepend a newline-terminated block so removing it restores existing prose byte-for-byte.
          const content = previous ? text.slice(0, previous.start) + replacement + text.slice(previous.end) : `${next}\n${text}`;
          const removing = opts.command === 'remove';
          const final = removing && previous ? text.slice(0, previous.start) + text.slice(previous.end + (text[previous.end] === '\n' ? 1 : 0)) : content;
          operations.push({ label: `${opts.command} ${agent}/shared-rules`, destination: file, check() {
            safe(base, path.relative(base, file));
            if (!sameBytes(bytes(file), original)) fail(`Rules document changed after inspection: ${file}; retry to inspect the new state`);
          }, apply() {
            const backup = `${file}.${crypto.randomUUID()}.bak`;
            let replaced = false;
            const rollback = () => {
              if (replaced) fs.rmSync(file, { force: true });
              if (fs.existsSync(backup)) fs.renameSync(backup, file);
            };
            try {
              if (existed) fs.renameSync(file, backup);
              if (!(removing && record.rules.created && final === '')) { atomicWrite(file, final, mode); replaced = true; }
              if (removing) delete record.rules;
              else record.rules = { hash: hash(next), created: record.rules?.created ?? !existed };
              state.agents[agent] = record;
              return { rollback, finish: () => fs.rmSync(backup, { force: true }), backup };
            } catch (error) { rollback(); throw error; }
          } });
        }
      }
      if (!operations.length) fail(`No matching installed items at ${stateFile}. Run list with the same scope and agent options.`);
      console.log(`${opts.global ? 'Global' : 'Project'}: ${base}\nPlanned changes (${operations.length}):\n${operations.map(o => `  ${o.label} -> ${o.destination}`).join('\n')}`);
      if (prompt && !/^y(es)?$/i.test((await ask('Apply? [y/N] ')).trim())) { console.log('Cancelled. No selected changes applied.'); return; }
      safe(base, path.relative(base, lock));
      try { handle = fs.openSync(lock, 'wx'); } catch (error) {
        if (error.code === 'EEXIST') fail(`Another operation may be running; inspect ${lock} before removing a stale lock`);
        throw error;
      }
      safe(base, path.relative(base, stateFile));
      if (!sameBytes(bytes(stateFile), originalState)) fail(`Installation record changed after inspection: ${stateFile}; retry`);
      for (const operation of operations) operation.check();
      let completed = 0;
      try {
        for (const operation of operations) {
          operation.check();
          const transaction = operation.apply();
          try { atomicWrite(stateFile, JSON.stringify(state, null, 2) + '\n'); }
          catch (error) {
            try { transaction.rollback(); }
            catch (rollbackError) { fail(`${error.message}; rollback failed: ${rollbackError.message}${transaction.backup && fs.existsSync(transaction.backup) ? `; preserved backup: ${transaction.backup}` : ''}`); }
            throw error;
          }
          completed += 1;
          transaction.finish();
        }
      } catch (error) {
        error.message += `\nCompleted ${completed}/${operations.length} items. Earlier completed items remain.\nInstallation record: ${stateFile}\nResolve the error, then retry with the same scope and selection.`;
        throw error;
      }
      console.log(`Completed ${completed}/${operations.length} items.\nInstallation record: ${stateFile}`);
    } finally {
      if (handle !== undefined) {
        const opened = fs.fstatSync(handle);
        fs.closeSync(handle);
        safe(base, path.relative(base, lock));
        if (fs.existsSync(lock)) {
          const current = fs.lstatSync(lock);
          if (current.dev !== opened.dev || current.ino !== opened.ino) fail(`Lock changed during operation: ${lock}; left untouched`);
          fs.unlinkSync(lock);
        }
      }
    }
  } finally { prompt?.close(); }
}

main().catch(error => {
  if (error.name === 'AbortError') { console.log('Cancelled. No selected changes applied.'); process.exitCode = 130; return; }
  console.error(`Error: ${error.message}`);
  const hints = { ENOSPC: 'Free disk space before retrying.', EACCES: 'Check access permissions for the reported path.', EPERM: 'Check permissions or whether the reported file is in use.' };
  console.error(hints[error.code] || 'For usage, run agentskills --help.');
  process.exitCode = 1;
});
