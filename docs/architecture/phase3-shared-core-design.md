# Phase 3: Shared Core Extraction - System Architecture Design

**Document Version:** 1.0.0
**Date:** 2025-10-02
**Author:** System Architecture Designer
**Phase:** 3 of 5 (Refactoring Roadmap)

## Executive Summary

This document outlines the architecture for extracting shared business logic from desktop (PyQt/Python) and web (FastAPI/React) platforms into a unified, platform-agnostic core library. The goal is to reduce code duplication from 20% to <5% while maintaining full functionality across all platforms.

## Current State Analysis

### Existing Code Duplication (Estimated 20%)

#### 1. **Conjugation Logic**
- **Desktop:** `/src/shared/conjugation_reference.py` (159 lines)
- **Web Backend:** `/src/web/backend/services/exercise_generator.py` (lines 164-191, 301-360)
- **JavaScript Core:** `/src/core/conjugation.js` (already extracted, needs validation)
- **Duplication:** Conjugation rules, irregular verbs, stem-changing patterns duplicated across Python and JavaScript

#### 2. **Exercise Generation**
- **Desktop:** Uses `TBLTTaskGenerator` from `/src/shared/tblt_scenarios.py`
- **Web Backend:** `/src/web/backend/services/exercise_generator.py` (full service, 508 lines)
- **JavaScript Core:** `/src/core/exercises.js` (already extracted)
- **Duplication:** Exercise templates, difficulty selection, verb selection logic duplicated

#### 3. **Learning Analytics**
- **Desktop:** `/src/shared/learning_analytics.py` (374 lines)
  - StreakTracker, ErrorAnalyzer, AdaptiveDifficulty, PracticeGoals
- **Web Backend:** Needs to implement similar analytics
- **JavaScript Core:** `/src/core/analytics.js` (partial implementation)
- **Duplication:** Error pattern detection, weakness analysis, adaptive algorithms

#### 4. **Session Management**
- **Desktop:** `/src/shared/session_manager.py` (174 lines)
  - SessionManager, ReviewQueue classes
- **Web Backend:** Session logic embedded in services
- **JavaScript Core:** `/src/core/session.js` (already extracted)
- **Duplication:** Session tracking, review queue management, statistics calculation

#### 5. **Validation Logic**
- **Desktop:** Distributed across exercise generators
- **Web Backend:** `_evaluate_answer`, `_normalize_answer` methods
- **Frontend:** Answer validation in components
- **Duplication:** Answer normalization, comparison logic, accent handling

### Code Organization Issues

1. **Python modules in `/src/shared/`** are desktop-specific (use Python-only features)
2. **JavaScript core in `/src/core/`** is partially complete but not validated
3. **Web backend** re-implements logic instead of using shared code
4. **No unified data schemas** - each platform uses different formats

## Target Architecture

### Shared Core Structure

