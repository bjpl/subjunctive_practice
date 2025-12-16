import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import './Leaderboard.css';

// Types
interface LeaderboardEntry {
  id: number;
  user_id: number;
  username: string;
  avatar_url?: string;
  full_name?: string;
  score_type: 'xp' | 'accuracy' | 'streak' | 'exercises_completed';
  score: number;
  rank: number;
  achieved_at: string;
  period: 'daily' | 'weekly' | 'monthly' | 'all_time';
  is_current_user: boolean;
}

interface LeaderboardData {
  score_type: string;
  period: string;
  entries: LeaderboardEntry[];
  total_participants: number;
  last_updated: string;
  period_start: string;
  period_end: string;
}

interface UserRankInfo {
  user_id: number;
  username: string;
  score_type: string;
  period: string;
  score: number;
  rank: number;
  total_participants: number;
  percentile: number;
  nearby_users: LeaderboardEntry[];
}

type ScoreType = 'xp' | 'accuracy' | 'streak' | 'exercises_completed';
type Period = 'daily' | 'weekly' | 'monthly' | 'all_time';

// API Service
class LeaderboardAPI {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  private getHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  async getLeaderboard(
    scoreType: ScoreType,
    period: Period = 'all_time',
    limit: number = 10
  ): Promise<LeaderboardData> {
    const response = await fetch(
      `${this.baseUrl}/api/leaderboard/${scoreType}?period=${period}&limit=${limit}`,
      { headers: this.getHeaders() }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch leaderboard');
    }

    return response.json();
  }

