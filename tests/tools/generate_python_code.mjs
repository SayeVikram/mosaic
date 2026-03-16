import { readFile } from 'node:fs/promises';
import { extname, resolve } from 'node:path';
import { parse as parseYAML } from 'yaml';

import { astToPython } from '../../packages/vgplot/spec/src/ast-to-python.js';
import { parseSpec } from '../../packages/vgplot/spec/src/parse-spec.js';

const filePath = process.argv[2];

if (!filePath) {
  console.error('Usage: node tests/tools/generate_python_code.mjs <spec.{json,yaml}>');
  process.exit(2);
}

const absPath = resolve(filePath);
const text = await readFile(absPath, 'utf8');
const ext = extname(absPath).toLowerCase();
const input = ext === '.yaml' || ext === '.yml' ? parseYAML(text) : JSON.parse(text);
const ast = parseSpec(input);

process.stdout.write(astToPython(ast));
