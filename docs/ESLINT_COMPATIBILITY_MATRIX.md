# ESLint 9.x Compatibility Matrix

## Overview

This document provides a detailed compatibility matrix for migrating our Next.js TypeScript project to ESLint 9.x with flat config.

---

## Plugin Compatibility Status

| Plugin | Current Version | ESLint 9 Status | Flat Config Support | Required Action | Priority |
|--------|----------------|-----------------|---------------------|-----------------|----------|
| **eslint-config-next** | 14.2.33 | ⚠️ Partial | Via FlatCompat | Use FlatCompat wrapper | HIGH |
| **@typescript-eslint** | 5.62.0 (old) | ❌ Replace | ✅ Native (v8+) | Migrate to `typescript-eslint` | HIGH |
| **eslint-plugin-jsx-a11y** | Latest | ✅ Compatible | ✅ Native | Use `flatConfigs.recommended` | MEDIUM |
| **eslint-plugin-import** | Latest | ⚠️ Limited | Via fixup | Use `fixupPluginRules` OR switch to `import-x` | MEDIUM |
| **eslint-plugin-import-x** | N/A | ✅ Compatible | ✅ Native | Install as replacement | MEDIUM |
| **eslint-config-prettier** | Latest | ✅ Compatible | ✅ Native | No changes needed | LOW |

**Legend**:
- ✅ Full compatibility
- ⚠️ Partial compatibility (workaround needed)
- ❌ Not compatible (replacement needed)

---

## Detailed Plugin Compatibility

### 1. ESLint Config Next (`eslint-config-next`)

#### Status
⚠️ **Partial Support** - Requires FlatCompat

#### Compatibility Details

| Feature | ESLint 8 | ESLint 9 (Next.js 14.2) | ESLint 9 (Next.js 15.3+) |
|---------|----------|-------------------------|--------------------------|
| Legacy config | ✅ Native | ✅ Via ESLINT_USE_FLAT_CONFIG=false | ✅ Native |
| Flat config | ❌ Not supported | ⚠️ Via FlatCompat | ✅ Native |
| next/core-web-vitals | ✅ Works | ⚠️ Needs wrapper | ✅ Works |
| next/typescript | ✅ Works | ⚠️ Needs wrapper | ✅ Works |

#### Migration Path

**Current (Next.js 14.2)**:
```javascript
// Must use FlatCompat
import { FlatCompat } from '@eslint/eslintrc';
import { fixupConfigRules } from '@eslint/compat';

const compat = new FlatCompat({ baseDirectory: import.meta.dirname });

export default [
  ...fixupConfigRules(
    compat.config({
      extends: ['next/core-web-vitals', 'next/typescript'],
    })
  ),
];
```

**Future (Next.js 15.3+)**:
```javascript
// Native flat config support
import nextConfig from 'eslint-config-next/flat';

export default [
  nextConfig,
];
```

#### Known Issues
1. Warning: "The Next.js plugin was not detected" - Resolved by using `fixupConfigRules`
2. Cache serialization errors - Resolved by disabling cache or using `--cache-strategy content`

#### Required Packages
```json
{
  "devDependencies": {
    "eslint-config-next": "^14.2.0",
    "@eslint/eslintrc": "^3.0.0",
    "@eslint/compat": "^1.0.0"
  }
}
```

---

### 2. TypeScript ESLint (`@typescript-eslint` → `typescript-eslint`)

#### Status
✅ **Full Support** - Via unified package

#### Compatibility Details

| Package | ESLint 8 | ESLint 9 | Flat Config | Status |
|---------|----------|----------|-------------|--------|
| `@typescript-eslint/parser` (old) | ✅ | ⚠️ | ❌ | Deprecated |
| `@typescript-eslint/eslint-plugin` (old) | ✅ | ⚠️ | ❌ | Deprecated |
| `typescript-eslint` (unified) | ✅ | ✅ | ✅ | Recommended |

#### Migration Path

**Old (ESLint 8)**:
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  extends: ['plugin:@typescript-eslint/recommended'],
};
```

**New (ESLint 9)**:
```javascript
import tseslint from 'typescript-eslint';
import { defineConfig } from 'eslint/config';

