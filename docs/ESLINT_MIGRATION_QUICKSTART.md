# ESLint 9.x Migration Quick Start

## TL;DR - Fast Track Migration

If you just want to migrate quickly, follow these steps. For detailed information, see [ESLINT_9_MIGRATION_GUIDE.md](./ESLINT_9_MIGRATION_GUIDE.md).

---

## Prerequisites Check

```bash
# Check Node.js version (must be v18.18.0+)
node --version

# If outdated, install Node.js 20 LTS from https://nodejs.org
```

---

## Step 1: Backup (30 seconds)

```bash
cd frontend

# Backup existing configs
cp .eslintrc.json .eslintrc.json.backup
cp .eslintrc.enhanced.json .eslintrc.enhanced.json.backup
```

---

## Step 2: Install Dependencies (2-3 minutes)

```bash
# Install all required packages
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

## Step 3: Choose Your Config (1 minute)

### Option A: Basic Config (Simple, Minimal)
**Use if**: You only need Next.js + TypeScript with basic rules

```bash
# Copy template to project
cp ../docs/eslint.config.basic.template.mjs ./eslint.config.mjs
```

### Option B: Enhanced Config (Recommended)
**Use if**: You want full accessibility, import ordering, and all current features

```bash
# Copy template to project
cp ../docs/eslint.config.enhanced.template.mjs ./eslint.config.mjs
```

---

## Step 4: Test (1 minute)

```bash
# Test on a single file
npx eslint src/components/ExerciseCard.tsx

# If successful, test entire codebase
npx eslint .

# Test auto-fix
npx eslint . --fix
```

---

## Step 5: Update IDE (30 seconds)

**VS Code**:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Reload Window" and press Enter
3. Check ESLint output panel - should show "Using flat config"

---

## Step 6: Finalize (30 seconds)

```bash
# If everything works, remove old configs
rm .eslintrc.json
rm .eslintrc.enhanced.json
rm .eslintrc.json.backup
rm .eslintrc.enhanced.json.backup

# Commit changes
git add .
git commit -m "chore: Migrate to ESLint 9 with flat config"
```

---

## Troubleshooting Common Issues

### Issue 1: "The Next.js plugin was not detected"
**Quick Fix**: Already handled in templates via FlatCompat. If you see this, verify you copied the template correctly.

---

### Issue 2: "Cannot find tsconfig.json"
**Quick Fix**: Open `eslint.config.mjs` and verify the path at line with `project: './tsconfig.json'` is correct.

If your `tsconfig.json` is in a different location:
```javascript
// In eslint.config.mjs, find this section:
parserOptions: {
  project: './tsconfig.json',  // Update this path
  tsconfigRootDir: __dirname,
}
```

---

### Issue 3: Import plugin errors
**Quick Fix**: The enhanced template uses `eslint-plugin-import-x` which has better ESLint 9 support. If you still have issues:

```bash
# Ensure old plugin is removed
npm uninstall eslint-plugin-import

# Verify import-x is installed
npm list eslint-plugin-import-x
```

---

### Issue 4: Cache errors
**Quick Fix**: Clear the cache

```bash
rm -rf node_modules/.cache/eslint
npx eslint . --no-cache
```

---

## Rollback (If Needed)

If something goes wrong and you need to rollback immediately:

```bash
# Restore old config
cp .eslintrc.json.backup .eslintrc.json
rm eslint.config.mjs

# Downgrade ESLint
npm install eslint@8.57.1 --save-dev

# Restore old TypeScript ESLint
npm uninstall typescript-eslint
npm install @typescript-eslint/parser@5.62.0 @typescript-eslint/eslint-plugin@5.62.0 --save-dev

# Test
npx eslint .
```

---

## Next Steps

After successful migration:

1. Update your CI/CD to use Node.js 18.18.0+ or 20.x
2. Update team documentation
3. Inform team members to:
   - Pull latest changes
   - Run `npm install`
   - Reload their IDE

---

## Complete Migration Time Estimate

- **Preparation**: 5 minutes (reading this guide)
- **Installation**: 3 minutes (npm install)
- **Configuration**: 1 minute (copy template)
- **Testing**: 2 minutes (verify it works)
- **Finalization**: 1 minute (cleanup)

**Total**: ~12 minutes for a smooth migration

---

## Verification Checklist

After migration, verify:

- [ ] `npx eslint .` runs without errors
- [ ] VS Code shows ESLint errors inline
- [ ] Auto-fix works: `npx eslint . --fix`
- [ ] All team members can lint successfully
- [ ] CI/CD pipeline passes

---

## What Changed?

### File Changes
- **Removed**: `.eslintrc.json`, `.eslintrc.enhanced.json`
- **Added**: `eslint.config.mjs`

### Package Changes
- **Updated**: `eslint` 8.57.1 → 9.37.0
- **Removed**: `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `eslint-plugin-import`
- **Added**: `typescript-eslint`, `@eslint/js`, `globals`, `@eslint/eslintrc`, `@eslint/compat`, `eslint-plugin-import-x`
- **Updated**: All other ESLint plugins to latest versions

### Behavior Changes
- **Config Format**: Now uses JavaScript with ES modules instead of JSON
- **Plugin Loading**: Plugins imported directly instead of string references
- **Ignores**: Now configured in `eslint.config.mjs` instead of `.eslintignore`
- **Performance**: Slightly faster linting (especially with `--quiet`)

---

## Getting Help

- **Detailed Guide**: See [ESLINT_9_MIGRATION_GUIDE.md](./ESLINT_9_MIGRATION_GUIDE.md)
- **Summary**: See [ESLINT_MIGRATION_SUMMARY.md](./ESLINT_MIGRATION_SUMMARY.md)
- **Templates**: See `eslint.config.basic.template.mjs` and `eslint.config.enhanced.template.mjs`
- **Official Docs**: https://eslint.org/docs/latest/use/configure/migration-guide

---

**Last Updated**: 2025-10-06
**Migration Path**: ESLint 8.57.1 → 9.37.0
**Config Format**: `.eslintrc.json` → `eslint.config.mjs` (flat config)
**Status**: Ready for production use
