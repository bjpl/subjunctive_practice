// Polyfills that MUST load BEFORE any test files or MSW
// This file is loaded via setupFiles (runs before setupFilesAfterEnv)

// TextEncoder/TextDecoder for MSW 2.x
const { TextEncoder, TextDecoder } = require('util')
global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

// whatwg-fetch for Response, Request, Headers, fetch APIs
require('whatwg-fetch')