export default defineConfig([
  ...tseslint.configs.recommended,
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

#### Available Configs
- `tseslint.configs.recommended` - Basic TypeScript rules
- `tseslint.configs.strict` - Stricter ruleset
- `tseslint.configs.stylistic` - Code style rules

#### Type-Aware Linting
Requires `parserOptions.project` to be set:

```javascript
languageOptions: {
  parserOptions: {
    project: true, // Auto-detect
    // OR
    project: './tsconfig.json',
    tsconfigRootDir: import.meta.dirname,
  },
}
```

#### Performance Notes
- Type-aware rules are slower (requires TypeScript compilation)
- Use `project: true` for automatic tsconfig detection
- Consider disabling type-aware rules for large codebases if performance is an issue

#### Required Packages
```json
{
  "devDependencies": {
    "typescript-eslint": "^8.0.0",
    "typescript": "^5.4.0"
  }
}
```

---

### 3. JSX A11y (`eslint-plugin-jsx-a11y`)

#### Status
✅ **Full Support** - Native flat config

#### Compatibility Details

| Feature | ESLint 8 | ESLint 9 | Notes |
|---------|----------|----------|-------|
| Plugin loading | ✅ | ✅ | Direct import |
| Flat config preset | ❌ | ✅ | `flatConfigs.recommended` |
| All a11y rules | ✅ | ✅ | No changes |
| Custom configs | ✅ | ✅ | Standard format |

#### Migration Path

**Old (ESLint 8)**:
```javascript
module.exports = {
  extends: ['plugin:jsx-a11y/recommended'],
};
```

**New (ESLint 9)**:
```javascript
import jsxA11y from 'eslint-plugin-jsx-a11y';
import globals from 'globals';

export default [
  jsxA11y.flatConfigs.recommended,
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
  },
];
```

#### Important Notes
- Plugin does NOT configure `files` or `languageOptions.globals`
- Must manually configure file patterns and browser globals
- All 40+ accessibility rules work unchanged

#### Available Presets
- `jsxA11y.flatConfigs.recommended` - WCAG 2.1 AA rules
- `jsxA11y.flatConfigs.strict` - Stricter accessibility rules

#### Required Packages
```json
{
  "devDependencies": {
    "eslint-plugin-jsx-a11y": "^6.10.0",
    "globals": "^15.0.0"
  }
}
```

---

### 4. Import Plugin (`eslint-plugin-import` vs `eslint-plugin-import-x`)

#### Status
⚠️ **Limited Support** (import) / ✅ **Full Support** (import-x)

#### Compatibility Comparison

| Feature | `eslint-plugin-import` | `eslint-plugin-import-x` |
|---------|------------------------|--------------------------|
| ESLint 9 support | ⚠️ Via fixup | ✅ Native |
| Flat config | ⚠️ Limited | ✅ Full |
| TypeScript resolver | ⚠️ May need fixes | ✅ Works |
| Maintenance | Slow updates | Active |
| Migration effort | Medium | Low |

#### Option A: Keep Original Plugin (with fixes)

**Requires**:
- `@eslint/compat` for `fixupPluginRules`
- Additional configuration

```javascript
import { fixupPluginRules } from '@eslint/compat';
import importPlugin from 'eslint-plugin-import';

export default [{
  plugins: {
    import: fixupPluginRules(importPlugin),
  },
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
    },
  },
  rules: {
    'import/order': ['error', { /* config */ }],
  },
}];
```

#### Option B: Switch to `eslint-plugin-import-x` (Recommended)

**Benefits**:
- Native ESLint 9 and flat config support
- Active maintenance
- Better TypeScript integration
- Drop-in replacement

```javascript
import importX from 'eslint-plugin-import-x';

export default [
  importX.flatConfigs.recommended,
  {
    rules: {
      'import-x/order': ['error', {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
        'newlines-between': 'always',
        alphabetize: { order: 'asc', caseInsensitive: true },
      }],
    },
  },
];
```

**Note**: Rule names change from `import/*` to `import-x/*`

#### Migration Steps (import → import-x)

```bash
# 1. Uninstall old plugin
npm uninstall eslint-plugin-import

# 2. Install new plugin
npm install eslint-plugin-import-x --save-dev

# 3. Update config (change rule names)
# import/order → import-x/order
# import/no-duplicates → import-x/no-duplicates
```

#### Required Packages

**Option A** (keep original):
```json
{
  "devDependencies": {
    "eslint-plugin-import": "^2.31.0",
    "@eslint/compat": "^1.0.0"
  }
}
```

**Option B** (recommended):
```json
{
  "devDependencies": {
    "eslint-plugin-import-x": "^4.0.0"
  }
}
```

---

### 5. Prettier Integration (`eslint-config-prettier`)

#### Status
✅ **Full Support** - Works out of the box

#### Compatibility Details

| Feature | ESLint 8 | ESLint 9 | Notes |
|---------|----------|----------|-------|
| Disables formatting rules | ✅ | ✅ | No changes |
| Works with plugins | ✅ | ✅ | Must be last |
| Flat config support | ✅ | ✅ | Direct import |

#### Migration Path

**Old (ESLint 8)**:
```javascript
module.exports = {
  extends: ['prettier'],
};
```

**New (ESLint 9)**:
```javascript
import prettier from 'eslint-config-prettier';

export default [
  // ... all other configs ...
  prettier, // MUST BE LAST
];
```

#### Critical Rule
Prettier config **MUST be the last item** in the config array to properly override formatting rules from other configs.

#### Required Packages
```json
{
  "devDependencies": {
    "eslint-config-prettier": "^9.1.0",
    "prettier": "^3.2.0"
  }
}
```

---

## ESLint Core Features Compatibility

### Configuration Options

| Feature | ESLint 8 | ESLint 9 Flat Config | Migration Notes |
|---------|----------|----------------------|-----------------|
| `extends` | ✅ String array | ❌ Use spread | Spread imported configs |
| `plugins` | ✅ String array | ✅ Object map | Import and map plugins |
| `env` | ✅ Preset globals | ❌ Use `globals` | Install `globals` package |
| `parser` | ✅ String | ✅ Object | Import parser module |
| `parserOptions` | ✅ | ✅ | Moved to `languageOptions` |
| `overrides` | ✅ Array | ❌ Use cascading | Use multiple config objects |
| `ignores` | Via `.eslintignore` | ✅ In config | Add `ignores` array |
| `settings` | ✅ | ✅ | No changes |
| `rules` | ✅ | ✅ | No changes |

### CLI Flags

| Flag | ESLint 8 | ESLint 9 | Replacement |
|------|----------|----------|-------------|
| `--ext` | ✅ | ❌ | Use `files` in config |
| `--rulesdir` | ✅ | ❌ | Load rules programmatically |
| `--resolve-plugins-relative-to` | ✅ | ❌ | Plugins resolve from config dir |
| `--quiet` | Hides warnings | Skips warning rules | Behavior change, not breaking |
| `--cache` | ✅ | ✅ | Works, but clear cache on migration |
| `--fix` | ✅ | ✅ | No changes |
| `--format` | ✅ | ✅ | Some formatters removed |

### Removed Formatters

| Formatter | ESLint 8 | ESLint 9 | Alternative |
|-----------|----------|----------|-------------|
| `json` | ✅ | ✅ | Built-in |
| `stylish` | ✅ | ✅ | Built-in (default) |
| `compact` | ✅ | ❌ | Install separately |
| `unix` | ✅ | ❌ | Install separately |
| `visualstudio` | ✅ | ❌ | Install separately |
| `table` | ✅ | ❌ | Install separately |

---

## Framework-Specific Compatibility

### Next.js

| Version | ESLint 8 | ESLint 9 | Flat Config | Recommended Approach |
|---------|----------|----------|-------------|----------------------|
| < 14.0 | ✅ | ⚠️ | ❌ | Upgrade Next.js first |
| 14.0 - 15.2 | ✅ | ⚠️ | Via FlatCompat | Use compatibility layer |
| 15.3+ | ✅ | ✅ | ✅ Native | Direct flat config |

### React

| Feature | ESLint 8 | ESLint 9 | Notes |
|---------|----------|----------|-------|
| React plugin | ✅ | ✅ | No changes |
| React Hooks | ✅ | ✅ | No changes |
| JSX | ✅ | ✅ | No changes |

### TypeScript

| Feature | ESLint 8 | ESLint 9 | Notes |
|---------|----------|----------|-------|
| `.ts` files | ✅ | ✅ | No changes |
| `.tsx` files | ✅ | ✅ | No changes |
| Type checking | ✅ | ✅ | Configure `project` |
| Path aliases | ✅ | ✅ | Configure resolver |

---

## IDE Integration

### Visual Studio Code

| Feature | ESLint 8 | ESLint 9 | Notes |
|---------|----------|----------|-------|
| ESLint extension | ✅ | ✅ | Update to latest |
| Flat config detection | ❌ | ✅ Auto | Detects `eslint.config.*` |
| Inline errors | ✅ | ✅ | No changes |
| Auto-fix on save | ✅ | ✅ | No changes |
| Config file | `.vscode/settings.json` | Same | May need `experimental.useFlatConfig` |

**VS Code Settings**:
```json
{
  "eslint.experimental.useFlatConfig": true,
  "eslint.format.enable": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### Other IDEs

| IDE | ESLint 8 | ESLint 9 | Notes |
|-----|----------|----------|-------|
| WebStorm | ✅ | ✅ | Update to 2024.1+ |
| Sublime Text | ✅ | ✅ | Update ESLint plugin |
| Vim/Neovim | ✅ | ✅ | Update ALE or CoC |

---

## CI/CD Compatibility

### Node.js Versions

| Node Version | ESLint 8 | ESLint 9 | Status |
|--------------|----------|----------|--------|
| v14.x | ✅ | ❌ | EOL |
| v16.x | ✅ | ❌ | EOL |
| v18.0 - v18.17 | ✅ | ❌ | Too old |
| v18.18+ | ✅ | ✅ | Supported |
| v19.x | ✅ | ❌ | Dropped |
| v20.9+ | ✅ | ✅ | Recommended |
| v21+ | ✅ | ✅ | Supported |

### GitHub Actions

**Before** (Node 16):
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '16.x'
```

**After** (Node 20):
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20.x'
```

### Other CI Platforms

All platforms require Node.js v18.18.0+ or v20.9.0+:
- GitLab CI
- CircleCI
- Travis CI
- Azure Pipelines
- Jenkins

---

## Performance Comparison

### Linting Speed

| Metric | ESLint 8 | ESLint 9 | Change |
|--------|----------|----------|--------|
| Startup time | 1.0x | 0.9-1.0x | Similar or faster |
| Lint time | 1.0x | 0.9x | ~10% faster |
| Memory usage | 1.0x | 0.95x | ~5% less |
| Cache performance | Good | Better | Improved algorithm |

### Configuration Parsing

| Aspect | ESLint 8 | ESLint 9 | Improvement |
|--------|----------|----------|-------------|
| Config loading | Cascade + merge | Direct array | Faster |
| Plugin resolution | String lookup | Direct import | Faster |
| Extends resolution | Recursive | Spread | Faster |

---

## Migration Risk Assessment

### Low Risk Changes
- ✅ Updating ESLint version (with flat config)
- ✅ Installing compatibility packages
- ✅ Using FlatCompat for Next.js
- ✅ Updating TypeScript ESLint
- ✅ Prettier integration

### Medium Risk Changes
- ⚠️ Switching import plugin to import-x
- ⚠️ Custom rule adjustments
- ⚠️ IDE configuration updates
- ⚠️ CI/CD Node.js version updates

### High Risk Changes
- ⚠️ Upgrading Next.js (if doing both migrations)
- ⚠️ Custom plugin development
- ⚠️ Complex override patterns

---

## Recommended Migration Timeline

### Week 1: Preparation
- Read documentation
- Backup configurations
- Verify Node.js versions
- Test current setup

### Week 2: Development Environment
- Update local dependencies
- Create flat config
- Test thoroughly
- Fix issues

### Week 3: Team Migration
- Update documentation
- Team training
- Gradual rollout
- Monitor for issues

### Week 4: Production
- Update CI/CD
- Final testing
- Production deployment
- Post-deployment monitoring

---

## Version Matrix

| Package | Current | Target | ESLint 8 | ESLint 9 |
|---------|---------|--------|----------|----------|
| eslint | 8.57.1 | 9.37.0 | ✅ | ✅ |
| typescript-eslint | N/A | latest | ✅ | ✅ |
| @typescript-eslint/parser | 5.62.0 | Remove | ✅ | ⚠️ |
| @typescript-eslint/eslint-plugin | 5.62.0 | Remove | ✅ | ⚠️ |
| eslint-config-next | 14.2.33 | latest | ✅ | ⚠️ |
| eslint-plugin-jsx-a11y | latest | latest | ✅ | ✅ |
| eslint-plugin-import | latest | Remove | ✅ | ⚠️ |
| eslint-plugin-import-x | N/A | latest | ✅ | ✅ |
| eslint-config-prettier | latest | latest | ✅ | ✅ |
| @eslint/js | N/A | latest | N/A | ✅ |
| globals | N/A | latest | N/A | ✅ |
| @eslint/eslintrc | N/A | latest | N/A | ✅ |
| @eslint/compat | N/A | latest | N/A | ✅ |

---

## Conclusion

The migration to ESLint 9 with flat config is **feasible and recommended** for our Next.js TypeScript project. Key considerations:

1. **Use FlatCompat** for Next.js 14.2 compatibility
2. **Migrate to `typescript-eslint`** unified package
3. **Consider `eslint-plugin-import-x`** for better support
4. **Update Node.js** to v20.9.0+ for optimal compatibility
5. **Test thoroughly** before production deployment

The enhanced template provided handles all compatibility issues and provides a smooth migration path.

---

**Last Updated**: 2025-10-06
**Document Version**: 1.0
**For Project**: Subjunctive Practice Application