```
/src/shared/core/
├── README.md                          # Core library documentation
├── package.json                       # JavaScript package metadata
├── setup.py                          # Python package metadata
│
├── conjugation/                      # Conjugation engine (multi-language)
│   ├── __init__.py                  # Python exports
│   ├── index.js                     # JavaScript exports
│   ├── rules.json                   # Language-agnostic conjugation rules
│   ├── irregular_verbs.json         # Irregular verb database
│   ├── stem_changes.json            # Stem-changing patterns
│   ├── engine.py                    # Python implementation
│   └── engine.js                    # JavaScript implementation
│
├── exercises/                        # Exercise generation (multi-language)
│   ├── __init__.py
│   ├── index.js
│   ├── templates.json               # Exercise templates (language-agnostic)
│   ├── difficulty_rules.json        # Difficulty progression rules
│   ├── generator.py                 # Python implementation
│   └── generator.js                 # JavaScript implementation
│
├── analytics/                        # Learning analytics (multi-language)
│   ├── __init__.py
│   ├── index.js
│   ├── error_patterns.json          # Error categorization rules
│   ├── learning_models.json         # Adaptive learning models
│   ├── analyzer.py                  # Python implementation
│   └── analyzer.js                  # JavaScript implementation
│
├── session/                          # Session management (multi-language)
│   ├── __init__.py
│   ├── index.js
│   ├── session_schema.json          # Session data schema
│   ├── manager.py                   # Python implementation
│   └── manager.js                   # JavaScript implementation
│
├── validation/                       # Answer validation (multi-language)
│   ├── __init__.py
│   ├── index.js
│   ├── validation_rules.json        # Validation rules
│   ├── validator.py                 # Python implementation
│   └── validator.js                 # JavaScript implementation
│
├── schemas/                          # JSON schemas for all data structures
│   ├── exercise.schema.json         # Exercise data format
│   ├── session.schema.json          # Session data format
│   ├── analytics.schema.json        # Analytics data format
│   ├── feedback.schema.json         # Feedback data format
│   └── progress.schema.json         # Progress data format
│
└── adapters/                         # Platform-specific adapters
    ├── python/                      # Python adapter layer
    │   ├── __init__.py
    │   ├── desktop_adapter.py       # PyQt desktop adapter
    │   └── fastapi_adapter.py       # FastAPI web adapter
    └── javascript/                  # JavaScript adapter layer
        ├── index.js
        ├── react_adapter.js         # React frontend adapter
        └── node_adapter.js          # Node.js backend adapter
```

## Architecture Principles

### 1. Platform Agnostic Design

**Rule:** Core logic MUST NOT depend on platform-specific libraries

```python
# ❌ BAD: Platform-specific
from PyQt6.QtCore import QSettings

class SessionManager:
    def save(self):
        settings = QSettings()  # PyQt dependency!
        settings.setValue("session", self.data)
```

```python
# ✅ GOOD: Platform-agnostic
import json

class SessionManager:
    def to_dict(self) -> dict:
        """Return session data as dictionary"""
        return {
            "start_time": self.start_time.isoformat(),
            "exercises_completed": self.exercises_completed,
            "correct_answers": self.correct_answers
        }

    def save(self, storage_handler):
        """Save using provided storage handler (adapter pattern)"""
        data = self.to_dict()
        storage_handler.save("session", data)
```

### 2. Data Format Standardization

**Rule:** All data MUST be serializable to JSON using defined schemas

```json
// exercise.schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "question", "correct_answer", "difficulty"],
  "properties": {
    "id": {"type": "string"},
    "question": {"type": "string"},
    "correct_answer": {"type": "string"},
    "difficulty": {"enum": ["beginner", "intermediate", "advanced"]},
    "category": {"enum": ["present", "past", "future", "compound"]},
    "exercise_type": {"enum": ["fill_blank", "multiple_choice", "conjugation"]},
    "options": {"type": "array", "items": {"type": "string"}},
    "hint": {"type": "string"},
    "explanation": {"type": "string"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "learning_objectives": {"type": "array", "items": {"type": "string"}},
    "estimated_time": {"type": "integer", "minimum": 0}
  }
}
```

### 3. Adapter Pattern for Integration

**Rule:** Each platform uses adapters to integrate with shared core

```python
# Desktop adapter (PyQt)
from src.shared.core.session import SessionManager
from PyQt6.QtCore import QSettings

class DesktopSessionAdapter:
    def __init__(self):
        self.core = SessionManager()
        self.storage = QSettings()

    def save_session(self):
        data = self.core.to_dict()
        self.storage.setValue("session_data", json.dumps(data))

    def load_session(self):
        data = json.loads(self.storage.value("session_data", "{}"))
        self.core.from_dict(data)
```

```javascript
// React adapter (Frontend)
import { SessionManager } from '@/shared/core/session';

class ReactSessionAdapter {
  constructor() {
    this.core = new SessionManager();
  }

  saveSession() {
    const data = this.core.toDict();
    localStorage.setItem('session_data', JSON.stringify(data));
  }

  loadSession() {
    const data = JSON.parse(localStorage.getItem('session_data') || '{}');
    this.core.fromDict(data);
  }
}
```

### 4. Language Parity

