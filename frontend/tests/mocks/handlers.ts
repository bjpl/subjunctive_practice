import { http, HttpResponse } from 'msw';

// Match the API client base URL exactly
const API_BASE_URL = 'http://localhost:8000/api';

export const handlers = [
  // Auth endpoints
  http.post(`${API_BASE_URL}/auth/register`, async ({ request }) => {
    const body = await request.json() as { email: string; username: string; password: string };

    if (body.email === 'existing@example.com') {
      return HttpResponse.json(
        { detail: 'User already exists' },
        { status: 400 }
      );
    }

    return HttpResponse.json({
      access_token: 'mock-token-123',
      user: {
        id: 1,
        email: body.email,
        username: body.username,
        createdAt: new Date().toISOString(),
      },
    });
  }),

  http.post(`${API_BASE_URL}/auth/login`, async ({ request }) => {
    const body = await request.json() as { email: string; password: string };

    // More specific check for wrong credentials
    if (body.email === 'wrong@example.com' && body.password === 'wrongpass') {
      return HttpResponse.json(
        { detail: 'Invalid credentials' },
        { status: 401 }
      );
    }

    return HttpResponse.json({
      access_token: 'mock-token-123',
      user: {
        id: 1,
        email: body.email,
        username: 'testuser',
        createdAt: new Date().toISOString(),
      },
    });
  }),

  http.post(`${API_BASE_URL}/auth/logout`, () => {
    return HttpResponse.json({ message: 'Logged out successfully' });
  }),

  // Exercise endpoints
  http.get(`${API_BASE_URL}/exercises`, ({ request }) => {
    const url = new URL(request.url);
    const difficulty = url.searchParams.get('difficulty');
    const tense = url.searchParams.get('tense');

    const exercises = [
      {
        id: 1,
        verb: 'hablar',
        subject: 'yo',
        tense: 'present',
        difficulty: 'beginner',
        english: 'I speak',
        correctAnswer: 'hable',
      },
      {
        id: 2,
        verb: 'comer',
        subject: 'tú',
        tense: 'present',
        difficulty: 'intermediate',
        english: 'you eat',
        correctAnswer: 'comas',
      },
    ].filter((ex) => {
      if (difficulty && ex.difficulty !== difficulty) return false;
      if (tense && ex.tense !== tense) return false;
      return true;
    });

    return HttpResponse.json({ exercises, total: exercises.length });
  }),

  http.post(`${API_BASE_URL}/exercises/:id/submit`, async ({ params, request }) => {
    const body = await request.json() as { answer: string };
    const { id } = params;

    const correct = body.answer.toLowerCase() === 'hable' || body.answer.toLowerCase() === 'comas';

    return HttpResponse.json({
      correct,
      correctAnswer: id === '1' ? 'hable' : 'comas',
      explanation: correct
        ? 'Correct! Great job!'
        : `The correct answer is ${id === '1' ? 'hable' : 'comas'}`,
      points: correct ? 10 : 0,
    });
  }),

  // Progress endpoints
  http.get(`${API_BASE_URL}/progress/stats`, () => {
    return HttpResponse.json({
      totalExercises: 150,
      correctAnswers: 120,
      accuracy: 80,
      currentStreak: 5,
      longestStreak: 12,
      totalPoints: 1200,
      level: 5,
      achievements: [
        { id: 1, name: 'First Steps', description: 'Complete 10 exercises', unlocked: true },
        { id: 2, name: 'Week Warrior', description: '7 day streak', unlocked: true },
        { id: 3, name: 'Perfect Score', description: '100% on 5 exercises', unlocked: false },
      ],
    });
  }),

  http.get(`${API_BASE_URL}/progress/history`, () => {
    return HttpResponse.json({
      sessions: [
        {
          id: 1,
          date: '2024-10-01',
          exercises: 10,
          correctAnswers: 8,
          accuracy: 80,
          points: 80,
          duration: 600,
        },
        {
          id: 2,
          date: '2024-10-02',
          exercises: 15,
          correctAnswers: 14,
          accuracy: 93.3,
          points: 140,
          duration: 900,
        },
      ],
    });
  }),

  http.get(`${API_BASE_URL}/progress/weak-areas`, () => {
    return HttpResponse.json({
      weakAreas: [
        { tense: 'imperfect', accuracy: 65, totalAttempts: 40 },
        { tense: 'future', accuracy: 70, totalAttempts: 30 },
      ],
    });
  }),

  // Settings endpoints
  http.get(`${API_BASE_URL}/settings`, () => {
    return HttpResponse.json({
      notifications: true,
      dailyGoal: 20,
      difficulty: 'intermediate',
      preferredTenses: ['present', 'imperfect'],
      theme: 'light',
    });
  }),

  http.patch(`${API_BASE_URL}/settings`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      ...body,
      message: 'Settings updated successfully',
    });
  }),
];
