# SDK Quick Start Guide

Get started with the Spanish Subjunctive Practice API SDKs in minutes.

## Choose Your Language

We provide official SDKs for:
- **Python** - Type-safe with async/await support
- **TypeScript** - Full type definitions with React hooks

## Python SDK

### Installation

```bash
pip install subjunctive-practice-sdk
```

### Quick Example

```python
from subjunctive_practice import SubjunctivePracticeClient, ApiKeyAuth

# Initialize client
client = SubjunctivePracticeClient(auth=ApiKeyAuth("your-api-key"))

# Create session and generate exercise
session = client.create_session(user_id="student_123")
exercise = client.generate_practice(
    session_id=session.session_id,
    difficulty=2,
    tense="present_subjunctive"
)

print(f"Prompt: {exercise.prompt}")

# Submit answer
result = client.submit_answer({
    "task_id": exercise.task_id,
    "session_id": session.session_id,
    "answer": "estudie",
    "response_time": 12.5
})

print(f"Correct: {result['correct']}")
print(f"Feedback: {result['feedback']}")

client.close()
```

### Async Example

```python
import asyncio
from subjunctive_practice import AsyncSubjunctivePracticeClient, ApiKeyAuth

async def main():
    async with AsyncSubjunctivePracticeClient(auth=ApiKeyAuth("your-api-key")) as client:
        session = await client.create_session(user_id="student_123")
        exercise = await client.generate_practice(
            session_id=session.session_id,
            difficulty=2
        )
        print(f"Exercise: {exercise.prompt}")

asyncio.run(main())
```

## TypeScript SDK

### Installation

```bash
npm install @subjunctive-practice/sdk
# or
yarn add @subjunctive-practice/sdk
```

### Quick Example

```typescript
import { SubjunctivePracticeClient } from '@subjunctive-practice/sdk';

// Initialize client
const client = new SubjunctivePracticeClient({
  apiKey: 'your-api-key'
});

// Create session and generate exercise
const session = await client.createSession('student_123');
const exercise = await client.generatePractice({
  sessionId: session.session_id,
  difficulty: 2,
  tense: 'present_subjunctive'
});

console.log(`Prompt: ${exercise.prompt}`);

// Submit answer
const result = await client.submitAnswer({
  task_id: exercise.task_id,
  session_id: session.session_id,
  answer: 'estudie',
  response_time: 12.5
});

console.log(`Correct: ${result.correct}`);
console.log(`Feedback: ${result.feedback}`);
```

### React Hooks Example

```tsx
import {
  useSubjunctivePracticeClient,
  useCreateSession,
  useGeneratePractice,
  useSubmitAnswer
} from '@subjunctive-practice/sdk/react';

function PracticeComponent() {
  const client = useSubjunctivePracticeClient({ apiKey: 'your-api-key' });
  const { data: session, mutate: createSession } = useCreateSession(client);
  const { data: exercise, mutate: generateExercise } = useGeneratePractice(client);
  const { data: result, loading, mutate: submitAnswer } = useSubmitAnswer(client);

  const handleStart = async () => {
    await createSession('student_123');
  };

  const handleGenerate = async () => {
    if (session) {
      await generateExercise({ sessionId: session.session_id, difficulty: 2 });
    }
  };

  const handleSubmit = async () => {
    if (exercise && session) {
      await submitAnswer({
        task_id: exercise.task_id,
        session_id: session.session_id,
        answer: 'estudie',
        response_time: 12.5
      });
    }
  };

  return (
    <div>
      <button onClick={handleStart}>Start</button>
      <button onClick={handleGenerate}>Generate</button>
      {exercise && (
        <div>
          <p>{exercise.prompt}</p>
          <button onClick={handleSubmit}>Submit</button>
        </div>
      )}
      {loading && <p>Loading...</p>}
      {result && <p>Feedback: {result.feedback}</p>}
    </div>
  );
}
```

## AI-Powered Features

Both SDKs support advanced AI features:

### Python

```python
from subjunctive_practice import (
    AIExerciseRequest,
    DifficultyLevel,
    SubjunctiveTense
)

exercise = client.generate_ai_exercise(
    AIExerciseRequest(
        difficulty=DifficultyLevel.INTERMEDIATE,
        tense=SubjunctiveTense.PRESENT,
        topic="travel",
        student_id="student_123"
    )
)

print(f"AI Exercise: {exercise.sentence}")
print(f"Explanation: {exercise.explanation}")
```

### TypeScript

```typescript
import { DifficultyLevel, SubjunctiveTense } from '@subjunctive-practice/sdk';

const exercise = await client.generateAIExercise({
  difficulty: DifficultyLevel.INTERMEDIATE,
  tense: SubjunctiveTense.PRESENT,
  topic: 'travel',
  student_id: 'student_123'
});

console.log(`AI Exercise: ${exercise.sentence}`);
console.log(`Explanation: ${exercise.explanation}`);
```

## Error Handling

### Python

```python
from subjunctive_practice import (
    AuthenticationError,
    ValidationError,
    RateLimitError
)

try:
    exercise = client.generate_ai_exercise(request)
except AuthenticationError:
    print("Authentication failed - check your API key")
except ValidationError as e:
    print(f"Invalid request: {e.message}")
    print(f"Details: {e.details}")
except RateLimitError as e:
    print(f"Rate limited - retry after {e.retry_after} seconds")
```

### TypeScript

```typescript
import {
  AuthenticationError,
  ValidationError,
  RateLimitError
} from '@subjunctive-practice/sdk';

try {
  const exercise = await client.generateAIExercise(request);
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Authentication failed');
  } else if (error instanceof ValidationError) {
    console.error('Invalid request:', error.details);
  } else if (error instanceof RateLimitError) {
    console.error(`Retry after ${error.retryAfter} seconds`);
  }
}
```

## Next Steps

- **Python SDK**: See [/sdk/python/README.md](../../sdk/python/README.md)
- **TypeScript SDK**: See [/sdk/typescript/README.md](../../sdk/typescript/README.md)
- **API Documentation**: https://docs.subjunctive-practice.com
- **Examples**: Check the `/examples` directory in each SDK

## Getting an API Key

1. Visit https://api.subjunctive-practice.com/signup
2. Create an account
3. Navigate to API Keys in your dashboard
4. Generate a new API key
5. Keep it secure - never commit it to version control!

## Support

- **Email**: support@subjunctive-practice.com
- **Issues**: GitHub repository issues
- **Documentation**: https://docs.subjunctive-practice.com
