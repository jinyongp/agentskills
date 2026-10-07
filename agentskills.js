#!/usr/bin/env node
'use strict';

// No runtime dependencies. npm ships the skill directories alongside this file.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const readline = require('node:readline/promises');

const ROOT = __dirname;
const PACKAGE = require('./package.json');
const BIN = Object.keys(PACKAGE.bin)[0];
const START = '<!-- agentskills:rules:start -->';
const END = '<!-- agentskills:rules:end -->';
const NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const AGENTS = {
  codex: { project: { skills: '.agents/skills', rules: 'AGENTS.md' }, global: { skills: '.codex/skills', rules: '.codex/AGENTS.md' } },
  claude: { project: { skills: '.claude/skills', rules: 'CLAUDE.md' }, global: { skills: '.claude/skills', rules: '.claude/CLAUDE.md' } },
};
const SCOPES = {
  project: { label: 'Project', root: opts => path.resolve(opts.project), record: '.agents/agentskills.json', skills: '.agents/skills' },
  global: { label: 'Global', root: () => os.homedir(), record: '.local/share/agentskills/install.json', skills: '.agents/skills' },
};
const OPTION_GROUPS = {
  target: { label: 'Target', options: {
    agent: { flags: ['--agent', '-a'], type: 'one', value: 'AGENT', default: null, choices: () => Object.keys(AGENTS), description: 'Select connections and rules; skills share one source.' },
    project: { flags: ['--project'], type: 'one', value: 'PATH', default: () => process.cwd(), description: 'Use an existing project directory.' },
    global: { flags: ['--global', '-g'], type: 'flag', default: false, conflicts: ['project'], description: 'Use the current user\'s global installation.' },
  } },
  selection: { label: 'Selection', options: {
    names: { flags: ['--skill', '-s'], type: 'many', value: 'NAME ...', default: () => [], description: 'Select skills; quote \'*\' to select all.' },
    rulesOnly: { flags: ['--rules-only'], type: 'flag', default: false, conflicts: ['noRules', 'names'], description: 'Manage shared rules without skills.' },
    noRules: { flags: ['--no-rules'], type: 'flag', default: false, description: 'Manage skills without shared rules.' },
  } },
  execution: { label: 'Execution', options: {
    yes: { flags: ['--yes', '-y'], type: 'flag', default: false, description: 'Apply without prompts.' },
    help: { flags: ['--help', '-h'], type: 'flag', default: false, description: 'Show help; also accepts help <command>.' },
  } },
};
const OPTIONS = Object.fromEntries(Object.values(OPTION_GROUPS).flatMap(group => Object.entries(group.options)));
const SCOPE_OPTIONS = Object.keys(OPTION_GROUPS.target.options);
const EDIT_OPTIONS = Object.keys(OPTIONS);
const COMMANDS = {
  add: { description: 'Install selected skills and shared rules; prompt for unspecified choices.', options: EDIT_OPTIONS, mutates: true, selection: 'catalog', requiresAgent: true,
    examples: ctx => [{}, { agent: ctx.agents[0], names: ctx.skills.slice(0, 2), yes: true }, { agent: ctx.agents.at(-1), global: true, rulesOnly: true, yes: true }] },
  update: { description: 'Refresh recorded installations; new skills require add.', options: EDIT_OPTIONS, mutates: true, selection: 'installed',
    examples: ctx => [{}, { global: true, yes: true }, { names: ctx.skills.slice(0, 1), noRules: true, yes: true }] },
  remove: { description: 'Remove recorded skills and rules; no selection means all in this scope.', options: EDIT_OPTIONS, mutates: true, selection: 'installed', removes: true,
    examples: ctx => [{ names: ctx.skills.slice(0, 1), noRules: true }, { global: true }] },
  list: { description: 'Show available skills and recorded installations in this scope.', options: [...SCOPE_OPTIONS, 'help'], mutates: false,
    examples: ctx => [{}, { global: true, agent: ctx.agents[0] }] },
};
const FLAGS = new Map(Object.entries(OPTIONS).flatMap(([key, option]) => option.flags.map(flag => [flag, key])));
const optionKeys = command => Object.keys(OPTIONS).filter(key => !command || COMMANDS[command].options.includes(key));
const flag = key => OPTIONS[key].flags[0];
const scopeOf = opts => opts.scope || (opts.global ? 'global' : 'project');
const optionDefault = option => typeof option.default === 'function' ? option.default() : option.default;
const defaults = () => Object.fromEntries(Object.entries(OPTIONS).map(([key, option]) => [key, optionDefault(option)]));
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const fail = message => { throw new Error(message); };
const CANCELLED = 'Cancelled. No selected changes applied.';
const completion = (completed, total, record) => `Completed ${completed}/${total} items.\nInstallation record: ${record}`;

