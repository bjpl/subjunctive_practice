/**
 * ESLint 9.x Flat Config - Basic Template
 *
 * Equivalent to frontend/.eslintrc.json
 *
 * Features:
 * - Next.js core-web-vitals preset
 * - TypeScript support
 * - Basic custom rules
 *
 * Usage:
 * 1. Copy this file to frontend/eslint.config.mjs
 * 2. Install dependencies (see ESLINT_9_MIGRATION_GUIDE.md)
 * 3. Test: npx eslint .
 */

import { FlatCompat } from '@eslint/eslintrc';
import js from '@eslint/js';
import { fileURLToPath } from 'url';
import path from 'path';

// Mimic __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize FlatCompat for backward compatibility with Next.js config
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
});

export default [
  // Ignore patterns (replaces .eslintignore)
  {
    ignores: [
      '**/node_modules/**',
      '**/.next/**',
      '**/out/**',
      '**/build/**',
      '**/dist/**',
      '**/.cache/**',
      '**/public/**',
      '**/coverage/**',
      '**/*.config.js',
      '**/*.config.mjs',
    ],
  },

  // Use Next.js config via FlatCompat
  // This includes next/core-web-vitals and next/typescript presets
  ...compat.config({
    extends: ['next/core-web-vitals', 'next/typescript'],
  }),

  // Custom rules configuration
  {
    rules: {
      // TypeScript
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',

      // General
      'prefer-const': 'warn',
    },
  },
];
