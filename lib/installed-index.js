'use strict';

const fs = require('node:fs');
const path = require('node:path');

const MAX_PAGE_CHARS = 2500;

// Summaries come from the authored category catalogs, never skill bodies.
function intents(available) {
  const result = new Map();
  for (const { source } of Object.values(available)) {
    const file = path.join(path.dirname(source), 'README.md');
    if (result.has(file)) continue;
    const summaries = new Map();
    if (fs.existsSync(file)) {
      for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
        const match = /^- \[([a-z0-9-]+)\]\([^)]*\) — (.+)$/.exec(line);
        if (match) summaries.set(match[1], match[2]);
      }
    }
    result.set(file, summaries);
  }
  return name => {
    const source = available[name]?.source;
    return source ? result.get(path.join(path.dirname(source), 'README.md'))?.get(name) || name : name;
  };
}

function renderInstalledIndex(root, entries, available, indexBase) {
  if (typeof indexBase !== 'string' || !path.isAbsolute(indexBase)) throw new Error('Index base must be an absolute path');
  const summary = intents(available);
  const categories = new Map();
  for (const entry of [...entries].sort((a, b) => a.name.localeCompare(b.name, 'en'))) {
    const category = available[entry.name]?.category || 'other';
    if (!categories.has(category)) categories.set(category, []);
    const intent = summary(entry.name);
    if (intent.length > 300 || /[\r\n]/.test(intent)) throw new Error(`Invalid catalog summary: ${entry.name}`);
    categories.get(category).push(`- \`${entry.name}\` — ${intent}\n  Path: \`${entry.path}\``);
  }
  const files = {}, links = [];
  for (const [category, lines] of [...categories].sort(([a], [b]) => a.localeCompare(b, 'en'))) {
    const groups = [], reserve = 420;
    let group = [];
    for (const line of lines) {
      if (line.length + reserve > MAX_PAGE_CHARS) throw new Error(`Index entry exceeds page limit: ${category}`);
      if (group.join('\n').length + line.length + reserve > MAX_PAGE_CHARS) { groups.push(group); group = []; }
      group.push(line);
    }
    if (group.length) groups.push(group);
    let offset = 0;
    groups.forEach((rows, page) => {
      const filename = `references/catalog/${category}${page ? `.page-${page + 1}` : ''}.md`;
      const next = `references/catalog/${category}.page-${page + 2}.md`;
      const text = [`# ${category}`, '',
        `Page ${page + 1} of ${groups.length}. Entries ${offset + 1}-${offset + rows.length} of ${lines.length}; ${lines.length - rows.length} on other pages.`, '',
        ...rows, '', page + 1 < groups.length ? `Next page: \`${next}\` (relative to this skill).` : 'End of this category catalog.', ''].join('\n');
      if (text.length > MAX_PAGE_CHARS) throw new Error(`Index page exceeds limit: ${filename}`);
      files[filename] = text;
      offset += rows.length;
    });
    links.push(`- [${category}](references/catalog/${category}.md) — ${lines.length} skills; ${groups.length} pages.`);
  }
  const template = fs.readFileSync(path.join(root, 'templates/installed-index.md.tmpl'), 'utf8').replaceAll('\r\n', '\n');
  files['SKILL.md'] = template
    .replace('{{catalog}}', () => links.join('\n') || 'No task skills installed in this scope. Use other available skill metadata.')
    .replace('{{base}}', () => JSON.stringify(indexBase));
  files.LICENSE = fs.readFileSync(path.join(root, 'LICENSE'), 'utf8');
  return files;
}

module.exports = { renderInstalledIndex, MAX_PAGE_CHARS };