function preview(scope, base, operations, unchanged) {
  const lines = [`${PACKAGE.name}@${PACKAGE.version}`, `${SCOPES[scope].label}: ${base}`, `Changes: ${operations.length}`];
  const skills = [...operations, ...unchanged].filter(item => item.kind === 'skill');
  if (skills.length) {
    lines.push('', `Shared skills: ${path.join(base, SCOPES[scope].skills)}`);
    for (const action of ['add', 'update', 'migrate', 'connect', 'disconnect', 'remove']) {
      const names = operations.filter(item => item.kind === 'skill' && item.action === action).map(item => item.name);
      if (!names.length) continue;
      const label = `${action[0].toUpperCase()}${action.slice(1)} (${names.length}):`;
      let row = `  ${label}`;
      for (const name of names) {
        if (row.length + name.length + 2 > 88) { lines.push(row); row = '   '; }
        row += `${row.trim() === label || !row.trim() ? ' ' : ', '}${name}`;
      }
      lines.push(row);
    }
    const count = unchanged.filter(item => item.kind === 'skill').length;
    if (count) lines.push(`  Unchanged: ${count} ${count === 1 ? 'skill' : 'skills'}`);
    lines.push('Connections:');
    for (const agent of [...new Set(skills.flatMap(item => item.agents))]) {
      const directory = path.join(base, AGENTS[agent][scope].skills);
      lines.push(`  ${agent}: ${directory === path.join(base, SCOPES[scope].skills) ? 'reads shared skills directly' : directory}`);
    }
  }
  for (const item of [...operations, ...unchanged].filter(item => item.kind === 'rules')) {
    lines.push(`Rules (${item.agent}): ${item.action || 'unchanged'} -> ${item.destination}`);
  }
  return lines.join('\n');
}
function commandLine(command, values = {}) {
  if (!Object.hasOwn(COMMANDS, command)) fail(`Unknown command example: ${command}`);
  for (const key of Object.keys(values)) if (!COMMANDS[command].options.includes(key)) fail(`Unsupported example option: ${command}/${key}`);
  const words = [BIN, command];
  for (const key of optionKeys(command)) {
    const value = values[key], option = OPTIONS[key];
    if (value === undefined || value === null || value === false || (Array.isArray(value) && !value.length)) continue;
    words.push(flag(key));
    if (option.type !== 'flag') words.push(...(Array.isArray(value) ? value : [value]).map(String));
  }
  parse(words.slice(1));
  return words.map(word => /^[a-zA-Z0-9_./:@-]+$/.test(word) ? word : `'${word.replaceAll("'", "'\\''")}'`).join(' ');
}