**Rule:** Python and JavaScript implementations MUST have identical APIs

```python
# Python implementation
class ConjugationEngine:
    def conjugate(self, verb: str, tense: str, person: str) -> str:
        """Conjugate verb in specified tense and person"""
        pass

    def validate(self, verb: str, tense: str, person: str, answer: str) -> dict:
        """Validate conjugation answer"""
        pass
```

```javascript
// JavaScript implementation
class ConjugationEngine {
  conjugate(verb, tense, person) {
    // Conjugate verb in specified tense and person
  }

  validate(verb, tense, person, answer) {
    // Validate conjugation answer
  }
}
```

## Extraction Plan

### Phase 3.1: Data Schema Creation

**Objective:** Create JSON schemas for all shared data structures

**Deliverables:**
1. `exercise.schema.json` - Exercise data format
2. `session.schema.json` - Session tracking format
3. `analytics.schema.json` - Analytics data format
4. `feedback.schema.json` - Feedback response format
5. `progress.schema.json` - Progress tracking format

**Benefits:**
- Ensures data consistency across platforms
- Enables validation
- Self-documenting API

### Phase 3.2: Conjugation Core

**Objective:** Extract conjugation logic to shared core

**Current Duplication:**
- Python: `conjugation_reference.py` (159 lines)
- JavaScript: `core/conjugation.js` (partial)
- Web: Embedded in `exercise_generator.py`

**Extraction Tasks:**
1. Create `conjugation/rules.json` with all conjugation rules
2. Create `conjugation/irregular_verbs.json` with irregular verb database
3. Implement `conjugation/engine.py` reading from JSON
4. Implement `conjugation/engine.js` reading from JSON
5. Validate API parity between Python and JavaScript
6. Update desktop app to use shared core
7. Update web backend to use shared core

**Expected Reduction:** ~200 lines of duplicated code eliminated

### Phase 3.3: Exercise Generation Core

**Objective:** Extract exercise generation to shared core

**Current Duplication:**
- Python: `tblt_scenarios.py` + logic in `exercise_generator.py`
- JavaScript: `core/exercises.js` (partial)

**Extraction Tasks:**
1. Create `exercises/templates.json` with all templates
2. Create `exercises/difficulty_rules.json` with progression rules
3. Implement `exercises/generator.py` reading from JSON
4. Implement `exercises/generator.js` reading from JSON
5. Extract TBLT methodology to shared algorithms
6. Update platforms to use shared core

**Expected Reduction:** ~300 lines of duplicated code eliminated

### Phase 3.4: Analytics Core

**Objective:** Extract learning analytics to shared core

**Current Duplication:**
- Python: `learning_analytics.py` (374 lines)
- JavaScript: `core/analytics.js` (partial, ~100 lines)

**Extraction Tasks:**
1. Create `analytics/error_patterns.json` with pattern rules
2. Create `analytics/learning_models.json` with adaptive models
3. Implement `analytics/analyzer.py` with ErrorAnalyzer, StreakTracker, AdaptiveDifficulty
4. Implement `analytics/analyzer.js` with identical API
5. Extract achievement system to shared core
6. Update platforms to use shared analytics

**Expected Reduction:** ~400 lines of duplicated code eliminated

### Phase 3.5: Session Management Core

**Objective:** Extract session tracking to shared core

**Current Duplication:**
- Python: `session_manager.py` (174 lines)
- JavaScript: `core/session.js` (partial)

**Extraction Tasks:**
1. Create `session/session_schema.json`
2. Implement `session/manager.py` with SessionManager, ReviewQueue
3. Implement `session/manager.js` with identical API
4. Extract statistics calculation to shared core
5. Update platforms to use shared session management

**Expected Reduction:** ~200 lines of duplicated code eliminated

### Phase 3.6: Validation Core

**Objective:** Extract answer validation to shared core

**Current Duplication:**
- Scattered across platforms in different methods

**Extraction Tasks:**
1. Create `validation/validation_rules.json`
2. Implement `validation/validator.py`
3. Implement `validation/validator.js`
4. Consolidate all answer normalization logic
5. Consolidate all comparison logic
6. Update platforms to use shared validation

