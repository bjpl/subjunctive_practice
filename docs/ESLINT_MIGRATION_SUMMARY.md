# ESLint 9.x Migration Summary

## Quick Reference

### Current State
- **ESLint**: 8.57.1
- **Config**: `.eslintrc.json` (legacy format)
- **TypeScript ESLint**: 5.62.0 (outdated, separate packages)
- **Next.js**: 14.2.0
- **Plugins**: jsx-a11y, import, prettier integration

### Target State
- **ESLint**: 9.37.0
- **Config**: `eslint.config.mjs` (flat config)
- **TypeScript ESLint**: Latest unified package (`typescript-eslint`)
- **Next.js**: 14.2.0 (with FlatCompat for compatibility)
- **All plugins**: Updated to latest versions

---

## Critical Breaking Changes

### 1. Node.js Version Requirements
- **Minimum Required**: v18.18.0
- **Recommended**: v20.9.0 or v21+
- **Action**: Check with `node --version`

### 2. Configuration File Format
- **Old**: `.eslintrc.json` / `.eslintrc.js`
- **New**: `eslint.config.js` / `eslint.config.mjs`
- **Key Differences**:
  - Array-based config instead of single object
  - ES modules with explicit imports
  - No more string-based plugin references
  - Manual `ignores` patterns (no automatic `.eslintignore` loading)

### 3. CLI Flag Changes
| Removed Flag | Replacement |
|--------------|-------------|
| `--ext` | Configure `files` patterns in config |
| `--rulesdir` | Load custom rules programmatically |
| `--resolve-plugins-relative-to` | Plugins resolved from config location |

### 4. `--quiet` Behavior Change
- **Old**: Runs "warn" rules but hides output
- **New**: Does NOT execute "warn" rules
- **Impact**: May improve performance but could miss warnings

### 5. Environment Comments
- **Old**: `/* eslint-env browser, node */`
- **New**: Not supported - use `languageOptions.globals` in config

---

## Compatibility Issues by Plugin

### Next.js (`eslint-config-next`)

| Issue | Severity | Solution |
|-------|----------|----------|
| No native flat config support (Next.js 14.2) | HIGH | Use `FlatCompat` from `@eslint/eslintrc` |
| Plugin detection warnings | MEDIUM | Use `fixupConfigRules` from `@eslint/compat` |
| Native support available in Next.js 15.3.0+ | INFO | Consider upgrading Next.js |

**Required Packages**:
```bash
npm install @eslint/eslintrc @eslint/compat --save-dev
```

**Working Pattern**:
```javascript
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

---

### TypeScript ESLint

| Issue | Severity | Solution |
|-------|----------|----------|
| Separate packages deprecated | HIGH | Use unified `typescript-eslint` package |
| `tseslint.config()` deprecated | MEDIUM | Use ESLint's `defineConfig()` instead |
| Old v5.x outdated | HIGH | Upgrade to latest version |

**Package Migration**:
```bash
# Remove old packages
npm uninstall @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Install unified package
npm install typescript-eslint --save-dev
```

**Working Pattern**:
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

---

### JSX A11y

| Issue | Severity | Solution |
|-------|----------|----------|
| Files/globals not auto-configured | LOW | Manually configure `files` and `languageOptions.globals` |
| Need flat config preset | LOW | Use `jsxA11y.flatConfigs.recommended` |

**Working Pattern**:
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

---

### Import Plugin

| Issue | Severity | Solution |
|-------|----------|----------|
| Limited flat config support | MEDIUM | Use `fixupPluginRules` OR switch to `import-x` |
| TypeScript resolver issues | MEDIUM | Ensure correct settings configuration |
| `context.getScope` errors | HIGH | Apply `fixupPluginRules` |

**Option A: Fix Original Plugin**
```javascript
import { fixupPluginRules } from '@eslint/compat';
import importPlugin from 'eslint-plugin-import';

export default [{
  plugins: {
    import: fixupPluginRules(importPlugin),
  },
}];
```

**Option B: Use `import-x` (Recommended)**
```bash
npm uninstall eslint-plugin-import
npm install eslint-plugin-import-x --save-dev
```

```javascript
import importX from 'eslint-plugin-import-x';

