"""
User settings routes: manage user preferences and configuration.
"""

from typing import Dict, Any, Literal
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from core.security import get_current_active_user
from core.database import get_db_session
from models.settings import UserSettings as DBUserSettings
from models.user import User
from pydantic import BaseModel, Field


# Settings schemas
class NotificationSettings(BaseModel):
    """Notification preferences."""
    email: bool = True
    push: bool = False
    streakReminders: bool = True


class PracticeSettings(BaseModel):
    """Practice session preferences."""
    dailyGoal: int = Field(default=10, ge=1, le=100, description="Number of exercises per day")
    autoAdvance: bool = True
    showHints: bool = True
    showExplanations: bool = True


class AccessibilitySettings(BaseModel):
    """Accessibility preferences."""
    fontSize: Literal['small', 'medium', 'large'] = 'medium'
    highContrast: bool = False
    reduceMotion: bool = False


class LanguageSettings(BaseModel):
    """Language preferences."""
    interface: str = Field(default='en', description="Interface language code")
    practice: str = Field(default='es', description="Practice language code")


class UserSettings(BaseModel):
    """Complete user settings."""
    notifications: NotificationSettings = NotificationSettings()
    practice: PracticeSettings = PracticeSettings()
    accessibility: AccessibilitySettings = AccessibilitySettings()
    language: LanguageSettings = LanguageSettings()


class SettingsResponse(BaseModel):
    """Response schema for settings with metadata."""
    user_id: str
    settings: UserSettings
    last_updated: datetime
    version: int = 1


router = APIRouter(prefix="/settings", tags=["Settings"])


