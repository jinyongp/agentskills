'use strict';

const fs = require('node:fs');
const path = require('node:path');

function readRoutes(root) {
  const routes = JSON.parse(fs.readFileSync(path.join(root, 'lib/skill-routes.json'), 'utf8'));
  if (!Array.isArray(routes)) throw new Error('Skill routes must be a list');
  const seen = new Set();
  const text = (value, limit) => typeof value === 'string' && value.length > 0 && value.length <= limit && !/[\r\n]/.test(value);
  for (const route of routes) {
    if (!route || typeof route !== 'object' || Array.isArray(route)) throw new Error('Invalid skill route');
    if (!text(route.id, 64) || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(route.id) || seen.has(route.id)) throw new Error('Invalid or duplicate skill route id');
    seen.add(route.id);
    if (!text(route.title, 120) || !text(route.when, 300)) throw new Error(`Invalid route description: ${route.id}`);
    if (!Array.isArray(route.choices) || !route.choices.length) throw new Error(`Missing route choices: ${route.id}`);
    const skills = new Set();
    for (const choice of route.choices) {
      if (!choice || typeof choice !== 'object' || Array.isArray(choice)) throw new Error(`Invalid route choice: ${route.id}`);
      if (!text(choice.skill, 64) || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(choice.skill) || skills.has(choice.skill)) throw new Error(`Invalid or duplicate route skill: ${route.id}`);
      if (!text(choice.when, 300)) throw new Error(`Invalid route condition: ${route.id}/${choice.skill}`);
      skills.add(choice.skill);
    }
  }
  return routes;
}

function renderRoutes(root, paths, limit) {
  const files = {}, links = [], covered = new Set();
  for (const route of readRoutes(root)) {
    const rows = [];
    for (const choice of route.choices) {
      if (!paths.has(choice.skill)) continue;
      rows.push(`- ${choice.when}\n  Skill: \`${choice.skill}\`\n  Path: \`${paths.get(choice.skill)}\``);
      covered.add(choice.skill);
    }
    if (!rows.length) continue;
    const pageText = (chunk, offset, number, count) => [
      `# ${route.title}`, '', route.when, '',
      'Choose by the requested outcome and permission; these are alternatives, not a sequence.',
      `Page ${number} of ${count}. Choices ${offset + 1}-${offset + chunk.length} of ${rows.length}; ${rows.length - chunk.length} on other pages.`,
      '', ...chunk, '', number < count ? `Next page: \`references/routes/${route.id}.page-${number + 1}.md\` (relative to this skill).` : 'End of this decision route.', '',
    ].join('\n');
    const groups = [];
    let current = [], offset = 0;
    for (const row of rows) {
      const candidate = [...current, row];
      if (pageText(candidate, offset, 999998, 999999).length > limit) {
        if (!current.length) throw new Error(`Decision route entry exceeds page limit: ${route.id}`);
        groups.push(current);
        offset += current.length;
        current = [row];
        if (pageText(current, offset, 999998, 999999).length > limit) throw new Error(`Decision route entry exceeds page limit: ${route.id}`);
      } else current = candidate;
    }
    groups.push(current);
    offset = 0;
    groups.forEach((chunk, page) => {
      const filename = `references/routes/${route.id}${page ? `.page-${page + 1}` : ''}.md`;
      const content = pageText(chunk, offset, page + 1, groups.length);
      if (content.length > limit) throw new Error(`Decision route page exceeds limit: ${route.id}`);
      files[filename] = content;
      offset += chunk.length;
    });
    links.push(`- [${route.title}](references/routes/${route.id}.md) — ${route.when}`);
  }
  return { files, links, unrouted: [...paths.keys()].filter(name => !covered.has(name)) };
}

module.exports = { readRoutes, renderRoutes };