export default [
  importX.flatConfigs.recommended,
];
```

---

### Prettier

| Issue | Severity | Solution |
|-------|----------|----------|
| Must be last in config array | LOW | Place `prettier` config at end of array |

**Working Pattern**:
```javascript
import prettier from 'eslint-config-prettier';

export default [
  // All other configs...
  prettier, // MUST BE LAST!
];
```

---

## Package Installation Summary

### Core Dependencies

```bash
# ESLint core
npm install eslint@^9.37.0 --save-dev

# TypeScript ESLint (unified package)
npm install typescript-eslint --save-dev
npm uninstall @typescript-eslint/parser @typescript-eslint/eslint-plugin

# ESLint utilities
npm install @eslint/js globals --save-dev

# Compatibility layer (for Next.js)
npm install @eslint/eslintrc @eslint/compat --save-dev
```

### Plugin Updates

```bash
# Next.js config (update to latest)
npm install eslint-config-next@latest --save-dev

# Accessibility
npm install eslint-plugin-jsx-a11y@latest --save-dev

# Import plugin (choose one)
# Option A: Original with fixes
npm install eslint-plugin-import@latest --save-dev

# Option B: Better ESLint 9 support (recommended)
npm install eslint-plugin-import-x --save-dev

# Prettier integration
npm install eslint-config-prettier --save-dev
```

### Complete Installation Command

```bash
cd frontend

# Install all at once
npm install --save-dev \
  eslint@^9.37.0 \
  typescript-eslint \
  @eslint/js \
  globals \
  @eslint/eslintrc \
  @eslint/compat \
  eslint-config-next@latest \
  eslint-plugin-jsx-a11y@latest \
  eslint-plugin-import-x \
  eslint-config-prettier