def get_user_db_id(db: Session, username: str) -> int:
    """Get database user ID from username (JWT subject)."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.id


def load_user_settings(db: Session, user_db_id: int) -> DBUserSettings:
    """Load user settings from database, creating defaults if not found."""
    settings = db.query(DBUserSettings).filter(DBUserSettings.user_id == user_db_id).first()

    if not settings:
        # Create default settings for new users
        settings = DBUserSettings(
            user_id=user_db_id,
            notifications={
                "email": True,
                "push": False,
                "streakReminders": True
            },
            practice={
                "dailyGoal": 10,
                "autoAdvance": True,
                "showHints": True,
                "showExplanations": True
            },
            accessibility={
                "fontSize": "medium",
                "highContrast": False,
                "reduceMotion": False
            },
            language={
                "interface": "en",
                "practice": "es"
            },
            version=1
        )
        try:
            db.add(settings)
            db.commit()
            db.refresh(settings)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create default settings: {str(e)}"
            )

    return settings


def save_user_settings(db: Session, user_db_id: int, settings: UserSettings) -> DBUserSettings:
    """Save or update user settings in database."""
    db_settings = db.query(DBUserSettings).filter(DBUserSettings.user_id == user_db_id).first()

    if db_settings:
        # Update existing settings
        db_settings.notifications = settings.notifications.model_dump()
        db_settings.practice = settings.practice.model_dump()
        db_settings.accessibility = settings.accessibility.model_dump()
        db_settings.language = settings.language.model_dump()
        db_settings.version += 1
        db_settings.updated_at = datetime.utcnow()
    else:
        # Create new settings
        db_settings = DBUserSettings(
            user_id=user_db_id,
            notifications=settings.notifications.model_dump(),
            practice=settings.practice.model_dump(),
            accessibility=settings.accessibility.model_dump(),
            language=settings.language.model_dump(),
            version=1
        )
        db.add(db_settings)

    try:
        db.commit()
        db.refresh(db_settings)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save settings: {str(e)}"
        )

    return db_settings


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get current user's settings.

    Returns all user preferences including:
    - Notification settings (email, push, streak reminders)
    - Practice settings (daily goal, auto-advance, hints, explanations)
    - Accessibility settings (font size, high contrast, reduced motion)
    - Language settings (interface and practice languages)

    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)
    db_settings = load_user_settings(db, user_db_id)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    settings: UserSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Update all user settings.

    Replaces all settings with the provided values.
    Use PATCH endpoints to update specific sections only.

    Request body should include:
    - **notifications**: Email, push, and streak reminder preferences
    - **practice**: Daily goal, auto-advance, hints, and explanations
    - **accessibility**: Font size, high contrast, and reduced motion
    - **language**: Interface and practice language codes

    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)

    # Validate settings
    if settings.practice.dailyGoal < 1 or settings.practice.dailyGoal > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Daily goal must be between 1 and 100"
        )

    if settings.accessibility.fontSize not in ['small', 'medium', 'large']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Font size must be 'small', 'medium', or 'large'"
        )

    # Save settings
    db_settings = save_user_settings(db, user_db_id, settings)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )


@router.patch("/notifications", response_model=SettingsResponse)
async def update_notification_settings(
    notifications: NotificationSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Update only notification settings.

    Request body:
    - **email**: Enable/disable email notifications
    - **push**: Enable/disable push notifications
    - **streakReminders**: Enable/disable streak reminder notifications

    Other settings remain unchanged.
    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)
    db_settings = load_user_settings(db, user_db_id)

    # Update only notification settings
    current_settings = UserSettings(
        notifications=NotificationSettings(**db_settings.notifications),
        practice=PracticeSettings(**db_settings.practice),
        accessibility=AccessibilitySettings(**db_settings.accessibility),
        language=LanguageSettings(**db_settings.language)
    )
    current_settings.notifications = notifications

    # Save updated settings
    db_settings = save_user_settings(db, user_db_id, current_settings)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )


@router.patch("/practice", response_model=SettingsResponse)
async def update_practice_settings(
    practice: PracticeSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Update only practice session settings.

    Request body:
    - **dailyGoal**: Number of exercises per day (1-100)
    - **autoAdvance**: Automatically advance to next exercise
    - **showHints**: Show hints during exercises
    - **showExplanations**: Show explanations after answers

    Other settings remain unchanged.
    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)

    # Validate daily goal
    if practice.dailyGoal < 1 or practice.dailyGoal > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Daily goal must be between 1 and 100"
        )

    db_settings = load_user_settings(db, user_db_id)

    # Update only practice settings
    current_settings = UserSettings(
        notifications=NotificationSettings(**db_settings.notifications),
        practice=PracticeSettings(**db_settings.practice),
        accessibility=AccessibilitySettings(**db_settings.accessibility),
        language=LanguageSettings(**db_settings.language)
    )
    current_settings.practice = practice

    # Save updated settings
    db_settings = save_user_settings(db, user_db_id, current_settings)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )


@router.patch("/accessibility", response_model=SettingsResponse)
async def update_accessibility_settings(
    accessibility: AccessibilitySettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Update only accessibility settings.

    Request body:
    - **fontSize**: 'small', 'medium', or 'large'
    - **highContrast**: Enable/disable high contrast mode
    - **reduceMotion**: Enable/disable reduced motion mode

    Other settings remain unchanged.
    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)

    # Validate font size
    if accessibility.fontSize not in ['small', 'medium', 'large']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Font size must be 'small', 'medium', or 'large'"
        )

    db_settings = load_user_settings(db, user_db_id)

    # Update only accessibility settings
    current_settings = UserSettings(
        notifications=NotificationSettings(**db_settings.notifications),
        practice=PracticeSettings(**db_settings.practice),
        accessibility=AccessibilitySettings(**db_settings.accessibility),
        language=LanguageSettings(**db_settings.language)
    )
    current_settings.accessibility = accessibility

    # Save updated settings
    db_settings = save_user_settings(db, user_db_id, current_settings)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )


@router.patch("/language", response_model=SettingsResponse)
async def update_language_settings(
    language: LanguageSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Update only language settings.

    Request body:
    - **interface**: Interface language code (e.g., 'en', 'es', 'fr')
    - **practice**: Practice language code (e.g., 'es', 'fr', 'de')

    Other settings remain unchanged.
    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)

    # Validate language codes (basic validation)
    if not language.interface or len(language.interface) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid interface language code"
        )

    if not language.practice or len(language.practice) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid practice language code"
        )

    db_settings = load_user_settings(db, user_db_id)

    # Update only language settings
    current_settings = UserSettings(
        notifications=NotificationSettings(**db_settings.notifications),
        practice=PracticeSettings(**db_settings.practice),
        accessibility=AccessibilitySettings(**db_settings.accessibility),
        language=LanguageSettings(**db_settings.language)
    )
    current_settings.language = language

    # Save updated settings
    db_settings = save_user_settings(db, user_db_id, current_settings)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def reset_settings(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Reset all settings to defaults.

    This will delete the user's settings record and create defaults on next access.
    This action cannot be undone.

    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)

    try:
        # Delete existing settings
        db.query(DBUserSettings).filter(DBUserSettings.user_id == user_db_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset settings: {str(e)}"
        )

    return None


@router.get("/export", response_model=Dict[str, Any])
async def export_settings(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Export all user settings as JSON.

    Useful for backup or migration purposes.
    Returns the complete settings data including metadata.

    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)
    db_settings = load_user_settings(db, user_db_id)

    return {
        "export_date": datetime.utcnow().isoformat(),
        "user_id": username,
        "settings": {
            "notifications": db_settings.notifications,
            "practice": db_settings.practice,
            "accessibility": db_settings.accessibility,
            "language": db_settings.language
        },
        "metadata": {
            "last_updated": db_settings.updated_at.isoformat(),
            "version": db_settings.version
        }
    }


@router.post("/import", response_model=SettingsResponse)
async def import_settings(
    settings_data: UserSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Import settings from exported JSON.

    Useful for restoring settings from backup or migrating from another account.
    This will replace all current settings.

    Request body should contain the settings object from an export.
    Requires authentication.
    """
    username = current_user["sub"]
    user_db_id = get_user_db_id(db, username)

    # Validate and save settings
    db_settings = save_user_settings(db, user_db_id, settings_data)

    return SettingsResponse(
        user_id=username,
        settings=UserSettings(
            notifications=NotificationSettings(**db_settings.notifications),
            practice=PracticeSettings(**db_settings.practice),
            accessibility=AccessibilitySettings(**db_settings.accessibility),
            language=LanguageSettings(**db_settings.language)
        ),
        last_updated=db_settings.updated_at,
        version=db_settings.version
    )
