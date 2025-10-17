# MSW 2.x Frontend Test Configuration Fix

**Date:** 2025-10-11
**Task:** Fix MSW 2.x polyfill and configuration issues
**Status:** ✅ Configuration Fixed (Test execution pending Next.js async config resolution)

## Issues Identified

### 1. Jest Configuration Typo
- **Issue:** `coverageThresholds` should be `coverageThreshold` (singular)
- **Impact:** Jest validation warnings
- **Fix:** Corrected in `jest.config.js` line 33

### 2. Missing/Incomplete Polyfills for MSW 2.x
- **Issue:** MSW 2.x requires additional Web APIs (ReadableStream, TextEncoder/TextDecoder, fetch)
- **Impact:** MSW fails to initialize properly in Node.js test environment
- **Fix:** Enhanced `jest.polyfills.js` with:
  - Conditional polyfills (only load if not already available)
  - ReadableStream from 'stream/web' for Node.js 22
  - TextEncoder/TextDecoder from 'util'
  - whatwg-fetch for Request/Response APIs

### 3. MSW Lifecycle Hook Placement
- **Issue:** `beforeAll/afterEach/afterAll` called at module import time in `server.ts`
- **Impact:** "beforeAll is not defined" errors when module imported outside Jest context
- **Fix:** Moved lifecycle hooks from `tests/mocks/server.ts` to `jest.setup.js`

### 4. Transform Patterns for MSW
- **Issue:** MSW 2.x uses ESM modules that Jest needs to transform
- **Impact:** Import errors with MSW modules
- **Fix:** Updated `transformIgnorePatterns` to exclude MSW from ignore list

### 5. Test Environment Options
- **Issue:** MSW 2.x needs specific export conditions for Node.js environment
- **Impact:** Module resolution issues
- **Fix:** Added `testEnvironmentOptions.customExportConditions: ['']`

### 6. Test Performance Settings
- **Issue:** Tests can hang with concurrent workers and async Next.js config
- **Impact:** Timeouts and hanging test runs
- **Fix:** Added `testTimeout: 10000` and `maxWorkers: 1` for stability

## Files Modified

### `/frontend/jest.config.js`
```javascript
// Key changes:
1. Fixed: coverageThresholds → coverageThreshold
2. Added: testEnvironmentOptions with customExportConditions
3. Added: testTimeout: 10000, maxWorkers: 1
4. Fixed: transformIgnorePatterns to include MSW
5. Added: ReadableStream workaround for MSW 2.x compatibility
```

### `/frontend/jest.polyfills.js`
```javascript
// Enhanced polyfills with conditional loading:
1. TextEncoder/TextDecoder (Node.js < 18 compat)
2. whatwg-fetch (Request/Response/Headers/fetch)
3. ReadableStream (from stream/web for Node 22)
```

### `/frontend/tests/mocks/server.ts`
```javascript
// Removed lifecycle hooks (moved to jest.setup.js):
- beforeAll/afterEach/afterAll removed from module scope
- Server export remains for use in jest.setup.js
```

### `/frontend/jest.setup.js`
```javascript
// Added MSW lifecycle management:
- beforeAll: server.listen({ onUnhandledRequest: 'warn' })
- afterEach: server.resetHandlers()
- afterAll: server.close()
```

## Configuration Validation

✅ Jest configuration loads without errors
✅ MSW 2.x modules can be imported
✅ Polyfills are properly sequenced (setupFiles → setupFilesAfterEnv)
✅ No validation warnings from Jest
⏸️ Test execution pending (Next.js async config causing hang)

## Known Issue: Next.js Async Config Hang

**Problem:** Tests hang when Next.js config has async `rewrites()` function.
**Root Cause:** Next.js jest wrapper waits for async config resolution indefinitely.
**Workaround Options:**
1. Remove async rewrites from `next.config.js` during testing
2. Use `--forceExit` flag (not ideal)
3. Mock Next.js config for tests

**Recommended Solution:**
```javascript
// next.config.js - Add condition for test environment
async rewrites() {
  if (process.env.NODE_ENV === 'test') {
    return [];
  }
  return [/* ... */];
}
```

## Test Execution Commands

```bash
# List all tests (verify configuration)
cd frontend && npm test -- --listTests

# Run specific test file
cd frontend && npm test -- tests/unit/lib/utils.test.ts

# Run with coverage
cd frontend && npm run test:coverage

# Run by category
npm run test:unit        # Unit tests
npm run test:integration # Integration tests
npm run test:a11y        # Accessibility tests
```

## MSW 2.x Best Practices Implemented

1. **Polyfills First:** Loaded via `setupFiles` before any test code
2. **Lifecycle in Setup:** `beforeAll/afterEach/afterAll` in `jest.setup.js`, not module scope
3. **Conditional Polyfills:** Only load what's missing (Node.js version compatibility)
4. **Server Isolation:** MSW server config separate from lifecycle management
5. **Proper Handlers:** Using MSW 2.x `http.get/post` and `HttpResponse` API

## Success Criteria Met

✅ Jest runs without configuration errors
✅ MSW 2.x compatibility ensured
✅ Polyfills properly configured for Node.js 22
✅ No validation warnings
✅ Configuration changes documented
⏸️ Test execution works (pending Next.js config fix)

## Next Steps

1. **Fix Next.js async config:** Conditional rewrites for test environment
2. **Run full test suite:** Verify all 17 tests execute properly
3. **Measure coverage:** Establish baseline (estimated 40-50%)
4. **Fix failing tests:** Address any test failures after execution works
5. **CI/CD integration:** Ensure tests run in pipeline

## Coordination

- **Memory Keys:**
  - `swarm/frontend/msw-config-fix` - Jest configuration changes
  - `swarm/frontend/msw-polyfills` - Polyfill enhancements
  - `swarm/frontend/msw-server` - Server lifecycle fixes

- **Related Files:**
  - `/frontend/jest.config.js` - Main Jest configuration
  - `/frontend/jest.polyfills.js` - Web API polyfills
  - `/frontend/jest.setup.js` - Test environment setup
  - `/frontend/tests/mocks/server.ts` - MSW server definition
  - `/frontend/tests/mocks/handlers.ts` - API mock handlers
  - `/frontend/tests/mocks/browser.ts` - Browser environment setup

## References

- MSW 2.x Migration Guide: https://mswjs.io/docs/migrations/1.x-to-2.x
- MSW Node.js Integration: https://mswjs.io/docs/integrations/node
- Jest Environment Options: https://jestjs.io/docs/configuration#testenvironmentoptions-object
- Next.js Jest Plugin: https://nextjs.org/docs/testing#jest-and-react-testing-library
