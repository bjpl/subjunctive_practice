// Polyfills that MUST load BEFORE any test files or MSW
// This file is loaded via setupFiles (runs before setupFilesAfterEnv)

// TextEncoder/TextDecoder for MSW 2.x (Node.js < 18 compatibility)
if (typeof global.TextEncoder === 'undefined') {
  const { TextEncoder, TextDecoder } = require('util')
  global.TextEncoder = TextEncoder
  global.TextDecoder = TextDecoder
}

// whatwg-fetch for Response, Request, Headers, fetch APIs
// Note: Node 18+ has native fetch, but we still need this for consistent behavior
if (typeof global.fetch === 'undefined') {
  require('whatwg-fetch')
}

// ReadableStream polyfill for MSW 2.x
if (typeof global.ReadableStream === 'undefined') {
  const { ReadableStream } = require('stream/web')
  global.ReadableStream = ReadableStream
}
