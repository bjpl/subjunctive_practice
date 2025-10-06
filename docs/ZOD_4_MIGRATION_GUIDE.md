# Zod 3.x to 4.x Migration Guide

**Project:** Spanish Subjunctive Practice Application
**Current Version:** Zod 3.23.0
**Target Version:** Zod 4.1.11
**Date:** October 6, 2025

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Critical Breaking Changes](#critical-breaking-changes)
3. [Detailed Migration Path](#detailed-migration-path)
4. [Code Migration Examples](#code-migration-examples)
5. [React Hook Form Integration](#react-hook-form-integration)
6. [Testing Checklist](#testing-checklist)
7. [Rollback Plan](#rollback-plan)
8. [Resources](#resources)

---

## Executive Summary

This guide provides a comprehensive roadmap for migrating the Spanish Subjunctive Practice application from Zod 3.23.0 to Zod 4.1.11. The migration primarily affects authentication forms in:
- `frontend/app/auth/login/page.tsx`
- `frontend/app/auth/register/page.tsx`

**Migration Complexity:** MODERATE
**Estimated Time:** 2-4 hours
**Risk Level:** LOW-MEDIUM (React Hook Form integration has known issues with Zod 4)

---

## Critical Breaking Changes

### TOP 5 Breaking Changes Affecting Our Codebase

#### 1. Unified Error Customization API
**Impact:** HIGH - Affects all custom error messages
**Status:** CRITICAL

**Change:**
- The `message`, `invalid_type_error`, and `required_error` parameters have been replaced with a unified `error` parameter
- Error messages can now be strings or functions

**Migration Required:**
```typescript
// Zod 3.x (CURRENT)
z.string().min(1, "Username is required")
z.string().min(3, { message: "Username must be at least 3 characters" })

// Zod 4.x (TARGET)
z.string().min(1, { error: "Username is required" })
z.string().min(3, { error: "Username must be at least 3 characters" })

// Alternative: Simplified syntax (string still supported but deprecated)
z.string().min(1, "Username is required") // Works but deprecated
```

#### 2. String Format Methods Moved to Top-Level
**Impact:** MEDIUM - Affects email validation in register form
**Status:** BREAKING CHANGE

**Change:**
- `z.string().email()` is deprecated
- New top-level functions: `z.email()`, `z.url()`, etc.

**Migration Required:**
```typescript
// Zod 3.x (CURRENT) - Used in register/page.tsx line 21
email: z.string().email("Invalid email address")

// Zod 4.x (TARGET) - Recommended
email: z.email({ error: "Invalid email address" })

// Zod 4.x (TARGET) - Alternative (deprecated but works)
email: z.string().email({ error: "Invalid email address" })
```

#### 3. Refinement Function Changes - ctx.path Removed
**Impact:** MEDIUM - Affects password confirmation validation
**Status:** BREAKING CHANGE

**Change:**
- `ctx.path` is no longer available in `superRefine()` and `refine()`
- Must manually specify the `path` in `ctx.addIssue()`

**Migration Required:**
```typescript
// Zod 3.x (CURRENT) - register/page.tsx lines 31-34
.refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

// Zod 4.x (TARGET) - Same syntax works! No change needed for this specific case
// However, if using ctx.path inside the refine function:

// DON'T DO THIS in Zod 4:
.superRefine((data, ctx) => {
  const currentPath = ctx.path; // ❌ Not available
})

// DO THIS in Zod 4:
.superRefine((data, ctx) => {
  if (data.password !== data.confirmPassword) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["confirmPassword"], // ✅ Explicitly specify path
      message: "Passwords don't match",
    });
  }
})
```

#### 4. React Hook Form Integration Issues
**Impact:** HIGH - Critical for form validation
**Status:** KNOWN ISSUE

**Change:**
- Zod 4.x has compatibility issues with `@hookform/resolvers`
- Validation errors may be thrown instead of captured in `formState.errors`
- Current `@hookform/resolvers` version: 3.3.0
- Minimum required version for Zod 4: 5.0.1+

**Migration Required:**
```json
// package.json update required
{
  "dependencies": {
    "@hookform/resolvers": "^5.2.2", // Update from ^3.3.0
    "zod": "^4.1.11" // Update from ^3.23.0
  }
}
```

**Known Issues:**
- GitHub Issue #12816: ZodError thrown instead of captured
- GitHub Issue #12829: Feature request for improved Zod v4 support
- Latest fix in @hookform/resolvers v5.2.1 for output type issues

#### 5. Default Values in Optional Fields
**Impact:** LOW-MEDIUM - May affect form behavior
**Status:** BEHAVIOR CHANGE

**Change:**
- Defaults inside properties are now applied even within optional fields
- This aligns better with expectations but may break code relying on key existence

**Migration Required:**
```typescript
// Zod 3.x behavior
const schema = z.object({
  optionalField: z.string().optional().default("default value")
});
// Zod 3: If undefined, key doesn't exist in output

// Zod 4.x behavior
const schema = z.object({
  optionalField: z.string().optional().default("default value")
});
// Zod 4: If undefined, key exists with default value

// Our forms: No impact - we don't use defaults in optional fields
```

---

## Detailed Migration Path

### Phase 1: Preparation (30 minutes)

#### 1.1 Update Dependencies
```bash
cd frontend

# Update Zod to 4.1.11
npm install --save-exact zod@4.1.11

# Update @hookform/resolvers to support Zod 4
npm install --save-exact @hookform/resolvers@5.2.2

# Verify installation
npm list zod @hookform/resolvers
```

#### 1.2 Backup Current Code
```bash
# Create a backup branch
git checkout -b backup/zod-3-pre-migration
git add .
git commit -m "Backup before Zod 4 migration"
git push origin backup/zod-3-pre-migration

# Create migration branch
git checkout main
git checkout -b feat/zod-4-migration
```

#### 1.3 Run Automated Codemod (Optional)
```bash
# Install codemod tool
npx codemod jssg run zod-3-4

# Review changes
git diff

# Note: Codemod doesn't cover all changes - manual review required
```

### Phase 2: Code Migration (60-90 minutes)

#### 2.1 Update Login Form Schema
**File:** `frontend/app/auth/login/page.tsx`

**Current Code (Lines 16-19):**
```typescript
const loginSchema = z.object({
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
});
```

**Migration Option 1 (Minimal Change - Uses Deprecated API):**
```typescript
const loginSchema = z.object({
  username: z.string().min(1, "Username is required"), // Works but deprecated
  password: z.string().min(1, "Password is required"), // Works but deprecated
});
```

**Migration Option 2 (Recommended - Full Zod 4 API):**
```typescript
const loginSchema = z.object({
  username: z.string().min(1, { error: "Username is required" }),
  password: z.string().min(1, { error: "Password is required" }),
});
```

#### 2.2 Update Register Form Schema
**File:** `frontend/app/auth/register/page.tsx`

**Current Code (Lines 15-34):**
```typescript
const registerSchema = z.object({
  username: z.string()
    .min(3, "Username must be at least 3 characters")
    .max(50, "Username must be less than 50 characters")
    .regex(/^[a-zA-Z0-9_]+$/, "Username can only contain letters, numbers, and underscores"),
  email: z.string()
    .email("Invalid email address")
    .min(1, "Email is required"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .max(100, "Password must be less than 100 characters"),
  confirmPassword: z.string()
    .min(1, "Please confirm your password"),
  full_name: z.string()
    .min(1, "Full name is required")
    .max(100, "Full name must be less than 100 characters"),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});
```

**Migration Option 1 (Minimal Change):**
```typescript
const registerSchema = z.object({
  username: z.string()
    .min(3, "Username must be at least 3 characters")
    .max(50, "Username must be less than 50 characters")
    .regex(/^[a-zA-Z0-9_]+$/, "Username can only contain letters, numbers, and underscores"),
  email: z.string()
    .email("Invalid email address") // Still works but deprecated
    .min(1, "Email is required"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .max(100, "Password must be less than 100 characters"),
  confirmPassword: z.string()
    .min(1, "Please confirm your password"),
  full_name: z.string()
    .min(1, "Full name is required")
    .max(100, "Full name must be less than 100 characters"),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match", // 'message' still works in refine
  path: ["confirmPassword"],
});
```

**Migration Option 2 (Recommended - Full Zod 4 API):**
```typescript
const registerSchema = z.object({
  username: z.string()
    .min(3, { error: "Username must be at least 3 characters" })
    .max(50, { error: "Username must be less than 50 characters" })
    .regex(/^[a-zA-Z0-9_]+$/, { error: "Username can only contain letters, numbers, and underscores" }),
  email: z.email({ error: "Invalid email address" }) // ✅ New top-level function
    .min(1, { error: "Email is required" }),
  password: z.string()
    .min(8, { error: "Password must be at least 8 characters" })
    .max(100, { error: "Password must be less than 100 characters" }),
  confirmPassword: z.string()
    .min(1, { error: "Please confirm your password" }),
  full_name: z.string()
    .min(1, { error: "Full name is required" })
    .max(100, { error: "Full name must be less than 100 characters" }),
}).superRefine((data, ctx) => {
  if (data.password !== data.confirmPassword) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["confirmPassword"],
      message: "Passwords don't match",
    });
  }
});
```

**Migration Option 3 (Most Conservative - Keep .refine()):**
```typescript
const registerSchema = z.object({
  username: z.string()
    .min(3, { error: "Username must be at least 3 characters" })
    .max(50, { error: "Username must be less than 50 characters" })
    .regex(/^[a-zA-Z0-9_]+$/, { error: "Username can only contain letters, numbers, and underscores" }),
  email: z.email({ error: "Invalid email address" })
    .min(1, { error: "Email is required" }),
  password: z.string()
    .min(8, { error: "Password must be at least 8 characters" })
    .max(100, { error: "Password must be less than 100 characters" }),
  confirmPassword: z.string()
    .min(1, { error: "Please confirm your password" }),
  full_name: z.string()
    .min(1, { error: "Full name is required" })
    .max(100, { error: "Full name must be less than 100 characters" }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match", // 'message' works in .refine()
  path: ["confirmPassword"],
});
```

#### 2.3 No Changes Needed
**Files with no Zod usage:**
- No other files in the project use Zod schemas based on our analysis

### Phase 3: Testing (60 minutes)

#### 3.1 Type Checking
```bash
cd frontend
npm run type-check
```

**Expected:** No TypeScript errors

#### 3.2 Unit Tests
```bash
npm run test:unit
```

**Expected:** All existing tests pass

#### 3.3 Integration Tests
```bash
npm run test:integration
```

**Expected:** All form validation tests pass

#### 3.4 E2E Tests
```bash
npm run test:e2e
```

**Expected:** All authentication flow tests pass

### Phase 4: Manual Verification (30 minutes)

#### 4.1 Start Development Server
```bash
npm run dev
```

#### 4.2 Test Login Form
1. Navigate to `/auth/login`
2. Test empty fields (should show "Username is required", "Password is required")
3. Test valid credentials
4. Verify error messages display correctly
5. Verify successful login redirects to dashboard

#### 4.3 Test Register Form
1. Navigate to `/auth/register`
2. Test empty fields (should show appropriate error messages)
3. Test invalid email format (should show "Invalid email address")
4. Test short username (should show "Username must be at least 3 characters")
5. Test short password (should show "Password must be at least 8 characters")
6. Test mismatched passwords (should show "Passwords don't match")
7. Test invalid username characters (should show appropriate error)
8. Test valid registration
9. Verify error messages display correctly
10. Verify successful registration redirects to login

---

## Code Migration Examples

### Example 1: Basic String Validation

```typescript
// ❌ Zod 3.x
z.string().min(1, "Required field")

// ✅ Zod 4.x (Recommended)
z.string().min(1, { error: "Required field" })

// ⚠️ Zod 4.x (Works but deprecated)
z.string().min(1, "Required field")
```

### Example 2: Email Validation

```typescript
// ❌ Zod 3.x
z.string().email("Invalid email")

// ✅ Zod 4.x (Recommended)
z.email({ error: "Invalid email" })

// ⚠️ Zod 4.x (Works but deprecated)
z.string().email("Invalid email")
```

### Example 3: Regex Validation

```typescript
// ❌ Zod 3.x
z.string().regex(/^[A-Z]+$/, "Must be uppercase")

// ✅ Zod 4.x (Recommended)
z.string().regex(/^[A-Z]+$/, { error: "Must be uppercase" })

// ⚠️ Zod 4.x (Works but deprecated)
z.string().regex(/^[A-Z]+$/, "Must be uppercase")
```

### Example 4: Conditional Error Messages

```typescript
// ❌ Zod 3.x (not directly supported)
z.string().min(1, "Required")

// ✅ Zod 4.x (New capability)
z.string({
  error: (iss) => iss.input === undefined
    ? "Field is required."
    : "Invalid input."
})
```

### Example 5: Refinements

```typescript
// ✅ Zod 3.x & 4.x (Same API - no change)
.refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

// ✅ Zod 4.x (Alternative with superRefine)
.superRefine((data, ctx) => {
  if (data.password !== data.confirmPassword) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ["confirmPassword"],
      message: "Passwords don't match",
    });
  }
})
```

### Example 6: Multiple Validations

```typescript
// ❌ Zod 3.x
z.string()
  .min(3, "Too short")
  .max(50, "Too long")
  .regex(/^[a-z]+$/, "Lowercase only")

// ✅ Zod 4.x (Recommended)
z.string()
  .min(3, { error: "Too short" })
  .max(50, { error: "Too long" })
  .regex(/^[a-z]+$/, { error: "Lowercase only" })

// ⚠️ Zod 4.x (Works but deprecated)
z.string()
  .min(3, "Too short")
  .max(50, "Too long")
  .regex(/^[a-z]+$/, "Lowercase only")
```

---

## React Hook Form Integration

### Current Setup (Zod 3.x)

```typescript
// frontend/app/auth/login/page.tsx
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm<LoginFormData>({
  resolver: zodResolver(loginSchema),
});
```

### Migration to Zod 4.x

**Step 1: Update @hookform/resolvers**
```json
// package.json
{
  "dependencies": {
    "@hookform/resolvers": "^5.2.2" // Update from ^3.3.0
  }
}
```

**Step 2: No Code Changes Required**
```typescript
// Same code works with Zod 4.x after updating @hookform/resolvers
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod"; // This will now import Zod 4.x

const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm<LoginFormData>({
  resolver: zodResolver(loginSchema), // Works with Zod 4 schemas
});
```

**Step 3: Alternative Import (if needed)**
```typescript
// If you need to use Zod 4 alongside Zod 3
import { z } from "zod/v4"; // Explicit Zod 4 import
```

### Known Issues & Workarounds

**Issue 1: ZodError Not Captured**
- **Symptom:** Validation errors throw exceptions instead of populating `formState.errors`
- **Cause:** Compatibility issue with @hookform/resolvers < 5.0.1
- **Fix:** Update to @hookform/resolvers 5.2.2+

**Issue 2: Type Inference Changes**
- **Symptom:** TypeScript errors with inferred types
- **Cause:** Zod 4 has stricter type inference
- **Fix:** Explicitly type the form data with `z.infer<typeof schema>`

```typescript
// ✅ Explicit typing (recommended)
type LoginFormData = z.infer<typeof loginSchema>;

const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm<LoginFormData>({
  resolver: zodResolver(loginSchema),
});
```

**Issue 3: Error Message Format**
- **Symptom:** Error messages not displaying correctly
- **Cause:** React Hook Form expects specific error structure
- **Fix:** Use the recommended error parameter syntax

```typescript
// ✅ Correct error parameter usage
z.string().min(3, { error: "Too short" })

// ❌ Avoid complex error functions with React Hook Form
z.string({
  error: (iss) => { /* complex logic */ }
})
```

### Testing React Hook Form Integration

**Test Case 1: Field-Level Errors**
```typescript
// Test that individual field errors display correctly
it('displays field-level validation errors', async () => {
  render(<LoginPage />);

  const submitButton = screen.getByRole('button', { name: /login/i });
  fireEvent.click(submitButton);

  await waitFor(() => {
    expect(screen.getByText('Username is required')).toBeInTheDocument();
    expect(screen.getByText('Password is required')).toBeInTheDocument();
  });
});
```

**Test Case 2: Custom Refinement Errors**
```typescript
// Test that custom refinement errors display correctly
it('displays password mismatch error', async () => {
  render(<RegisterPage />);

  fireEvent.change(screen.getByLabelText(/^password$/i), {
    target: { value: 'password123' }
  });
  fireEvent.change(screen.getByLabelText(/confirm password/i), {
    target: { value: 'different' }
  });

  fireEvent.click(screen.getByRole('button', { name: /create account/i }));

  await waitFor(() => {
    expect(screen.getByText("Passwords don't match")).toBeInTheDocument();
  });
});
```

---

## Testing Checklist

### Pre-Migration Tests
- [ ] Run all existing tests to establish baseline
- [ ] Document any flaky or failing tests
- [ ] Create test coverage report: `npm run test:coverage`

### Post-Migration Tests

#### Automated Tests
- [ ] **Type Checking:** `npm run type-check` passes
- [ ] **Unit Tests:** `npm run test:unit` passes
- [ ] **Integration Tests:** `npm run test:integration` passes
- [ ] **E2E Tests:** `npm run test:e2e` passes
- [ ] **Test Coverage:** Maintain or improve coverage percentage

#### Manual Testing - Login Form

**Test Case 1: Empty Form Submission**
- [ ] Navigate to `/auth/login`
- [ ] Click "Login" without entering data
- [ ] Verify error message: "Username is required"
- [ ] Verify error message: "Password is required"
- [ ] Verify error styling applied to fields
- [ ] Verify no console errors

**Test Case 2: Valid Login**
- [ ] Enter valid username
- [ ] Enter valid password
- [ ] Click "Login"
- [ ] Verify successful authentication
- [ ] Verify redirect to dashboard
- [ ] Verify no validation errors

**Test Case 3: Invalid Credentials**
- [ ] Enter username
- [ ] Enter password
- [ ] Click "Login"
- [ ] Verify API error displayed (not Zod validation error)
- [ ] Verify form remains functional

#### Manual Testing - Register Form

**Test Case 4: Empty Form Submission**
- [ ] Navigate to `/auth/register`
- [ ] Click "Create Account" without entering data
- [ ] Verify error: "Full name is required"
- [ ] Verify error: "Username must be at least 3 characters"
- [ ] Verify error: "Email is required"
- [ ] Verify error: "Password must be at least 8 characters"
- [ ] Verify error: "Please confirm your password"

**Test Case 5: Username Validation**
- [ ] Enter username with 2 characters
- [ ] Verify error: "Username must be at least 3 characters"
- [ ] Enter username with 51 characters
- [ ] Verify error: "Username must be less than 50 characters"
- [ ] Enter username with special characters (e.g., "user@123")
- [ ] Verify error: "Username can only contain letters, numbers, and underscores"
- [ ] Enter valid username (e.g., "user_123")
- [ ] Verify no username error

**Test Case 6: Email Validation**
- [ ] Enter invalid email (e.g., "notanemail")
- [ ] Verify error: "Invalid email address"
- [ ] Enter valid email (e.g., "user@example.com")
- [ ] Verify no email error

**Test Case 7: Password Validation**
- [ ] Enter password with 7 characters
- [ ] Verify error: "Password must be at least 8 characters"
- [ ] Enter password with 101 characters
- [ ] Verify error: "Password must be less than 100 characters"
- [ ] Enter valid password (e.g., "password123")
- [ ] Verify no password error

**Test Case 8: Password Confirmation**
- [ ] Enter password: "password123"
- [ ] Enter confirm password: "different"
- [ ] Click "Create Account"
- [ ] Verify error: "Passwords don't match"
- [ ] Verify error appears on confirmPassword field
- [ ] Update confirm password to: "password123"
- [ ] Verify error clears

**Test Case 9: Full Name Validation**
- [ ] Leave full name empty
- [ ] Verify error: "Full name is required"
- [ ] Enter full name with 101 characters
- [ ] Verify error: "Full name must be less than 100 characters"
- [ ] Enter valid full name
- [ ] Verify no full name error

**Test Case 10: Valid Registration**
- [ ] Enter valid full name
- [ ] Enter valid username
- [ ] Enter valid email
- [ ] Enter valid password
- [ ] Enter matching confirm password
- [ ] Click "Create Account"
- [ ] Verify successful registration
- [ ] Verify redirect to login page
- [ ] Verify success toast message

#### Error Display Tests
- [ ] Verify error messages are red/destructive color
- [ ] Verify error messages appear below relevant fields
- [ ] Verify multiple errors display simultaneously
- [ ] Verify errors clear when field is corrected
- [ ] Verify no TypeScript errors in browser console
- [ ] Verify no React errors in browser console

#### Accessibility Tests
- [ ] Run accessibility tests: `npm run test:a11y`
- [ ] Verify error messages are associated with inputs (aria-describedby)
- [ ] Verify form is navigable via keyboard
- [ ] Verify error announcements work with screen readers
- [ ] Verify focus management during error states

#### Cross-Browser Tests
- [ ] Test in Chrome
- [ ] Test in Firefox
- [ ] Test in Safari
- [ ] Test in Edge

#### Performance Tests
- [ ] Verify no performance regression in form rendering
- [ ] Verify validation response time < 100ms
- [ ] Verify no memory leaks during repeated form submissions

---

## Rollback Plan

### If Migration Fails

**Scenario 1: Type Errors**
```bash
# Revert to Zod 3.x
cd frontend
npm install --save-exact zod@3.23.0
npm install --save-exact @hookform/resolvers@3.3.0

# Verify
npm list zod @hookform/resolvers
npm run type-check
```

**Scenario 2: Tests Fail**
```bash
# Revert code changes
git checkout main -- frontend/app/auth/login/page.tsx
git checkout main -- frontend/app/auth/register/page.tsx

# Revert dependencies
npm install --save-exact zod@3.23.0
npm install --save-exact @hookform/resolvers@3.3.0

# Verify
npm run test:all
```

**Scenario 3: Runtime Errors**
```bash
# Complete rollback
git checkout main

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Verify
npm run dev
```

**Scenario 4: React Hook Form Integration Issues**
```bash
# Option 1: Wait for @hookform/resolvers update
# Stay on Zod 3.x until @hookform/resolvers fully supports Zod 4

# Option 2: Use Zod 3.x via subpath import
# If Zod 4 is installed but causing issues
import { z } from "zod/v3"; // Use Zod 3 API
```

### Communication Plan
1. **Before Migration:**
   - Notify team of planned migration
   - Document current state
   - Create backup branch

2. **During Migration:**
   - Monitor test results
   - Document issues encountered
   - Take screenshots of errors

3. **After Migration:**
   - Update team on status
   - Document lessons learned
   - Update this guide with findings

### Emergency Rollback Steps
```bash
# 1. Stop development server
Ctrl+C

# 2. Revert to backup branch
git checkout backup/zod-3-pre-migration

# 3. Reinstall dependencies
cd frontend
npm install

# 4. Restart server
npm run dev

# 5. Verify functionality
# Test login and register forms manually
```

---

## Additional Breaking Changes Reference

### Changes Not Affecting Our Codebase

#### Number Validation
- `POSITIVE_INFINITY` and `NEGATIVE_INFINITY` no longer valid for `z.number()`
- `.safe()` now behaves identically to `.int()`
- **Impact:** None (we don't use number schemas)

#### Object Methods
- `.strict()`, `.passthrough()`, and `.strip()` deprecated
- Use `z.strictObject()` and `z.looseObject()` instead
- `.merge()` deprecated, use `.extend()`
- **Impact:** None (we don't use these methods)

#### ZodError Methods
- `.format()` deprecated, use `z.treeifyError()`
- `.flatten()` deprecated, use `z.treeifyError()`
- **Impact:** None (we don't format ZodErrors directly)

#### Function Schemas
- `z.function()` now a "function factory"
- New API with `.args()` and `.returns()` upfront
- **Impact:** None (we don't use function schemas)

#### Array Methods
- `.nonempty()` inferred type changed
- **Impact:** None (we don't use array schemas)

#### Coercion
- `z.coerce` schemas now have `unknown` input type
- **Impact:** None (we don't use coercion)

#### Default Values
- `.default()` short-circuits parsing for `undefined`
- New `.prefault()` to replicate old behavior
- **Impact:** None (we don't use defaults)

---

## Resources

### Official Documentation
- **Zod 4 Release Notes:** https://zod.dev/v4
- **Zod 4 Migration Guide:** https://zod.dev/v4/changelog
- **Zod 4 Error Customization:** https://zod.dev/error-customization
- **Zod 4 Error Formatting:** https://zod.dev/error-formatting
- **Zod 4 API Reference:** https://zod.dev/api

### Community Resources
- **Codemod Migration Tool:** https://docs.codemod.com/guides/migrations/zod-3-4
- **React Hook Form Resolvers:** https://github.com/react-hook-form/resolvers
- **Zod GitHub Repository:** https://github.com/colinhacks/zod

### Known Issues
- **React Hook Form Zod 4 Support:** https://github.com/react-hook-form/react-hook-form/issues/12829
- **ZodError Not Captured:** https://github.com/react-hook-form/react-hook-form/issues/12816

### Package Versions
- **Current Zod:** 3.23.0
- **Target Zod:** 4.1.11
- **Current @hookform/resolvers:** 3.3.0
- **Target @hookform/resolvers:** 5.2.2+
- **React Hook Form:** 7.51.0 (no update needed)

### Additional Learning
- **Zod Email Validation:** https://medium.com/@python-javascript-php-html-css/zod-email-validation-and-email-confirmation-f1cf3d5a915a
- **Refinements Guide:** https://brockherion.dev/blog/posts/creating-extendable-zod-schemas-with-refine/
- **Form Validation Tutorial:** https://www.freecodecamp.org/news/react-form-validation-zod-react-hook-form/

---

## Appendix A: Quick Reference

### Most Common Migrations

| Zod 3.x | Zod 4.x (Recommended) | Zod 4.x (Deprecated) |
|---------|----------------------|----------------------|
| `z.string().min(1, "Error")` | `z.string().min(1, { error: "Error" })` | `z.string().min(1, "Error")` |
| `z.string().email("Error")` | `z.email({ error: "Error" })` | `z.string().email("Error")` |
| `z.string().url("Error")` | `z.url({ error: "Error" })` | `z.string().url("Error")` |
| `z.string().regex(/.../, "Error")` | `z.string().regex(/.../, { error: "Error" })` | `z.string().regex(/.../, "Error")` |

### Import Statements

```typescript
// Standard import (works for both Zod 3 and 4)
import * as z from "zod";

// Explicit Zod 4 import
import { z } from "zod/v4";

// React Hook Form resolver
import { zodResolver } from "@hookform/resolvers/zod";
```

### Type Inference

```typescript
// Define schema
const schema = z.object({
  username: z.string(),
  email: z.email(),
});

// Infer TypeScript type
type FormData = z.infer<typeof schema>;
// Result: { username: string; email: string }
```

---

## Appendix B: Migration Decision Matrix

| Factor | Stay on Zod 3.x | Migrate to Zod 4.x |
|--------|----------------|-------------------|
| **@hookform/resolvers compatibility** | ✅ Stable (v3.3.0) | ⚠️ Requires v5.2.2+ |
| **New features needed** | ❌ No | ✅ Yes (better error handling) |
| **Performance improvements** | ❌ No | ✅ Yes (2.8-4.4x faster) |
| **Tree-shaking benefits** | ❌ Limited | ✅ Improved |
| **Long-term support** | ⚠️ End of life soon | ✅ Active development |
| **Breaking changes** | ✅ None | ⚠️ Some (manageable) |
| **Migration effort** | ✅ None | ⚠️ 2-4 hours |
| **Risk level** | ✅ Low | ⚠️ Medium |

**Recommendation:** MIGRATE to Zod 4.x
- Benefits outweigh costs
- Low complexity for our use case
- Future-proof the application
- Improved performance and DX

---

## Appendix C: Validation Performance Comparison

### Zod 3.x vs Zod 4.x Performance

According to official benchmarks:
- **2.8-4.4x speed improvement** in Zod 4.x
- **Smaller bundle size** due to improved tree-shaking
- **Reduced memory footprint** with new parsing architecture

### Our Application Impact
- **Forms affected:** 2 (login, register)
- **Schemas affected:** 2
- **Average validations per session:** ~3-5
- **Expected performance gain:** 10-50ms per validation
- **User-facing impact:** Imperceptible but positive

---

## Document Metadata

**Version:** 1.0
**Created:** October 6, 2025
**Last Updated:** October 6, 2025
**Author:** Development Team
**Status:** Ready for Implementation
**Review Status:** Pending Team Review

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-06 | 1.0 | Initial migration guide created |

---

**END OF MIGRATION GUIDE**
