"""
AI Usage tracking model for database persistence.

This model stores AI API usage records including token counts and costs
for monitoring and analysis purposes.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class AIUsageRecord(Base):
    """
    Tracks individual AI API usage events.

    Stores token consumption and cost data for:
    - Cost monitoring and budgeting
    - Usage analytics and optimization
    - User-level tracking
    - Request type analysis
    """
    __tablename__ = "ai_usage_records"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # User association (nullable for anonymous/system requests)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Request metadata
    request_type = Column(String(50), nullable=False, index=True)  # feedback, insights, hint, etc.
    model = Column(String(100), nullable=False, default="claude-3-5-sonnet-20241022")

    # Token usage
    input_tokens = Column(Integer, nullable=False, default=0)
    output_tokens = Column(Integer, nullable=False, default=0)

    # Cost tracking (in USD)
    estimated_cost = Column(Float, nullable=False, default=0.0)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])

    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'created_at'),
        Index('idx_type_date', 'request_type', 'created_at'),
        Index('idx_date_cost', 'created_at', 'estimated_cost'),
    )

    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)."""
        return self.input_tokens + self.output_tokens

    def __repr__(self):
        return (
            f"<AIUsageRecord(id={self.id}, user_id={self.user_id}, "
            f"type='{self.request_type}', tokens={self.total_tokens}, "
            f"cost=${self.estimated_cost:.4f})>"
        )