function help(topic) {
  const definition = topic ? COMMANDS[topic] : null;
  const keys = optionKeys(topic);
  const rows = keys.map(key => {
    const option = OPTIONS[key];
    const aliases = option.flags.length > 1 ? [...option.flags].reverse().join(', ') : `    ${option.flags[0]}`;
    const choices = option.choices?.();
    const initial = optionDefault(option);
    return [`${aliases}${option.value ? ` ${option.value}` : ''}`, `${option.description}${choices ? ` Choices: ${choices.join(', ')}.` : ''}${option.type === 'one' && initial !== null ? ` Default: ${initial}.` : ''}${option.conflicts ? ` Conflicts: ${option.conflicts.map(flag).join(', ')}.` : ''}`];
  });
  const width = Math.max(...rows.map(([label]) => label.length));
  const optionRows = Object.values(OPTION_GROUPS).flatMap(group => {
    const selected = Object.keys(group.options).filter(key => keys.includes(key));
    return selected.length ? [`${group.label}:`, ...selected.map(key => {
      const [label, description] = rows[keys.indexOf(key)];
      return `  ${label.padEnd(width)}  ${description}`;
    }), ''] : [];
  });
  const ctx = { agents: OPTIONS.agent.choices(), skills: Object.keys(catalog()).sort() };
  const examples = definition ? definition.examples(ctx).map(values => commandLine(topic, values)) : Object.entries(COMMANDS).map(([command, spec]) => commandLine(command, spec.examples(ctx)[0]));
  const agentRequired = definition ? (definition.requiresAgent ? [topic] : []) : Object.entries(COMMANDS).filter(([, spec]) => spec.requiresAgent).map(([command]) => command);
  const selections = definition ? [[topic, definition]] : Object.entries(COMMANDS).filter(([, spec]) => spec.mutates);
  const managesItems = !definition || definition.mutates;
  const defaultNotes = [
    'Defaults:',
    `  Scope: ${scopeOf(defaults())}. Use ${flag('global')} on every global command.`,
    ...(managesItems ? [
      `  Skills without ${flag('names')}:`,
      ...selections.map(([command, spec]) => `    ${command}: ${spec.selection === 'catalog' ? 'all bundled skills' : 'recorded skills'}`),
      `  Rules: included even with ${flag('names')}; ${flag('noRules')} skips them.`,
      '  Skills use one shared copy; updates affect every connected agent.',
      ...agentRequired.map(command => `  ${command}: prompts for unspecified choices; ${flag('yes')} requires ${flag('agent')}.`),
    ] : []), '',
  ];
  const ruleTable = [
    ['Agent', ...Object.values(SCOPES).map(scope => scope.label)],
    ...Object.entries(AGENTS).map(([agent, config]) => [agent, ...Object.keys(SCOPES).map(scope => config[scope].rules)]),
  ];
  const ruleWidths = ruleTable[0].map((_, column) => Math.max(...ruleTable.map(row => row[column].length)));
  const ruleNotes = managesItems ? [
    'Rule files:',
    ...ruleTable.map(row => `  ${row.map((cell, column) => cell.padEnd(ruleWidths[column])).join('  ').trimEnd()}`),
    '  Existing text outside managed rules is preserved.', '',
  ] : [];
  console.log([
    `Usage: ${BIN} ${topic || '<command>'} [options]`, '',
    definition ? definition.description : 'Commands:\n' + Object.entries(COMMANDS).map(([name, spec]) => `  ${name.padEnd(8)} ${spec.description}`).join('\n'), '',
    ...optionRows,
    ...defaultNotes, ...ruleNotes,
    ...(definition?.selection === 'installed' ? ['Named skill examples require an existing installation in this scope.', ''] : []),
    'Examples:',
    ...examples.map(example => `  ${example}`), '',
  ].join('\n'));
}

