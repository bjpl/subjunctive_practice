# ESLint 9.x Migration Guide - Flat Config for Next.js TypeScript Project

## Table of Contents
1. [Overview](#overview)
2. [Breaking Changes in ESLint 9.x](#breaking-changes-in-eslint-9x)
3. [Flat Config Philosophy](#flat-config-philosophy)
4. [Migration Prerequisites](#migration-prerequisites)
5. [Step-by-Step Migration](#step-by-step-migration)
6. [Configuration Examples](#configuration-examples)
7. [Plugin-Specific Migration](#plugin-specific-migration)
8. [Testing and Validation](#testing-and-validation)
9. [Compatibility Issues](#compatibility-issues)
10. [Rollback Plan](#rollback-plan)

---

## Overview

This guide covers migrating from ESLint 8.57.1 with `.eslintrc.json` configuration to ESLint 9.37.0 with flat config (`eslint.config.js`/`eslint.config.mjs`) for our Next.js 14.2.0 TypeScript project.

### Current Configuration
- **ESLint Version**: 8.57.1
- **Config Format**: `.eslintrc.json`
- **Framework**: Next.js 14.2.0
- **Language**: TypeScript 5.4.0
- **Plugins**:
  - `eslint-config-next` (next/core-web-vitals, next/typescript)
  - `@typescript-eslint` (v5.62.0 - needs upgrade)
  - `eslint-plugin-jsx-a11y`
  - `eslint-plugin-import`
  - Prettier integration

### Target Configuration
- **ESLint Version**: 9.37.0
- **Config Format**: `eslint.config.mjs` (flat config)
- **All existing functionality preserved**

---

## Breaking Changes in ESLint 9.x

### 1. Node.js Support
- **Dropped Support**: Node.js < v18.18.0, v19.x
- **Required**: Node.js v18.18.0+, v20.9.0+, or v21+
- **Action**: Verify Node.js version with `node --version`

### 2. Configuration System
- **Default Format**: Flat config (`eslint.config.js`) is now default
- **Legacy Format**: `.eslintrc.*` files are deprecated
- **Migration Required**: Must migrate to flat config or set `ESLINT_USE_FLAT_CONFIG=false` (temporary fallback)

### 3. Removed Features

#### Removed Rules
- `require-jsdoc` (deprecated since 2018)
- `valid-jsdoc` (deprecated since 2018)

#### Removed CLI Flags
- `--rulesdir` - Custom rules must be loaded programmatically
- `--ext` - File extensions now specified in config via `files` pattern
- `--resolve-plugins-relative-to` - Plugins resolved from config file location

#### Removed Formatters
Several built-in formatters removed. Install separately if needed:
- `compact`
- `unix`
- `visualstudio`
- `table`

### 4. Behavior Changes

#### `--quiet` Flag
- **Old Behavior**: Runs "warn" rules but hides warnings from output
- **New Behavior**: Does NOT execute rules set to "warn"
- **Impact**: Can improve performance but may miss warnings

#### `eslint-env` Comments
- **Status**: No longer supported in flat config
- **Alternative**: Configure `languageOptions.globals` in config file

#### `eslint:recommended` and `eslint:all`
- **Old**: String references like `"extends": ["eslint:recommended"]`
- **New**: Import from `@eslint/js` and spread configs

### 5. API Changes (for custom rules/plugins)

- `context.getScope()` → `sourceCode.getScope()`
- `context.getAncestors()` → `sourceCode.getAncestors()`
- `context.markVariableAsUsed()` → `sourceCode.markVariableAsUsed()`
- Function-style rules no longer supported (must be objects)

---

## Flat Config Philosophy

### Key Concepts

#### 1. Array-Based Configuration
Flat config uses an array of configuration objects instead of a single object with cascading properties:

```javascript
// Old (.eslintrc.json)
{
  "extends": ["plugin:@typescript-eslint/recommended"],
  "rules": { /* ... */ }
}

// New (eslint.config.mjs)
export default [
  tseslint.configs.recommended,
  {
    rules: { /* ... */ }
  }
];
```

#### 2. JavaScript-First
- Use ES modules (`import`/`export`) or CommonJS (`require`/`module.exports`)
- Direct JavaScript imports for plugins and parsers
- No more string-based plugin references

#### 3. Explicit Over Implicit
- All plugins/parsers imported explicitly
- No automatic file extension detection
- No environment presets (use `globals` package)

#### 4. Cascading and Specificity
- Configs are applied in order (later configs override earlier ones)
- Use `files` patterns for targeted configuration
- More granular control over rule application

---

## Migration Prerequisites

### 1. Package Updates Required

```bash
# Core ESLint
npm install eslint@^9.37.0 --save-dev

# TypeScript ESLint (unified package)
npm install typescript-eslint --save-dev
npm uninstall @typescript-eslint/parser @typescript-eslint/eslint-plugin

# ESLint core utilities
npm install @eslint/js globals --save-dev

# Compatibility layer (for Next.js config)
npm install @eslint/eslintrc @eslint/compat --save-dev

# Update Next.js ESLint config (if needed)
npm install eslint-config-next@latest --save-dev

# Update other plugins
npm install eslint-plugin-jsx-a11y@latest --save-dev
npm install eslint-plugin-import@latest --save-dev
# OR consider import-x for better ESLint 9 support:
# npm install eslint-plugin-import-x --save-dev
```

### 2. Verify Node.js Version

```bash
node --version  # Should be v18.18.0 or higher
```

### 3. Backup Current Configuration

```bash
cp frontend/.eslintrc.json frontend/.eslintrc.json.backup
cp frontend/.eslintrc.enhanced.json frontend/.eslintrc.enhanced.json.backup
```

---

## Step-by-Step Migration

### Step 1: Install Dependencies

```bash
cd frontend

# Core updates
npm install eslint@^9.37.0 --save-dev
npm install typescript-eslint --save-dev
npm install @eslint/js globals --save-dev
npm install @eslint/eslintrc @eslint/compat --save-dev

# Remove old TypeScript ESLint packages
npm uninstall @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Update plugins
npm install eslint-config-next@latest eslint-plugin-jsx-a11y@latest eslint-plugin-import@latest --save-dev
```

### Step 2: Create `eslint.config.mjs`

Create a new file `frontend/eslint.config.mjs` (see [Configuration Examples](#configuration-examples) below)

### Step 3: Test the New Configuration

```bash
# Run ESLint with new config
npx eslint . --config eslint.config.mjs

# Check specific files
npx eslint src/components/ExerciseCard.tsx --config eslint.config.mjs
```

### Step 4: Update package.json Scripts

```json
{
  "scripts": {
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "lint:debug": "eslint . --debug"
  }
}
```

Note: `next lint` will automatically detect and use `eslint.config.mjs` in Next.js 15+. For Next.js 14, you may need to upgrade or use the ESLint CLI directly.

### Step 5: Remove Old Configuration Files

```bash
# After verifying the new config works
rm frontend/.eslintrc.json
rm frontend/.eslintrc.enhanced.json  # If using enhanced version
```

### Step 6: Update CI/CD

Ensure your CI/CD pipeline uses the correct Node.js version (v18.18.0+).

```yaml
# Example .github/workflows/lint.yml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20.x'  # Updated from v16/v18
      - run: npm ci
      - run: npm run lint
```

---

## Configuration Examples

### Basic Configuration (Equivalent to `.eslintrc.json`)

**File**: `frontend/eslint.config.mjs`

```javascript
import { FlatCompat } from '@eslint/eslintrc';
import js from '@eslint/js';
import { fileURLToPath } from 'url';
import path from 'path';

// Mimic __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize FlatCompat for backward compatibility
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
});

export default [
  // Use Next.js config via FlatCompat
  ...compat.config({
    extends: ['next/core-web-vitals', 'next/typescript'],
  }),

  // Custom rules
  {
    rules: {
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      'prefer-const': 'warn',
    },
  },
];
```

### Enhanced Configuration (Equivalent to `.eslintrc.enhanced.json`)

**File**: `frontend/eslint.config.mjs`

```javascript
import { FlatCompat } from '@eslint/eslintrc';
import { fixupConfigRules } from '@eslint/compat';
import js from '@eslint/js';
import globals from 'globals';
import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import importPlugin from 'eslint-plugin-import';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
});

export default defineConfig([
  // Ignore patterns (equivalent to .eslintignore)
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

  // Base ESLint recommended
  js.configs.recommended,

  // TypeScript configuration
  ...tseslint.configs.recommended,

  // Next.js configuration via FlatCompat
  ...fixupConfigRules(
    compat.config({
      extends: ['next/core-web-vitals', 'next/typescript'],
    })
  ),

  // JSX A11y configuration
  jsxA11y.flatConfigs.recommended,

  // Main configuration
  {
    files: ['**/*.{js,mjs,cjs,jsx,ts,tsx}'],

    plugins: {
      '@typescript-eslint': tseslint.plugin,
      'jsx-a11y': jsxA11y,
      import: importPlugin,
    },

    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true,
        },
        project: './tsconfig.json',
        tsconfigRootDir: __dirname,
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2021,
      },
    },

    settings: {
      react: {
        version: 'detect',
      },
      'import/resolver': {
        typescript: {
          alwaysTryTypes: true,
          project: './tsconfig.json',
        },
        node: {
          extensions: ['.js', '.jsx', '.ts', '.tsx'],
        },
      },
    },

    rules: {
      // TypeScript
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/consistent-type-imports': [
        'error',
        {
          prefer: 'type-imports',
          fixStyle: 'inline-type-imports',
        },
      ],

      // React
      'react/jsx-no-target-blank': 'error',
      'react/jsx-key': 'error',
      'react/no-array-index-key': 'warn',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // Accessibility (WCAG 2.1 AA)
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/anchor-has-content': 'error',
      'jsx-a11y/anchor-is-valid': 'error',
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/aria-proptypes': 'error',
      'jsx-a11y/aria-role': 'error',
      'jsx-a11y/aria-unsupported-elements': 'error',
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/heading-has-content': 'error',
      'jsx-a11y/html-has-lang': 'error',
      'jsx-a11y/img-redundant-alt': 'error',
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
      'jsx-a11y/media-has-caption': 'warn',
      'jsx-a11y/mouse-events-have-key-events': 'error',
      'jsx-a11y/no-access-key': 'error',
      'jsx-a11y/no-autofocus': 'warn',
      'jsx-a11y/no-distracting-elements': 'error',
      'jsx-a11y/no-interactive-element-to-noninteractive-role': 'error',
      'jsx-a11y/no-noninteractive-element-interactions': 'error',
      'jsx-a11y/no-noninteractive-element-to-interactive-role': 'error',
      'jsx-a11y/no-redundant-roles': 'error',
      'jsx-a11y/no-static-element-interactions': 'warn',
      'jsx-a11y/role-has-required-aria-props': 'error',
      'jsx-a11y/role-supports-aria-props': 'error',
      'jsx-a11y/scope': 'error',
      'jsx-a11y/tabindex-no-positive': 'error',

      // Import
      'import/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
            'object',
            'type',
          ],
          pathGroups: [
            {
              pattern: 'react',
              group: 'builtin',
              position: 'before',
            },
            {
              pattern: 'next/**',
              group: 'builtin',
              position: 'before',
            },
            {
              pattern: '@/**',
              group: 'internal',
              position: 'after',
            },
          ],
          pathGroupsExcludedImportTypes: ['react', 'next'],
          'newlines-between': 'always',
          alphabetize: {
            order: 'asc',
            caseInsensitive: true,
          },
        },
      ],
      'import/no-duplicates': 'error',
      'import/no-unresolved': 'error',
      'import/named': 'error',

      // Best Practices
      'prefer-const': 'error',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-debugger': 'warn',
      'no-unused-expressions': 'error',
      'no-var': 'error',
      eqeqeq: ['error', 'always'],
      curly: ['error', 'all'],
    },
  },

  // Test files override
  {
    files: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}'],

    languageOptions: {
      globals: {
        ...globals.jest,
      },
    },

    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
]);
```

### Alternative: Pure Flat Config (Without FlatCompat)

If Next.js config is not strictly required or you want a cleaner approach:

```javascript
import js from '@eslint/js';
import globals from 'globals';
import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default defineConfig([
  js.configs.recommended,
  ...tseslint.configs.recommended,
  jsxA11y.flatConfigs.recommended,

  {
    files: ['**/*.{js,jsx,mjs,cjs,ts,tsx}'],

    plugins: {
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
    },

    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        project: './tsconfig.json',
      },
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
    },

    settings: {
      react: { version: 'detect' },
    },

    rules: {
      // Your custom rules
      ...reactPlugin.configs.recommended.rules,
      ...reactHooksPlugin.configs.recommended.rules,
    },
  },
]);
```

---

## Plugin-Specific Migration

### 1. Next.js (`eslint-config-next`)

**Status**: Requires FlatCompat for ESLint 9 compatibility (as of Next.js 14.2)

**Reason**: Next.js ESLint plugins were designed for eslintrc format and don't yet export flat configs natively.

**Solution**:

```javascript
import { FlatCompat } from '@eslint/eslintrc';
import { fixupConfigRules } from '@eslint/compat';

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
});

export default [
  ...fixupConfigRules(
    compat.config({
      extends: ['next/core-web-vitals', 'next/typescript'],
    })
  ),
];
```

**Note**: Next.js 15.3.0+ has native ESLint 9 support. Consider upgrading if possible.

### 2. TypeScript ESLint (`typescript-eslint`)

**Status**: Full flat config support via unified package

**Migration**:

```bash
# Old packages (remove)
npm uninstall @typescript-eslint/parser @typescript-eslint/eslint-plugin

# New unified package
npm install typescript-eslint --save-dev
```

**Usage**:

```javascript
import tseslint from 'typescript-eslint';
import { defineConfig } from 'eslint/config';

export default defineConfig([
  ...tseslint.configs.recommended,
  // or ...tseslint.configs.strict
  // or ...tseslint.configs.stylistic

  {
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
]);
```

**Important**: The utility function `tseslint.config()` has been deprecated in favor of ESLint's `defineConfig()`.

### 3. JSX A11y (`eslint-plugin-jsx-a11y`)

**Status**: Native flat config support via `flatConfigs.recommended`

**Usage**:

```javascript
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  jsxA11y.flatConfigs.recommended,

  {
    plugins: {
      'jsx-a11y': jsxA11y,
    },

    rules: {
      // Override specific rules if needed
      'jsx-a11y/media-has-caption': 'warn',
    },
  },
];
```

**Important**: You must configure `files` and `languageOptions.globals` yourself, as the plugin doesn't provide these.

### 4. Import Plugin (`eslint-plugin-import`)

**Status**: Limited flat config support; consider `eslint-plugin-import-x`

**Option A: Use `eslint-plugin-import`** (May require compatibility fixes)

```javascript
import importPlugin from 'eslint-plugin-import';
import { fixupPluginRules } from '@eslint/compat';

export default [
  {
    plugins: {
      import: fixupPluginRules(importPlugin),
    },

    settings: {
      'import/resolver': {
        typescript: {
          project: './tsconfig.json',
        },
        node: {
          extensions: ['.js', '.jsx', '.ts', '.tsx'],
        },
      },
    },

    rules: {
      'import/order': ['error', { /* ... */ }],
      'import/no-duplicates': 'error',
    },
  },
];
```

**Option B: Use `eslint-plugin-import-x`** (Recommended - better ESLint 9 support)

```bash
npm install eslint-plugin-import-x --save-dev
```

```javascript
import importX from 'eslint-plugin-import-x';

export default [
  importX.flatConfigs.recommended,

  {
    rules: {
      'import-x/order': ['error', { /* ... */ }],
    },
  },
];
```

### 5. Prettier Integration

**Status**: Works via `eslint-config-prettier`

**Usage**:

```bash
npm install eslint-config-prettier --save-dev
```

```javascript
import prettier from 'eslint-config-prettier';

export default [
  // ... other configs ...
  prettier, // Must be last to override other formatting rules
];
```

---

## Testing and Validation

### 1. Automated Migration Tool

ESLint provides a migration utility:

```bash
npx @eslint/migrate-config .eslintrc.json
```

**Output**: Generates `eslint.config.mjs` automatically

**Note**: The output will need manual adjustments for Next.js and plugin compatibility.

### 2. Manual Testing Steps

```bash
# 1. Lint all files
npx eslint .

# 2. Lint with auto-fix
npx eslint . --fix

# 3. Lint specific directories
npx eslint src/
npx eslint src/components/

# 4. Lint specific file types
npx eslint "**/*.{ts,tsx}"

# 5. Debug mode (see rule applications)
npx eslint . --debug

# 6. Check specific rules
npx eslint . --rule '@typescript-eslint/no-unused-vars: error'
```

### 3. Comparison Testing

```bash
# Before migration (old config)
npx eslint . --config .eslintrc.json --format json > old-results.json

# After migration (new config)
npx eslint . --config eslint.config.mjs --format json > new-results.json

# Compare results
diff old-results.json new-results.json
```

### 4. IDE Integration

**VS Code**:

1. Install/update ESLint extension
2. Reload window: `Ctrl+Shift+P` → "Reload Window"
3. Check ESLint output panel for errors
4. Verify flat config detection: Output should show "Using flat config"

**Settings** (`.vscode/settings.json`):

```json
{
  "eslint.experimental.useFlatConfig": true,
  "eslint.format.enable": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### 5. CI/CD Validation

```bash
# In your CI pipeline
npm ci
npm run lint
npm run type-check

# Exit code should be 0 for passing
echo $?
```

### 6. Performance Testing

```bash
# Time the linting process
time npx eslint .

# Compare before and after migration
```

---

## Compatibility Issues

### Issue 1: Next.js Plugin Not Detecting Flat Config

**Symptom**: "The Next.js plugin was not detected in your ESLint configuration"

**Cause**: Next.js 14.x doesn't fully support flat config natively

**Solutions**:

1. **Use FlatCompat** (recommended for Next.js 14.x):
   ```javascript
   import { FlatCompat } from '@eslint/eslintrc';
   const compat = new FlatCompat({ baseDirectory: import.meta.dirname });
   export default [...compat.config({ extends: ['next/core-web-vitals'] })];
   ```

2. **Upgrade to Next.js 15.3.0+** (native ESLint 9 support):
   ```bash
   npm install next@latest
   ```

3. **Temporary fallback** (not recommended):
   ```bash
   ESLINT_USE_FLAT_CONFIG=false npx eslint .
   ```

### Issue 2: `context.getScope is not a function`

**Symptom**: Plugin throws errors about missing `context` methods

**Cause**: Plugin not updated for ESLint 9 rule API

**Solution**: Use `fixupPluginRules` from `@eslint/compat`:

```javascript
import { fixupPluginRules } from '@eslint/compat';
import somePlugin from 'eslint-plugin-some-plugin';

export default [
  {
    plugins: {
      'some-plugin': fixupPluginRules(somePlugin),
    },
  },
];
```

### Issue 3: Import Plugin Resolution Errors

**Symptom**: `import/no-unresolved` fails to resolve TypeScript paths

**Cause**: Import plugin may not fully support flat config resolver settings

**Solutions**:

1. **Use compatibility fix**:
   ```javascript
   import { fixupPluginRules } from '@eslint/compat';
   import importPlugin from 'eslint-plugin-import';

   export default [{
     plugins: {
       import: fixupPluginRules(importPlugin),
     },
   }];
   ```

2. **Switch to `eslint-plugin-import-x`**:
   ```bash
   npm uninstall eslint-plugin-import
   npm install eslint-plugin-import-x --save-dev
   ```

3. **Disable problematic rules temporarily**:
   ```javascript
   rules: {
     'import/no-unresolved': 'off', // Re-enable after fixing
   }
   ```

### Issue 4: TypeScript Parser Not Finding `tsconfig.json`

**Symptom**: "Parsing error: Cannot find tsconfig.json"

**Cause**: Incorrect `parserOptions.project` path in flat config

**Solution**:

```javascript
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default [
  {
    languageOptions: {
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: __dirname, // Critical!
      },
    },
  },
];
```

### Issue 5: Prettier Conflicts

**Symptom**: Formatting rules conflict with Prettier

**Cause**: Prettier config not applied last in flat config array

**Solution**:

```javascript
import prettier from 'eslint-config-prettier';

export default [
  // All other configs...
  prettier, // MUST be last!
];
```

### Issue 6: Ignores Not Working

**Symptom**: ESLint linting files that should be ignored

**Cause**: Flat config requires explicit `ignores` pattern (no automatic `.eslintignore` loading)

**Solution**:

```javascript
export default [
  {
    ignores: [
      '**/node_modules/**',
      '**/.next/**',
      '**/out/**',
      '**/build/**',
      '**/dist/**',
      '**/coverage/**',
    ],
  },
  // Other configs...
];
```

**Note**: Patterns starting with `/` are treated as absolute paths. Use `**/` for glob patterns.

### Issue 7: Cache Errors

**Symptom**: "Could not serialize parser object (missing 'meta' object)"

**Cause**: ESLint cache incompatible with flat config in some scenarios

**Solution**:

```bash
# Clear cache
rm -rf node_modules/.cache/eslint

# Disable cache temporarily
npx eslint . --no-cache

# Or update cache strategy
npx eslint . --cache-strategy content
```

---

## Rollback Plan

If migration causes critical issues, follow this rollback procedure:

### 1. Restore Original Configuration

```bash
# Restore backup
cp frontend/.eslintrc.json.backup frontend/.eslintrc.json
cp frontend/.eslintrc.enhanced.json.backup frontend/.eslintrc.enhanced.json

# Remove flat config
rm frontend/eslint.config.mjs
```

### 2. Downgrade Packages

```bash
# Restore ESLint 8.x
npm install eslint@8.57.1 --save-dev

# Restore old TypeScript ESLint
npm uninstall typescript-eslint
npm install @typescript-eslint/parser@5.62.0 @typescript-eslint/eslint-plugin@5.62.0 --save-dev

# Remove flat config dependencies
npm uninstall @eslint/eslintrc @eslint/compat @eslint/js globals
```

### 3. Verify Rollback

```bash
# Test linting
npx eslint .

# Verify package versions
npm list eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### 4. Update CI/CD (if changed)

Revert any CI/CD changes to use older Node.js versions if necessary.

---

## Recommended Migration Order

### Phase 1: Preparation (Low Risk)
1. Review this guide and breaking changes
2. Backup current configuration files
3. Verify Node.js version compatibility
4. Test current ESLint setup (baseline)

### Phase 2: Dependency Updates (Medium Risk)
1. Update ESLint to 9.37.0
2. Install compatibility packages (`@eslint/eslintrc`, `@eslint/compat`)
3. Install `typescript-eslint` unified package
4. Update plugin versions
5. Test with old config (should still work)

### Phase 3: Configuration Migration (High Risk)
1. Run automated migration tool: `npx @eslint/migrate-config`
2. Create `eslint.config.mjs` manually (start with basic example)
3. Test with new config on single file
4. Gradually add plugins and rules
5. Fix compatibility issues one by one

### Phase 4: Validation (Medium Risk)
1. Run full lint across codebase
2. Compare results with old config
3. Test IDE integration
4. Update CI/CD configuration
5. Get team feedback

### Phase 5: Finalization (Low Risk)
1. Remove old `.eslintrc.*` files
2. Update documentation
3. Remove old TypeScript ESLint packages
4. Clean up package.json
5. Commit changes

---

## Additional Resources

### Official Documentation
- [ESLint Flat Config Migration Guide](https://eslint.org/docs/latest/use/configure/migration-guide)
- [ESLint 9.x Migration Guide](https://eslint.org/docs/latest/use/migrate-to-9.0.0)
- [Flat Config Overview](https://eslint.org/docs/latest/use/configure/configuration-files)
- [TypeScript ESLint Flat Config](https://typescript-eslint.io/packages/typescript-eslint/)
- [Next.js ESLint Config](https://nextjs.org/docs/app/api-reference/config/eslint)

### Tools
- [ESLint Config Migrator](https://github.com/eslint/config-migrator): `npx @eslint/migrate-config`
- [ESLint Config Inspector](https://github.com/eslint/config-inspector): Visual tool for flat configs
- [Compatibility Utilities](https://github.com/eslint/compat): `@eslint/compat` and `@eslint/eslintrc`

### Community Resources
- [ESLint Discussions](https://github.com/eslint/eslint/discussions)
- [Next.js ESLint 9 Discussion](https://github.com/vercel/next.js/discussions/54238)
- [TypeScript ESLint GitHub](https://github.com/typescript-eslint/typescript-eslint)

---

## Conclusion

Migrating to ESLint 9 flat config requires careful planning and testing, but offers benefits:
- **Clearer Configuration**: JavaScript-based config with explicit imports
- **Better Performance**: More efficient rule application
- **Future-Proof**: Official format going forward
- **Improved Tooling**: Better IDE integration and debugging

For Next.js 14.2 projects, using the FlatCompat approach provides the smoothest migration path while maintaining all existing functionality.

---

**Last Updated**: 2025-10-06
**ESLint Version**: 9.37.0
**Next.js Version**: 14.2.0
**Project**: Subjunctive Practice Application