**Expected Reduction:** ~100 lines of duplicated code eliminated

### Phase 3.7: Adapter Layer Implementation

**Objective:** Create platform-specific adapters

**Deliverables:**
1. Desktop adapter (`adapters/python/desktop_adapter.py`)
2. FastAPI adapter (`adapters/python/fastapi_adapter.py`)
3. React adapter (`adapters/javascript/react_adapter.js`)
4. Node.js adapter (`adapters/javascript/node_adapter.js`)

**Responsibilities:**
- Storage abstraction (QSettings, localStorage, database)
- UI framework integration
- Platform-specific features (notifications, etc.)

### Phase 3.8: Platform Migration

**Objective:** Update all platforms to use shared core

**Desktop Platform:**
- Replace `from src.shared.conjugation_reference` with `from src.shared.core.conjugation`
- Use desktop adapter for storage
- Validate all functionality maintained

**Web Backend:**
- Replace embedded logic with shared core imports
- Use FastAPI adapter for database integration
- Validate API responses match schema

**Web Frontend:**
- Import JavaScript core modules
- Use React adapter for state management
- Validate UI functionality maintained

## Duplication Measurement

### Baseline (Current State)

**Total Lines of Code:** ~2,000 lines (estimated)
- Conjugation: 200 lines duplicated
- Exercise generation: 300 lines duplicated
- Analytics: 400 lines duplicated
- Session management: 200 lines duplicated
- Validation: 100 lines duplicated

**Total Duplication:** ~1,200 lines = 60% duplication rate

### Target (Post-Extraction)

**Shared Core:** ~1,500 lines (single source of truth)
- JSON data files: 500 lines
- Python implementations: 500 lines
- JavaScript implementations: 500 lines

**Platform-Specific Code:** ~500 lines
- Adapters: 300 lines
- UI integration: 200 lines

**Total Duplication:** <100 lines = <5% duplication rate

**Reduction:** 60% → <5% duplication (92% improvement)

## Technical Decisions

### Decision 1: Dual Implementation Strategy

**Options:**
1. **Python-only** with JavaScript bindings (e.g., Pyodide, Transcrypt)
2. **JavaScript-only** with Python bindings (e.g., Node.js in Python)
3. **Dual implementation** with JSON schemas as source of truth

**Decision:** Dual implementation ✅

**Rationale:**
- Native performance on each platform
- No runtime dependencies (Pyodide is large)
- Type safety in both languages
- JSON schemas ensure data consistency
- Easier debugging and testing

### Decision 2: Schema-Driven Development

**Decision:** Use JSON schemas as single source of truth for data structures

**Benefits:**
- Language-agnostic definitions
- Automatic validation
- Self-documenting
- Code generation potential
- Contract testing between platforms

### Decision 3: Adapter Pattern

**Decision:** Use adapter pattern for platform integration

**Benefits:**
- Clean separation of concerns
- Platform-specific optimizations
- Easy to add new platforms
- Testable in isolation

## Quality Attributes

### Performance

**Requirement:** Core operations must complete in <100ms

**Approach:**
- JSON files loaded once at startup
- In-memory caching of compiled rules
- Lazy loading of large datasets

### Maintainability

**Requirement:** Single source of truth for business logic

**Approach:**
- JSON schemas enforce consistency
- Dual implementation with API parity tests
- Comprehensive documentation

### Testability

**Requirement:** >90% code coverage for core modules

**Approach:**
- Unit tests for each module (Python + JavaScript)
- Integration tests with adapters
- Schema validation tests
- Cross-platform API parity tests

### Extensibility

**Requirement:** Easy to add new languages/features

**Approach:**
- Modular architecture
- JSON-based configuration
- Adapter pattern for platforms
- Plugin system for new exercise types

## Migration Strategy

### Stage 1: Parallel Development

1. Create shared core alongside existing code
2. Write comprehensive tests for shared core
3. No changes to existing platforms

### Stage 2: Desktop Migration