function parse(args) {
  if (!args.length || args.some(arg => OPTIONS.help.flags.includes(arg)) || args[0] === 'help') {
    const topic = args[0] === 'help' ? (args[1]?.startsWith('-') ? undefined : args[1]) : Object.hasOwn(COMMANDS, args[0]) ? args[0] : undefined;
    if (topic && !Object.hasOwn(COMMANDS, topic)) fail(`Unknown command: ${topic}. Run ${BIN} ${flag('help')} for available commands.`);
    return { command: 'help', topic };
  }
  const command = args.shift();
  if (!Object.hasOwn(COMMANDS, command)) fail(`Unknown command: ${command}`);
  const opts = { command, ...defaults() };
  const provided = new Set();
  while (args.length) {
    const arg = args.shift();
    const key = FLAGS.get(arg);
    if (!key) fail(`Unknown option: ${arg}`);
    if (!COMMANDS[command].options.includes(key)) fail(`Option ${arg} is not available for ${command}. See ${BIN} ${command} ${flag('help')}.`);
    const option = OPTIONS[key];
    provided.add(key);
    if (option.type === 'flag') opts[key] = true;
    else if (option.type === 'one') {
      const value = args.shift();
      if (!value || value.startsWith('-')) fail(`Missing value for ${arg}`);
      opts[key] = value;
    } else {
      const before = opts[key].length;
      while (args.length && !args[0].startsWith('-')) opts[key].push(args.shift());
      if (opts[key].length === before) fail(`Missing value for ${arg}`);
    }
  }
  for (const key of provided) {
    const option = OPTIONS[key];
    if (option.choices && !option.choices().includes(opts[key])) fail(`${flag(key)} must be one of: ${option.choices().join(', ')}.`);
    for (const conflict of option.conflicts || []) if (provided.has(conflict)) fail(`${flag(key)} and ${flag(conflict)} cannot be combined.`);
  }
  opts.projectExplicit = provided.has('project');
  opts.rulesExplicit = provided.has('rulesOnly') || provided.has('noRules');
  opts.rules = !opts.noRules;
  opts.skills = !opts.rulesOnly;
  opts.provided = provided;
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
  catch { fail(`Rules document must be UTF-8: ${file}; left untouched. Convert it to UTF-8 before retrying, or pass ${flag('noRules')} to manage skills.`); }
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

function validateFiles(files) {
  if (!files || typeof files !== 'object' || Array.isArray(files)) fail('Invalid skill file record');
  for (const [key, digest] of Object.entries(files)) {
    if (key.split(/[\\/]/).some(p => !p || p === '.' || p === '..') || path.isAbsolute(key) || !/^[a-f0-9]{64}$/.test(digest)) fail(`Invalid file record: ${key}`);
  }
}

function loadState(file) {
  if (!fs.existsSync(file)) return { version: 2, skills: {}, agents: {} };
  let state;
  try { state = JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { fail(`Cannot read installation record: ${file}. ${error.message}. Restore a valid record from backup before retrying.`); }
  if (!state || ![1, 2].includes(state.version) || !state.agents || typeof state.agents !== 'object' || Array.isArray(state.agents)) fail(`Invalid installation record: ${file}`);
  if (state.version === 1) {
    for (const record of Object.values(state.agents)) {
      if (!record || !record.skills || typeof record.skills !== 'object' || Array.isArray(record.skills)) fail(`Invalid installation record: ${file}`);
      record.legacy = record.skills;
      record.skills = Object.fromEntries(Object.keys(record.legacy).map(name => [name, true]));
    }
    state.version = 2;
    state.skills = {};
  }
  if (!state.skills || typeof state.skills !== 'object' || Array.isArray(state.skills)) fail('Invalid shared skill record');
  for (const [name, files] of Object.entries(state.skills)) {
    if (!NAME.test(name)) fail(`Invalid skill record: ${name}`);
    validateFiles(files);
  }
  for (const [agent, record] of Object.entries(state.agents)) {
    if (!Object.hasOwn(AGENTS, agent) || !record || !record.skills || typeof record.skills !== 'object' || Array.isArray(record.skills)) fail(`Invalid agent record: ${agent}`);
    if (record.legacy && (typeof record.legacy !== 'object' || Array.isArray(record.legacy))) fail('Invalid legacy record');
    for (const [name, connected] of Object.entries(record.skills)) {
      if (!NAME.test(name) || connected !== true) fail(`Invalid connection: ${agent}/${name}`);
      if (Object.hasOwn(record.legacy || {}, name)) validateFiles(record.legacy[name]);
      else if (!Object.hasOwn(state.skills, name)) fail(`Missing shared record: ${name}`);
    }
    for (const name of Object.keys(record.legacy || {})) if (!Object.hasOwn(record.skills, name)) fail(`Orphaned legacy record: ${name}`);
    if (record.rules && (typeof record.rules !== 'object' || !/^[a-f0-9]{64}$/.test(record.rules.hash))) fail('Invalid rules record');
  }
  for (const name of Object.keys(state.skills)) if (!Object.values(state.agents).some(r => Object.hasOwn(r.skills, name))) fail(`Orphaned shared record: ${name}`);
  return state;
}
function present(file) { try { fs.lstatSync(file); return true; } catch (error) { if (error.code === 'ENOENT') return false; throw error; } }

// Only an explicitly recorded connection may be a symlink, and only to its shared skill.
function describe(base, relative) {
  const target = path.join(safe(base, path.dirname(relative)), path.basename(relative));
  if (!present(target)) return null;
  const info = fs.lstatSync(target);
  if (info.isSymbolicLink()) return { link: fs.readlinkSync(target) };
  if (!info.isDirectory()) fail(`Not a skill directory: ${target}`);
  return { files: snapshot(target) };
}

function sameDescription(a, b) {
  if (a === null || b === null) return a === b;
  return a.link !== undefined || b.link !== undefined ? a.link === b.link : equalFiles(a.files, b.files);
}

function skillOperation(base, scope, state, name, selected, definition, available) {
  const sharedRelative = `${SCOPES[scope].skills}/${name}`;
  const shared = safe(base, sharedRelative);
  const owners = Object.keys(state.agents).filter(agent => Object.hasOwn(state.agents[agent].skills, name));
  const participants = [...new Set([...owners, ...selected])];
  const remaining = definition.removes ? owners.filter(agent => !selected.includes(agent)) : [...new Set([...owners, ...selected])];
  const sharedFiles = Object.hasOwn(state.skills, name) ? state.skills[name] : null;
  const legacyNative = owners.find(agent => state.agents[agent].legacy && Object.hasOwn(state.agents[agent].legacy, name) && `${AGENTS[agent][scope].skills}/${name}` === sharedRelative);
  const initial = describe(base, sharedRelative);
  if (initial && !sharedFiles && !legacyNative) fail(`Existing unowned skill: ${shared}; left untouched`);
  if (initial && (initial.link !== undefined || !equalFiles(initial.files, sharedFiles || state.agents[legacyNative].legacy[name]))) fail(`Locally modified skill: ${shared}; left untouched`);
  if (!initial && (sharedFiles || legacyNative) && !definition.removes) fail(`Installed skill is missing: ${shared}; restore it or remove its record first`);
  const inspected = new Map([[sharedRelative, initial]]);
  for (const agent of participants) {
    const relative = `${AGENTS[agent][scope].skills}/${name}`;
    if (relative === sharedRelative) continue;
    const current = describe(base, relative);
    inspected.set(relative, current);
    const owned = owners.includes(agent);
    const legacy = owned && Object.hasOwn(state.agents[agent].legacy || {}, name);
    if (!owned && current) fail(`Existing unowned skill: ${path.join(base, relative)}; left untouched`);
    if (legacy && current && (current.link !== undefined || !equalFiles(current.files, state.agents[agent].legacy[name]))) fail(`Locally modified skill: ${path.join(base, relative)}; left untouched`);
    if (owned && !legacy && current && (current.link === undefined || path.resolve(path.dirname(path.join(base, relative)), current.link) !== shared)) fail(`Changed skill connection: ${path.join(base, relative)}; left untouched`);
    if (owned && !current && !definition.removes) fail(`Installed connection is missing: ${path.join(base, relative)}; restore it or remove its record first`);
  }
  if (!definition.removes && !Object.hasOwn(available, name)) fail(`Skill no longer bundled: ${name}; remove explicitly`);
  const desired = definition.removes ? sharedFiles : snapshot(available[name].source);
  const replacements = [];
  if (definition.removes) {
    if (!remaining.length && initial) replacements.push({ relative: sharedRelative, type: 'remove' });
    // A legacy native directory can be deleted if remaining owners still have independent copies.
    else if (!sharedFiles && legacyNative && selected.includes(legacyNative) && initial) replacements.push({ relative: sharedRelative, type: 'remove' });
  } else if (!initial || !equalFiles(initial.files, desired)) {
    replacements.push({ relative: sharedRelative, type: 'copy', source: available[name].source, files: desired });
  }
  for (const [relative, current] of inspected) {
    if (relative === sharedRelative) continue;
    const agent = participants.find(a => `${AGENTS[a][scope].skills}/${name}` === relative);
    if (definition.removes) {
      if (selected.includes(agent) && current) replacements.push({ relative, type: 'remove' });
    } else {
      const link = path.relative(path.dirname(path.join(base, relative)), shared);
      if (!current || current.link !== link) replacements.push({ relative, type: 'link', link });
    }
  }
  const migration = !definition.removes && owners.some(agent => Object.hasOwn(state.agents[agent].legacy || {}, name));
  const bindingChange = definition.removes || selected.some(agent => !owners.includes(agent));
  const changed = replacements.length || migration || bindingChange;
  const action = definition.removes ? remaining.length ? 'disconnect' : 'remove'
    : migration ? 'migrate' : !initial ? 'add' : !equalFiles(initial.files, desired) ? 'update' : bindingChange || replacements.length ? 'connect' : null;
  const check = () => {
    safe(base, sharedRelative);
    for (const [relative, before] of inspected) if (!sameDescription(describe(base, relative), before)) fail(`Skill changed after inspection: ${path.join(base, relative)}; retry`);
  };
  return { kind: 'skill', name, action, changed: Boolean(changed), agents: participants, destination: shared, check, apply() {
    const saved = structuredClone(state);
    const staged = [], applied = [];
    const rollback = () => {
      for (const entry of [...applied].reverse()) {
        if (entry.replaced) fs.rmSync(entry.target, { recursive: true, force: true });
        if (present(entry.backup)) fs.renameSync(entry.backup, entry.target);
      }
      for (const key of Object.keys(state)) delete state[key];
      Object.assign(state, saved);
    };
    try {
      for (const replacement of replacements) {
        const target = path.join(safe(base, path.dirname(replacement.relative)), path.basename(replacement.relative));
        fs.mkdirSync(path.dirname(target), { recursive: true });
        const temporary = `${target}.${crypto.randomUUID()}.tmp`, backup = `${target}.${crypto.randomUUID()}.bak`;
        const entry = { target, temporary, backup, replaced: false };
        staged.push(entry);
        if (replacement.type === 'copy') {
          fs.cpSync(replacement.source, temporary, { recursive: true, verbatimSymlinks: true });
          if (!equalFiles(snapshot(temporary), replacement.files)) fail(`Bundled skill changed during copying: ${name}`);
        } else if (replacement.type === 'link') fs.symlinkSync(replacement.link, temporary, 'dir');
      }
      check();
      for (const entry of staged) {
        applied.push(entry);
        if (present(entry.target)) fs.renameSync(entry.target, entry.backup);
        if (present(entry.temporary)) { fs.renameSync(entry.temporary, entry.target); entry.replaced = true; }
      }
      if (definition.removes) {
        for (const agent of selected) {
          delete state.agents[agent].skills[name];
          if (state.agents[agent].legacy) {
            delete state.agents[agent].legacy[name];
            if (!Object.keys(state.agents[agent].legacy).length) delete state.agents[agent].legacy;
          }
        }
        if (!remaining.length) delete state.skills[name];
      } else {
        state.skills[name] = desired;
        for (const agent of remaining) {
          state.agents[agent] ||= { skills: {} };
          state.agents[agent].skills[name] = true;
          if (state.agents[agent].legacy) {
            delete state.agents[agent].legacy[name];
            if (!Object.keys(state.agents[agent].legacy).length) delete state.agents[agent].legacy;
          }
        }
      }
      return { rollback, backups: applied.map(entry => entry.backup), finish() { for (const entry of applied) fs.rmSync(entry.backup, { recursive: true, force: true }); } };
    } catch (error) {
      try { rollback(); } catch (rollbackError) { fail(`${error.message}; rollback failed: ${rollbackError.message}; backups: ${applied.map(e => e.backup).join(', ')}`); }
      throw error;
    } finally { for (const entry of staged) fs.rmSync(entry.temporary, { recursive: true, force: true }); }
  } };
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
  if (starts !== 1 || ends !== 1 || end <= start || (start && text[start - 1] !== '\n') || (end < text.length && !['\n', '\r'].includes(text[end]))) fail(`Damaged rules markers in ${file}; left untouched. Repair the managed markers, or pass ${flag('noRules')} to manage skills.`);
  return { start, end, text: text.slice(start, end) };
}

async function main() {
  const opts = parse(process.argv.slice(2));
  if (opts.command === 'help') return help(opts.topic);
  const definition = COMMANDS[opts.command];
  const available = catalog();
  let prompt;
  const cancellation = new AbortController();
  const ask = question => prompt.question(question, { signal: cancellation.signal });
  try {
    if (definition.mutates && !opts.yes) {
      if (!process.stdin.isTTY) {
        const retry = Object.fromEntries([...opts.provided].map(key => [key, opts[key]]));
        retry.yes = true;
        const needsAgent = definition.requiresAgent && !retry.agent;
        if (needsAgent) retry.agent = OPTIONS.agent.choices()[0];
        const agentNote = needsAgent ? ` Choose the intended ${flag('agent')}: ${OPTIONS.agent.choices().join(', ')}.` : '';
        fail(`Non-interactive input. Retry with ${commandLine(opts.command, retry)}, or run in a terminal to review changes.${agentNote}`);
      }
      prompt = readline.createInterface({ input: process.stdin, output: process.stdout });
      prompt.on('SIGINT', () => cancellation.abort());
      prompt.on('close', () => cancellation.abort());
    }
    if (definition.requiresAgent) {
      if (!opts.agent) {
        const choices = OPTIONS.agent.choices();
        if (!prompt) fail(`${opts.command} with ${flag('yes')} requires ${flag('agent')}. Choices: ${choices.join(', ')}. See ${BIN} ${opts.command} ${flag('help')}.`);
        opts.agent = (await ask(`Agent [${choices.join('/')}] (${choices[0]}): `)).trim() || choices[0];
        if (!choices.includes(opts.agent)) fail(`Choose one of these agents: ${choices.join(', ')}.`);
      }
      if (prompt && !opts.global && !opts.projectExplicit) {
        const choices = Object.keys(SCOPES), initial = scopeOf(opts);
        const scope = (await ask(`Scope [${choices.join('/')}] (${initial}): `)).trim() || initial;
        if (!Object.hasOwn(SCOPES, scope)) fail(`Choose one of these scopes: ${choices.join(', ')}; no installation was started.`);
        opts.scope = scope;
        opts.global = scope === 'global';
      }
      if (prompt && opts.skills && !opts.names.length) {
        console.log(`Available skills (${Object.keys(available).length}):\n${Object.keys(available).sort().join(', ')}`);
        opts.names = (await ask("Skills (space-separated names, '*' for all) (*): ")).trim().split(/\s+/).filter(Boolean);
      }
      if (prompt && opts.rules && !opts.rulesExplicit) {
        const choice = (await ask(`Include shared rules in ${AGENTS[opts.agent][scopeOf(opts)].rules}? [Y/n] `)).trim().toLowerCase();
        if (!['', 'y', 'yes', 'n', 'no'].includes(choice)) fail('Choose yes or no for shared rules; no installation was started.');
        opts.rules = !['n', 'no'].includes(choice);
      }
    }
    const scope = scopeOf(opts), scopeConfig = SCOPES[scope];
    const destination = scopeConfig.root(opts);
    if (!fs.existsSync(destination) || !fs.statSync(destination).isDirectory()) fail(`Target directory does not exist or is not a directory: ${destination}. Choose an existing directory with ${flag('project')}.`);
    const base = fs.realpathSync(destination);
    const stateFile = safe(base, scopeConfig.record);
    if (!definition.mutates) {
      const state = loadState(stateFile);
      console.log(`Available skills (${Object.keys(available).length}):`);
      for (const name of Object.keys(available).sort()) console.log(`  ${available[name].category}/${name}`);
      const targets = Object.entries(state.agents).filter(([agent]) => !opts.agent || agent === opts.agent).filter(([, record]) => Object.keys(record.skills).length || record.rules);
      console.log(`\nInstalled (${scope}: ${base}):`);
      if (!targets.length) console.log(`  None recorded. Use ${commandLine('add', opts.global ? { global: true } : {})} to install here. Check other scopes with ${flag('global')} or ${flag('project')}.`);
      const names = [...new Set(targets.flatMap(([, record]) => Object.keys(record.skills)))].sort();
      if (names.length) {
        console.log(`  Skills (${names.length}): ${names.join(', ')}`);
        if (names.some(name => Object.hasOwn(state.skills, name))) console.log(`    Shared source: ${path.join(base, SCOPES[scope].skills)}`);
      }
      for (const [agent, record] of targets) {
        console.log(`  ${agent}: ${Object.keys(record.skills).length} connections${record.rules ? '; shared rules' : ''}`);
        if (Object.keys(record.legacy || {}).length) console.log(`    Legacy copies: ${Object.keys(record.legacy).length}; add or update to migrate selected skills.`);
        console.log(`    Reads: ${path.join(base, AGENTS[agent][scope].skills)}`);
        if (record.rules) console.log(`    Rules: ${path.join(base, AGENTS[agent][scope].rules)}`);
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
      if (!targets.length) fail(`No recorded installations at ${stateFile}. Use ${commandLine('add')} first, or select the installed scope with ${flag('global')} or ${flag('project')}.`);
      const operations = [], inspections = [], unchanged = [];
      const requested = [...new Set(opts.names)];
      const all = requested.includes('*') || !requested.length;
      for (const name of requested.filter(n => n !== '*')) {
        if (definition.selection === 'catalog' && !Object.hasOwn(available, name)) fail(`Unknown skill: ${name}. Run ${commandLine('list')} to see available names.`);
        if (definition.selection === 'installed' && !targets.some(a => state.agents[a] && Object.hasOwn(state.agents[a].skills, name))) fail(`Skill is not installed in the selected scope: ${name}. Run ${commandLine('list')} with the same scope options to check installations.`);
      }
      for (const agent of targets) state.agents[agent] ||= { skills: {} };
      const names = !opts.skills ? [] : definition.selection === 'catalog'
        ? all ? Object.keys(available) : requested
        : [...new Set(targets.flatMap(agent => Object.keys(state.agents[agent].skills)))].filter(name => all || requested.includes(name));
      for (const name of names.sort()) {
        const selected = definition.selection === 'catalog' ? targets : targets.filter(agent => Object.hasOwn(state.agents[agent].skills, name));
        const operation = skillOperation(base, scope, state, name, selected, definition, available);
        inspections.push(operation);
        if (operation.changed) operations.push(operation);
        else unchanged.push(operation);
      }
      for (const agent of targets) {
        const config = AGENTS[agent];
        const record = state.agents[agent];
        if (opts.rules && (definition.selection === 'catalog' || record.rules)) {
          const file = safe(base, config[scope].rules);
          const existed = fs.existsSync(file);
          const mode = existed ? fs.statSync(file).mode : 0o600;
          const original = bytes(file);
          const text = existed ? utf8(original, file) : '';
          const previous = rulesBlock(text, file);
          if (previous && !record.rules) fail(`Existing unowned rules block in ${file}; left untouched. Pass ${flag('noRules')} to manage skills without this block.`);
          if (record.rules && (!previous || hash(previous.text) !== record.rules.hash)) fail(`Locally modified or missing rules block in ${file}; left untouched. Restore the managed block, or pass ${flag('noRules')} to manage skills without changing rules.`);
          const next = `${START}\n${fs.readFileSync(path.join(ROOT, 'rules/base.md'), 'utf8').trimEnd()}\n${END}`;
          const replacement = definition.removes ? '' : next;
          // Prepend a newline-terminated block so removing it restores existing prose byte-for-byte.
          const content = previous ? text.slice(0, previous.start) + replacement + text.slice(previous.end) : `${next}\n${text}`;
          const removing = definition.removes;
          const final = removing && previous ? text.slice(0, previous.start) + text.slice(previous.end + (text[previous.end] === '\n' ? 1 : 0)) : content;
          const operation = { kind: 'rules', agent, action: removing ? 'remove' : previous ? 'update' : 'add', destination: file, check() {
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
          } };
          inspections.push(operation);
          if (!removing && sameBytes(Buffer.from(final, 'utf8'), original)) unchanged.push({ ...operation, action: null });
          else operations.push(operation);
        }
      }
      if (!inspections.length) fail(`No matching installed items at ${stateFile}. Run ${commandLine('list')} with the same scope and agent options.`);
      console.log(preview(scope, base, operations, unchanged));
      if (!operations.length) { console.log('\nAlready up to date.'); return; }
      if (prompt && !/^y(es)?$/i.test((await ask('Apply? [y/N] ')).trim())) { console.log(CANCELLED); return; }
      safe(base, path.relative(base, lock));
      try { handle = fs.openSync(lock, 'wx'); } catch (error) {
        if (error.code === 'EEXIST') fail(`Another operation may be running; inspect ${lock} before removing a stale lock`);
        throw error;
      }
      safe(base, path.relative(base, stateFile));
      if (!sameBytes(bytes(stateFile), originalState)) fail(`Installation record changed after inspection: ${stateFile}; retry`);
      for (const inspection of inspections) inspection.check();
      let completed = 0;
      try {
        for (const operation of operations) {
          operation.check();
          const transaction = operation.apply();
          try { atomicWrite(stateFile, JSON.stringify(state, null, 2) + '\n'); }
          catch (error) {
            try { transaction.rollback(); }
            catch (rollbackError) {
              const backups = (transaction.backups || [transaction.backup]).filter(file => file && present(file));
              fail(`${error.message}; rollback failed: ${rollbackError.message}${backups.length ? `; preserved backups: ${backups.join(', ')}` : ''}`);
            }
            throw error;
          }
          completed += 1;
          transaction.finish();
        }
      } catch (error) {
        error.message += `\n${completion(completed, operations.length, stateFile)}\nEarlier completed items remain. Resolve the error, then retry with the same scope and selection.`;
        throw error;
      }
      console.log(completion(completed, operations.length, stateFile));
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
  if (error.name === 'AbortError') { console.log(CANCELLED); process.exitCode = 130; return; }
  console.error(`Error: ${error.message}`);
  const hints = { ENOSPC: 'Free disk space before retrying.', EACCES: 'Check access permissions for the reported path.', EPERM: 'Check permissions or whether the reported file is in use.' };
  console.error(hints[error.code] || `For usage, run ${BIN} ${flag('help')}.`);
  process.exitCode = 1;
});
