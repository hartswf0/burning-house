#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const caseA = JSON.parse(fs.readFileSync(path.join(ROOT, 'cases', 'case_a_assist.vtx.json'), 'utf8'));
const patchAB = JSON.parse(fs.readFileSync(path.join(ROOT, 'cases', 'patch_a_to_b_goal.json'), 'utf8'));
const policies = JSON.parse(fs.readFileSync(path.join(ROOT, 'cases', 'policies_synthetic_p1_p4.json'), 'utf8'));
const validation = JSON.parse(fs.readFileSync(path.join(ROOT, 'traces', 'validation_report.json'), 'utf8'));

const outJs = `// Auto-generated offline bundle for viewer/index.html (zero-server file:// compatibility)
window.VTX_BUNDLE = ${JSON.stringify({ caseA, patchAB, policies, validation }, null, 2)};
`;
fs.writeFileSync(path.join(ROOT, 'viewer', 'bundle_data.js'), outJs);
console.log('Wrote viewer/bundle_data.js');