  async getMyRank(scoreType: ScoreType, period: Period = 'all_time'): Promise<UserRankInfo> {
    const response = await fetch(
      `${this.baseUrl}/api/leaderboard/${scoreType}/me?period=${period}`,
      { headers: this.getHeaders() }
    );

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('You need to complete some activities to appear on the leaderboard');
      }
      throw new Error('Failed to fetch rank');
    }

    return response.json();
  }

  async getAllLeaderboardsSummary(period: Period = 'all_time'): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/leaderboard/all-types/summary?period=${period}`,
      { headers: this.getHeaders() }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch leaderboard summary');
    }

    return response.json();
  }
}

// Main Component
export const Leaderboard: React.FC = () => {
  const [scoreType, setScoreType] = useState<ScoreType>('xp');
  const [period, setPeriod] = useState<Period>('all_time');
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardData | null>(null);
  const [userRank, setUserRank] = useState<UserRankInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showNearbyUsers, setShowNearbyUsers] = useState(false);

  const api = new LeaderboardAPI();

  // Fetch leaderboard data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        // Fetch main leaderboard
        const data = await api.getLeaderboard(scoreType, period, 10);
        setLeaderboardData(data);

        // Try to fetch user's rank
        try {
          const rank = await api.getMyRank(scoreType, period);
          setUserRank(rank);
        } catch (err) {
          // User might not have data yet
          setUserRank(null);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load leaderboard');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [scoreType, period]);

  // Score type display names
  const scoreTypeNames: Record<ScoreType, string> = {
    xp: 'XP Points',
    accuracy: 'Accuracy',
    streak: 'Streak Days',
    exercises_completed: 'Exercises Completed',
  };

  // Period display names
  const periodNames: Record<Period, string> = {
    daily: 'Today',
    weekly: 'This Week',
    monthly: 'This Month',
    all_time: 'All Time',
  };

  // Get medal emoji for rank
  const getMedalEmoji = (rank: number): string => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return '';
  };

  // Format score based on type
  const formatScore = (score: number, type: ScoreType): string => {
    if (type === 'accuracy') {
      return `${score.toFixed(1)}%`;
    }
    if (type === 'streak') {
      return `${Math.floor(score)} days`;
    }
    return Math.floor(score).toLocaleString();
  };

  // Render loading state
  if (loading) {
    return (
      <Card className="leaderboard-card">
        <div className="leaderboard-loading">
          <div className="spinner" />
          <p>Loading leaderboard...</p>
        </div>
      </Card>
    );
  }

  // Render error state
  if (error) {
    return (
      <Card className="leaderboard-card">
        <div className="leaderboard-error">
          <p>⚠️ {error}</p>
          <button onClick={() => window.location.reload()} className="retry-button">
            Retry
          </button>
        </div>
      </Card>
    );
  }

  return (
    <Card className="leaderboard-card">
      {/* Header */}
      <div className="leaderboard-header">
        <h2 className="leaderboard-title">🏆 Leaderboard</h2>
        <p className="leaderboard-subtitle">
          {leaderboardData?.total_participants || 0} participants
        </p>
      </div>

      {/* Score Type Tabs */}
      <div className="score-type-tabs">
        {Object.entries(scoreTypeNames).map(([type, name]) => (
          <button
            key={type}
            className={`tab-button ${scoreType === type ? 'active' : ''}`}
            onClick={() => setScoreType(type as ScoreType)}
          >
            {name}
          </button>
        ))}
      </div>

      {/* Period Filter */}
      <div className="period-filter">
        {Object.entries(periodNames).map(([periodKey, periodName]) => (
          <button
            key={periodKey}
            className={`period-button ${period === periodKey ? 'active' : ''}`}
            onClick={() => setPeriod(periodKey as Period)}
          >
            {periodName}
          </button>
        ))}
      </div>

      {/* User's Rank Card (if available) */}
      {userRank && !showNearbyUsers && (
        <div className="user-rank-card">
          <div className="user-rank-content">
            <div className="rank-badge">#{userRank.rank}</div>
            <div className="rank-info">
              <p className="rank-label">Your Rank</p>
              <p className="rank-score">{formatScore(userRank.score, scoreType)}</p>
              <p className="rank-percentile">Top {userRank.percentile.toFixed(1)}%</p>
            </div>
          </div>
          <button
            className="view-nearby-button"
            onClick={() => setShowNearbyUsers(!showNearbyUsers)}
          >
            View Nearby Users
          </button>
        </div>
      )}

      {/* Nearby Users View */}
      {showNearbyUsers && userRank && (
        <div className="nearby-users-section">
          <div className="nearby-header">
            <h3>Users Near You</h3>
            <button className="close-nearby" onClick={() => setShowNearbyUsers(false)}>
              ✕
            </button>
          </div>
          <div className="leaderboard-list">
            {userRank.nearby_users.map((entry) => (
              <div
                key={entry.id}
                className={`leaderboard-entry ${entry.is_current_user ? 'current-user' : ''}`}
              >
                <div className="entry-rank">
                  <span className="rank-number">#{entry.rank}</span>
                  {getMedalEmoji(entry.rank) && (
                    <span className="medal">{getMedalEmoji(entry.rank)}</span>
                  )}
                </div>

                <div className="entry-user">
                  <div className="user-avatar">
                    {entry.avatar_url ? (
                      <img src={entry.avatar_url} alt={entry.username} />
                    ) : (
                      <div className="avatar-placeholder">
                        {entry.username.charAt(0).toUpperCase()}
                      </div>
                    )}
                  </div>
                  <div className="user-info">
                    <p className="username">
                      {entry.full_name || entry.username}
                      {entry.is_current_user && <span className="you-badge">You</span>}
                    </p>
                    <p className="user-id">@{entry.username}</p>
                  </div>
                </div>

                <div className="entry-score">
                  <p className="score-value">{formatScore(entry.score, scoreType)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Leaderboard List */}
      {!showNearbyUsers && (
        <div className="leaderboard-list">
          {leaderboardData?.entries.length === 0 ? (
            <div className="empty-state">
              <p>No data available for this period yet.</p>
              <p className="empty-hint">Be the first to appear on the leaderboard!</p>
            </div>
          ) : (
            leaderboardData?.entries.map((entry, index) => (
              <div
                key={entry.id}
                className={`leaderboard-entry ${entry.is_current_user ? 'current-user' : ''} ${
                  index < 3 ? 'top-three' : ''
                }`}
              >
                <div className="entry-rank">
                  <span className="rank-number">#{entry.rank}</span>
                  {getMedalEmoji(entry.rank) && (
                    <span className="medal">{getMedalEmoji(entry.rank)}</span>
                  )}
                </div>

                <div className="entry-user">
                  <div className="user-avatar">
                    {entry.avatar_url ? (
                      <img src={entry.avatar_url} alt={entry.username} />
                    ) : (
                      <div className="avatar-placeholder">
                        {entry.username.charAt(0).toUpperCase()}
                      </div>
                    )}
                  </div>
                  <div className="user-info">
                    <p className="username">
                      {entry.full_name || entry.username}
                      {entry.is_current_user && <span className="you-badge">You</span>}
                    </p>
                    <p className="user-id">@{entry.username}</p>
                  </div>
                </div>

                <div className="entry-score">
                  <p className="score-value">{formatScore(entry.score, scoreType)}</p>
                  <p className="score-date">
                    {new Date(entry.achieved_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Footer */}
      <div className="leaderboard-footer">
        <p className="last-updated">
          Last updated: {leaderboardData ? new Date(leaderboardData.last_updated).toLocaleTimeString() : 'N/A'}
        </p>
      </div>
    </Card>
  );
};

export default Leaderboard;
