# Contributing to Spanish Subjunctive Practice

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment details** (OS, browser, versions)
- **Screenshots** (if applicable)
- **Error messages and logs**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear use case**
- **Expected benefits**
- **Possible implementation approach**
- **Examples from other projects**

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Setup

See [Getting Started Guide](./getting-started.md) for detailed setup instructions.

Quick start:
```bash
git clone <your-fork>
cd subjunctive_practice
npm install
pip install -r requirements.txt
pre-commit install
```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Docstrings for all public functions

```python
def calculate_next_review(
    item: PracticeItem,
    quality: int,
    current_time: datetime
) -> PracticeItem:
    """
    Calculate next review date using SM-2 algorithm.

    Args:
        item: Practice item to update
        quality: Response quality (0-5)
        current_time: Current timestamp

    Returns:
        Updated practice item with new review date
    """
    # Implementation
    return item
```

### TypeScript/JavaScript

- Use TypeScript for all new code
- Follow Airbnb style guide
- Use ESLint and Prettier
- Functional programming preferred

```typescript
interface ExerciseOptions {
  difficulty: DifficultyLevel;
  tense: SubjunctiveTense;
  count: number;
}

function generateExercises(options: ExerciseOptions): Exercise[] {
  // Implementation
  return [];
}
```

### Git Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Example:
```
feat(exercises): add mood contrast exercise type

Implement new exercise type that helps users distinguish
between indicative and subjunctive moods in similar contexts.

Closes #123
```

## Testing Requirements

All contributions must include tests:

### Python Tests
```python
import pytest
from backend.services.exercise_service import ExerciseService

def test_generate_exercise_with_difficulty():
    service = ExerciseService()
    exercise = service.generate(difficulty='advanced')

    assert exercise.difficulty == 'advanced'
    assert exercise.verb.difficulty_level == 'advanced'
```

### TypeScript Tests
```typescript
import { describe, it, expect } from 'vitest';
import { ConjugationEngine } from '../conjugation';

describe('ConjugationEngine', () => {
  it('should conjugate regular -ar verbs correctly', () => {
    const engine = new ConjugationEngine();
    const result = engine.conjugate('hablar', 'present_subjunctive', 'yo');

    expect(result).toBe('hable');
  });
});
```

Run tests before submitting:
```bash
npm test
npm run test:coverage  # Ensure >80% coverage
```

## Documentation

- Update documentation for all new features
- Include code examples
- Add JSDoc/docstrings
- Update API documentation if endpoints change

## Review Process

1. **Automated Checks**: CI runs tests, linting, type checking
2. **Code Review**: Maintainer reviews code quality and design
3. **Testing**: Verify functionality works as expected
4. **Documentation**: Ensure docs are updated
5. **Approval**: Maintainer approves and merges

## Release Process

Releases follow semantic versioning:

- **Major**: Breaking changes
- **Minor**: New features (backwards compatible)
- **Patch**: Bug fixes

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Questions? Contact the maintainers or open a discussion on GitHub.
