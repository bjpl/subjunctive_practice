"""
User settings routes: manage user preferences and configuration.
"""

from typing import Dict, Any, Literal, Optional
from fastapi import APIRouter, HTTPException, status, Depends
import json
from pathlib import Path
from datetime import datetime

from core.security import get_current_active_user
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


# File-based settings storage
SETTINGS_DIR = Path("user_data/settings")


def get_settings_file(user_id: str) -> Path:
    """Get settings file path for a user."""
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    return SETTINGS_DIR / f"settings_{user_id}.json"


def load_user_settings(user_id: str) -> Dict[str, Any]:
    """Load user settings from file."""
    settings_file = get_settings_file(user_id)

    if settings_file.exists():
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # Return default settings for new users
    return {
        "user_id": user_id,
        "settings": UserSettings().model_dump(),
        "last_updated": datetime.utcnow().isoformat(),
        "version": 1
    }


def save_user_settings(user_id: str, settings: UserSettings) -> Dict[str, Any]:
    """Save user settings to file."""
    settings_file = get_settings_file(user_id)

    # Load existing data to preserve version and increment
    existing_data = load_user_settings(user_id)
    version = existing_data.get("version", 0) + 1

    data = {
        "user_id": user_id,
        "settings": settings.model_dump(),
        "last_updated": datetime.utcnow().isoformat(),
        "version": version
    }

    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    user_id = current_user["sub"]
    data = load_user_settings(user_id)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    settings: UserSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    user_id = current_user["sub"]

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
    data = save_user_settings(user_id, settings)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


@router.patch("/notifications", response_model=SettingsResponse)
async def update_notification_settings(
    notifications: NotificationSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    user_id = current_user["sub"]
    data = load_user_settings(user_id)

    # Update only notification settings
    current_settings = UserSettings(**data["settings"])
    current_settings.notifications = notifications

    # Save updated settings
    data = save_user_settings(user_id, current_settings)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


@router.patch("/practice", response_model=SettingsResponse)
async def update_practice_settings(
    practice: PracticeSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    user_id = current_user["sub"]

    # Validate daily goal
    if practice.dailyGoal < 1 or practice.dailyGoal > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Daily goal must be between 1 and 100"
        )

    data = load_user_settings(user_id)

    # Update only practice settings
    current_settings = UserSettings(**data["settings"])
    current_settings.practice = practice

    # Save updated settings
    data = save_user_settings(user_id, current_settings)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


@router.patch("/accessibility", response_model=SettingsResponse)
async def update_accessibility_settings(
    accessibility: AccessibilitySettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    user_id = current_user["sub"]

    # Validate font size
    if accessibility.fontSize not in ['small', 'medium', 'large']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Font size must be 'small', 'medium', or 'large'"
        )

    data = load_user_settings(user_id)

    # Update only accessibility settings
    current_settings = UserSettings(**data["settings"])
    current_settings.accessibility = accessibility

    # Save updated settings
    data = save_user_settings(user_id, current_settings)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


@router.patch("/language", response_model=SettingsResponse)
async def update_language_settings(
    language: LanguageSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Update only language settings.

    Request body:
    - **interface**: Interface language code (e.g., 'en', 'es', 'fr')
    - **practice**: Practice language code (e.g., 'es', 'fr', 'de')

    Other settings remain unchanged.
    Requires authentication.
    """
    user_id = current_user["sub"]

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

    data = load_user_settings(user_id)

    # Update only language settings
    current_settings = UserSettings(**data["settings"])
    current_settings.language = language

    # Save updated settings
    data = save_user_settings(user_id, current_settings)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def reset_settings(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Reset all settings to defaults.

    This will delete the user's settings file and revert to default values.
    This action cannot be undone.

    Requires authentication.
    """
    user_id = current_user["sub"]
    settings_file = get_settings_file(user_id)

    if settings_file.exists():
        settings_file.unlink()

    return None


@router.get("/export", response_model=Dict[str, Any])
async def export_settings(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Export all user settings as JSON.

    Useful for backup or migration purposes.
    Returns the complete settings data including metadata.

    Requires authentication.
    """
    user_id = current_user["sub"]
    data = load_user_settings(user_id)

    return {
        "export_date": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "settings": data["settings"],
        "metadata": {
            "last_updated": data["last_updated"],
            "version": data["version"]
        }
    }


@router.post("/import", response_model=SettingsResponse)
async def import_settings(
    settings_data: UserSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Import settings from exported JSON.

    Useful for restoring settings from backup or migrating from another account.
    This will replace all current settings.

    Request body should contain the settings object from an export.
    Requires authentication.
    """
    user_id = current_user["sub"]

    # Validate and save settings
    data = save_user_settings(user_id, settings_data)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )


# Additional endpoint for updating notification preferences (alias to /notifications)
@router.put("/users/me/notifications", response_model=SettingsResponse)
async def update_user_notification_preferences(
    notifications: NotificationSettings,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Update user notification preferences.

    Alternative endpoint path for notification preferences.
    This is an alias to PATCH /settings/notifications for convenience.

    Request body:
    - **email**: Enable/disable email notifications
    - **push**: Enable/disable push notifications
    - **streakReminders**: Enable/disable streak reminder notifications

    Requires authentication.
    """
    user_id = current_user["sub"]
    data = load_user_settings(user_id)

    # Update only notification settings
    current_settings = UserSettings(**data["settings"])
    current_settings.notifications = notifications

    # Save updated settings
    data = save_user_settings(user_id, current_settings)

    return SettingsResponse(
        user_id=data["user_id"],
        settings=UserSettings(**data["settings"]),
        last_updated=datetime.fromisoformat(data["last_updated"]),
        version=data["version"]
    )