# Remove old packages
npm uninstall @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-import
```

---

## Migration Checklist

### Phase 1: Preparation
- [ ] Read `ESLINT_9_MIGRATION_GUIDE.md` thoroughly
- [ ] Verify Node.js version: `node --version` (v18.18.0+)
- [ ] Backup current config files:
  ```bash
  cp frontend/.eslintrc.json frontend/.eslintrc.json.backup
  cp frontend/.eslintrc.enhanced.json frontend/.eslintrc.enhanced.json.backup
  ```
- [ ] Create baseline lint results:
  ```bash
  npx eslint . --format json > eslint-results-before.json
  ```

### Phase 2: Install Dependencies
- [ ] Install ESLint 9.37.0
- [ ] Install `typescript-eslint` unified package
- [ ] Remove old `@typescript-eslint/*` packages
- [ ] Install `@eslint/js`, `globals`
- [ ] Install `@eslint/eslintrc`, `@eslint/compat`
- [ ] Update all plugins to latest versions
- [ ] Verify installations: `npm list eslint typescript-eslint`

### Phase 3: Create Flat Config
- [ ] Choose config template:
  - [ ] Basic template (`eslint.config.basic.template.mjs`)
  - [ ] Enhanced template (`eslint.config.enhanced.template.mjs`)
- [ ] Copy template to `frontend/eslint.config.mjs`
- [ ] Adjust `tsconfig.json` path if needed
- [ ] Adjust ignore patterns for project structure
- [ ] Review and customize rules

### Phase 4: Testing
- [ ] Test on single file:
  ```bash
  npx eslint src/components/ExerciseCard.tsx
  ```
- [ ] Test on component directory:
  ```bash
  npx eslint src/components/
  ```
- [ ] Run full lint:
  ```bash
  npx eslint .
  ```
- [ ] Compare with baseline:
  ```bash
  npx eslint . --format json > eslint-results-after.json
  diff eslint-results-before.json eslint-results-after.json
  ```
- [ ] Test auto-fix:
  ```bash
  npx eslint . --fix
  ```

### Phase 5: IDE Integration
- [ ] Reload VS Code window: `Ctrl+Shift+P` → "Reload Window"
- [ ] Check ESLint extension status
- [ ] Verify flat config detection in output panel
- [ ] Test inline error highlighting
- [ ] Test auto-fix on save

### Phase 6: Resolve Issues
- [ ] Fix plugin compatibility errors (use `fixupPluginRules`)
- [ ] Fix parser errors (check `tsconfigRootDir`)
- [ ] Fix import resolution issues
- [ ] Clear cache if needed: `rm -rf node_modules/.cache/eslint`
- [ ] Document any workarounds needed

### Phase 7: CI/CD Update
- [ ] Update Node.js version in CI (v18.18.0+)
- [ ] Update lint commands if needed
- [ ] Test CI pipeline with new config
- [ ] Update documentation

### Phase 8: Finalization
- [ ] Remove old `.eslintrc.*` files
- [ ] Remove old package backups from `node_modules`
- [ ] Update team documentation
- [ ] Update README.md with new lint commands
- [ ] Create pull request with migration
- [ ] Get team review and approval
- [ ] Merge and monitor for issues

---

## Common Error Messages and Solutions

### Error: "The Next.js plugin was not detected"
**Cause**: Next.js 14.x doesn't support flat config natively

**Solution**: Use FlatCompat wrapper
```javascript
import { FlatCompat } from '@eslint/eslintrc';
const compat = new FlatCompat({ baseDirectory: import.meta.dirname });
export default [...compat.config({ extends: ['next/core-web-vitals'] })];
```

---

### Error: "context.getScope is not a function"
**Cause**: Plugin not updated for ESLint 9 API

**Solution**: Use compatibility fix
```javascript
import { fixupPluginRules } from '@eslint/compat';
plugins: { 'plugin-name': fixupPluginRules(pluginName) }
```

---

### Error: "Cannot find tsconfig.json"
**Cause**: Incorrect `tsconfigRootDir` in parser options

**Solution**: Set correct root directory
```javascript
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));

languageOptions: {
  parserOptions: {
    project: './tsconfig.json',
    tsconfigRootDir: __dirname,
  },
}
```

---

### Error: "Could not serialize parser object"
**Cause**: Cache incompatibility

**Solution**: Clear cache and disable temporarily
```bash
rm -rf node_modules/.cache/eslint
npx eslint . --no-cache
```

---

### Error: Files being linted that should be ignored
**Cause**: `.eslintignore` not automatically loaded in flat config

**Solution**: Add explicit `ignores` pattern
```javascript
export default [
  {
    ignores: ['**/node_modules/**', '**/.next/**', '**/build/**'],
  },
  // Other configs...
];
```

---

## Performance Comparison

After migration, expect:
- **Startup Time**: Similar or slightly faster
- **Lint Time**: 10-20% faster (due to `--quiet` changes)
- **Memory Usage**: Similar or slightly lower
- **Cache Performance**: Better with `--cache-strategy content`

Test before and after:
```bash
# Before
time npx eslint .

# After
time npx eslint .
```

---

## Rollback Procedure

If critical issues arise:

1. **Restore config files**:
   ```bash
   cp frontend/.eslintrc.json.backup frontend/.eslintrc.json
   rm frontend/eslint.config.mjs
   ```

2. **Downgrade packages**:
   ```bash
   npm install eslint@8.57.1 --save-dev
   npm uninstall typescript-eslint
   npm install @typescript-eslint/parser@5.62.0 @typescript-eslint/eslint-plugin@5.62.0 --save-dev
   npm uninstall @eslint/eslintrc @eslint/compat @eslint/js globals
   ```

3. **Verify rollback**:
   ```bash
   npx eslint .
   npm list eslint
   ```

---

## Recommended Approach

For our Next.js 14.2 TypeScript project, use the **Enhanced Template** with FlatCompat:

**Why?**
- Maintains all current functionality
- Preserves accessibility rules (WCAG 2.1 AA)
- Keeps import ordering
- Works with current Next.js version
- Easy to upgrade when Next.js 15+ adds native support

**Steps**:
1. Copy `docs/eslint.config.enhanced.template.mjs` to `frontend/eslint.config.mjs`
2. Install all dependencies (see command above)
3. Test thoroughly
4. Remove old config files

---

## Resources

- Full guide: `docs/ESLINT_9_MIGRATION_GUIDE.md`
- Basic template: `docs/eslint.config.basic.template.mjs`
- Enhanced template: `docs/eslint.config.enhanced.template.mjs`
- Official ESLint docs: https://eslint.org/docs/latest/use/configure/migration-guide

---

**Created**: 2025-10-06
**For**: Subjunctive Practice Application Frontend
**ESLint**: 8.57.1 → 9.37.0
**Status**: Ready for migration