1. Update desktop app to use shared core
2. Keep old code as fallback
3. Run side-by-side comparison tests
4. Full validation before removal

### Stage 3: Web Backend Migration

1. Update FastAPI services to use shared core
2. Validate API responses unchanged
3. Performance benchmarking
4. Gradual rollout

### Stage 4: Frontend Migration

1. Update React components to use JavaScript core
2. Validate UI behavior unchanged
3. End-to-end testing
4. Production deployment

### Stage 5: Cleanup

1. Remove deprecated code
2. Update documentation
3. Measure duplication reduction
4. Archive old implementations

## Risk Assessment

### Risk 1: API Divergence

**Risk:** Python and JavaScript implementations drift apart

**Mitigation:**
- Automated API parity tests
- Shared JSON schemas
- CI/CD validation
- Regular cross-platform testing

### Risk 2: Performance Regression

**Risk:** Shared core slower than optimized platform code

**Mitigation:**
- Performance benchmarking before/after
- Profiling of core operations
- Caching strategies
- Platform-specific optimizations in adapters

### Risk 3: Breaking Changes

**Risk:** Migration breaks existing functionality

**Mitigation:**
- Comprehensive test suite
- Gradual migration strategy
- Feature flags for rollback
- Parallel running during transition

### Risk 4: JSON Schema Bloat

**Risk:** JSON files become too large to maintain

**Mitigation:**
- Modular JSON file structure
- Schema composition and references
- Automated schema generation tools
- Documentation generation from schemas

## Success Metrics

### Primary Metrics

1. **Duplication Reduction:** 60% → <5% (Target: <5%)
2. **Code Maintenance:** Single source of truth for business logic
3. **Test Coverage:** >90% for all core modules
4. **Performance:** Core operations <100ms

### Secondary Metrics

1. **Development Velocity:** Faster feature development
2. **Bug Reduction:** Fewer platform-specific bugs
3. **Code Quality:** Improved maintainability scores
4. **Documentation:** Complete API documentation

## Next Steps

1. **Review and Approval:** Architecture review by development team
2. **Prototype:** Build conjugation core as proof of concept
3. **Validation:** Test with both platforms
4. **Full Implementation:** Execute complete extraction plan
5. **Documentation:** Complete developer guides
6. **Training:** Team onboarding to new architecture

## Appendices

### Appendix A: File Inventory

**Files to be consolidated:**
- `/src/shared/conjugation_reference.py`
- `/src/shared/session_manager.py`
- `/src/shared/learning_analytics.py`
- `/src/shared/tblt_scenarios.py`
- `/src/core/*.js` (partial implementations)
- `/src/web/backend/services/exercise_generator.py`

**New files to be created:**
- `/src/shared/core/conjugation/*.{py,js,json}`
- `/src/shared/core/exercises/*.{py,js,json}`
- `/src/shared/core/analytics/*.{py,js,json}`
- `/src/shared/core/session/*.{py,js,json}`
- `/src/shared/core/validation/*.{py,js,json}`
- `/src/shared/core/schemas/*.schema.json`
- `/src/shared/core/adapters/**/*.{py,js}`

### Appendix B: Technology Stack

**Core Implementation:**
- Python 3.9+ (type hints, dataclasses)
- JavaScript ES2018+ (async/await, classes)
- JSON Schema Draft 07

**Testing:**
- Python: pytest, hypothesis
- JavaScript: Jest, fast-check
- Schema: ajv (JSON Schema validator)

**Documentation:**
- Sphinx (Python)
- JSDoc (JavaScript)
- JSON Schema documentation generators

### Appendix C: References

- Phase 1: Component Extraction (Complete)
- Phase 2: Interface Standardization (Complete)
- Phase 3: Shared Core Extraction (This Document)
- Phase 4: Testing Framework (Pending)
- Phase 5: Integration & Validation (Pending)

---

**Document Control:**
- **Version:** 1.0.0
- **Last Updated:** 2025-10-02
- **Next Review:** After Phase 3 completion
- **Status:** Draft - Awaiting Review
