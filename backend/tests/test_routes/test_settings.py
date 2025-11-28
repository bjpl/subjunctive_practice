"""
Tests for settings API endpoints.
"""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from datetime import datetime

from main import app
from api.routes.settings import get_settings_file, UserSettings
from core.security import create_access_token
from core.config import get_settings as get_app_settings


@pytest.fixture
def client(override_get_db):
    """Create test client with database override."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create auth headers with a mock token."""
    # Create a test token directly without hitting the auth endpoint
    settings = get_app_settings()
    token_data = {
        "sub": "test_user_1",
        "username": "settingsuser",
        "email": "settings@test.com"
    }
    token = create_access_token(token_data, settings)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def cleanup_settings():
    """Clean up settings files after each test."""
    yield
    # Clean up test settings files
    settings_dir = Path("user_data/settings")
    if settings_dir.exists():
        for file in settings_dir.glob("settings_*.json"):
            file.unlink()


class TestGetSettings:
    """Test GET /api/settings endpoint."""

    def test_get_default_settings(self, client, auth_headers):
        """Test getting default settings for new user."""
        response = client.get("/api/settings", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert "user_id" in data
        assert "settings" in data
        assert "last_updated" in data
        assert "version" in data

        # Verify default settings structure
        settings = data["settings"]
        assert "notifications" in settings
        assert "practice" in settings
        assert "accessibility" in settings
        assert "language" in settings

    def test_get_settings_default_values(self, client, auth_headers):
        """Test default values are correct."""
        response = client.get("/api/settings", headers=auth_headers)
        settings = response.json()["settings"]

        # Notifications defaults
        assert settings["notifications"]["email"] is True
        assert settings["notifications"]["push"] is False
        assert settings["notifications"]["streakReminders"] is True

        # Practice defaults
        assert settings["practice"]["dailyGoal"] == 10
        assert settings["practice"]["autoAdvance"] is True
        assert settings["practice"]["showHints"] is True
        assert settings["practice"]["showExplanations"] is True

        # Accessibility defaults
        assert settings["accessibility"]["fontSize"] == "medium"
        assert settings["accessibility"]["highContrast"] is False
        assert settings["accessibility"]["reduceMotion"] is False

        # Language defaults
        assert settings["language"]["interface"] == "en"
        assert settings["language"]["practice"] == "es"

    def test_get_settings_unauthenticated(self, client):
        """Test that unauthenticated requests are rejected."""
        response = client.get("/api/settings")
        assert response.status_code in [401, 403]  # Either unauthorized or forbidden


class TestUpdateSettings:
    """Test PUT /api/settings endpoint."""

    def test_update_all_settings(self, client, auth_headers):
        """Test updating all settings at once."""
        new_settings = {
            "notifications": {
                "email": False,
                "push": True,
                "streakReminders": False
            },
            "practice": {
                "dailyGoal": 20,
                "autoAdvance": False,
                "showHints": False,
                "showExplanations": False
            },
            "accessibility": {
                "fontSize": "large",
                "highContrast": True,
                "reduceMotion": True
            },
            "language": {
                "interface": "es",
                "practice": "fr"
            }
        }

        response = client.put("/api/settings", json=new_settings, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["settings"]["notifications"]["email"] is False
        assert data["settings"]["notifications"]["push"] is True
        assert data["settings"]["practice"]["dailyGoal"] == 20
        assert data["settings"]["accessibility"]["fontSize"] == "large"
        assert data["settings"]["language"]["interface"] == "es"

    def test_update_settings_invalid_daily_goal(self, client, auth_headers):
        """Test that invalid daily goal is rejected."""
        new_settings = {
            "notifications": {"email": True, "push": False, "streakReminders": True},
            "practice": {"dailyGoal": 150, "autoAdvance": True, "showHints": True, "showExplanations": True},
            "accessibility": {"fontSize": "medium", "highContrast": False, "reduceMotion": False},
            "language": {"interface": "en", "practice": "es"}
        }

        response = client.put("/api/settings", json=new_settings, headers=auth_headers)
        assert response.status_code == 422  # Pydantic validation error
        # Check that error mentions dailyGoal constraint
        assert "dailyGoal" in str(response.json()).lower() or "daily" in str(response.json()).lower()

    def test_update_settings_invalid_font_size(self, client, auth_headers):
        """Test that invalid font size is rejected."""
        new_settings = {
            "notifications": {"email": True, "push": False, "streakReminders": True},
            "practice": {"dailyGoal": 10, "autoAdvance": True, "showHints": True, "showExplanations": True},
            "accessibility": {"fontSize": "huge", "highContrast": False, "reduceMotion": False},
            "language": {"interface": "en", "practice": "es"}
        }

        response = client.put("/api/settings", json=new_settings, headers=auth_headers)
        assert response.status_code == 422  # Pydantic validation error

    def test_update_settings_version_increment(self, client, auth_headers):
        """Test that version increments on update."""
        # Get initial settings
        response1 = client.get("/api/settings", headers=auth_headers)
        version1 = response1.json()["version"]

        # Update settings
        new_settings = {
            "notifications": {"email": False, "push": False, "streakReminders": False},
            "practice": {"dailyGoal": 15, "autoAdvance": True, "showHints": True, "showExplanations": True},
            "accessibility": {"fontSize": "medium", "highContrast": False, "reduceMotion": False},
            "language": {"interface": "en", "practice": "es"}
        }
        response2 = client.put("/api/settings", json=new_settings, headers=auth_headers)
        version2 = response2.json()["version"]

        assert version2 > version1


class TestPatchNotifications:
    """Test PATCH /api/settings/notifications endpoint."""

    def test_update_notifications_only(self, client, auth_headers):
        """Test updating only notification settings."""
        # Set initial settings with specific values
        initial_settings = {
            "notifications": {"email": True, "push": False, "streakReminders": True},
            "practice": {"dailyGoal": 25, "autoAdvance": False, "showHints": False, "showExplanations": False},
            "accessibility": {"fontSize": "large", "highContrast": True, "reduceMotion": True},
            "language": {"interface": "es", "practice": "fr"}
        }
        client.put("/api/settings", json=initial_settings, headers=auth_headers)

        # Update only notifications
        new_notifications = {
            "email": False,
            "push": True,
            "streakReminders": False
        }
        response = client.patch("/api/settings/notifications", json=new_notifications, headers=auth_headers)

        assert response.status_code == 200
        settings = response.json()["settings"]

        # Verify notifications changed
        assert settings["notifications"]["email"] is False
        assert settings["notifications"]["push"] is True
        assert settings["notifications"]["streakReminders"] is False

        # Verify other settings unchanged
        assert settings["practice"]["dailyGoal"] == 25
        assert settings["accessibility"]["fontSize"] == "large"
        assert settings["language"]["interface"] == "es"


class TestPatchPractice:
    """Test PATCH /api/settings/practice endpoint."""

    def test_update_practice_only(self, client, auth_headers):
        """Test updating only practice settings."""
        # Update only practice settings
        new_practice = {
            "dailyGoal": 50,
            "autoAdvance": False,
            "showHints": False,
            "showExplanations": True
        }
        response = client.patch("/api/settings/practice", json=new_practice, headers=auth_headers)

        assert response.status_code == 200
        settings = response.json()["settings"]

        assert settings["practice"]["dailyGoal"] == 50
        assert settings["practice"]["autoAdvance"] is False
        assert settings["practice"]["showHints"] is False
        assert settings["practice"]["showExplanations"] is True

        # Verify defaults for other sections
        assert settings["notifications"]["email"] is True
        assert settings["accessibility"]["fontSize"] == "medium"

    def test_update_practice_invalid_daily_goal(self, client, auth_headers):
        """Test that invalid daily goal is rejected in PATCH."""
        new_practice = {
            "dailyGoal": 0,
            "autoAdvance": True,
            "showHints": True,
            "showExplanations": True
        }
        response = client.patch("/api/settings/practice", json=new_practice, headers=auth_headers)

        assert response.status_code == 422  # Pydantic validation error
        # Check that error mentions dailyGoal constraint
        assert "dailyGoal" in str(response.json()).lower() or "daily" in str(response.json()).lower()


class TestPatchAccessibility:
    """Test PATCH /api/settings/accessibility endpoint."""

    def test_update_accessibility_only(self, client, auth_headers):
        """Test updating only accessibility settings."""
        new_accessibility = {
            "fontSize": "small",
            "highContrast": True,
            "reduceMotion": True
        }
        response = client.patch("/api/settings/accessibility", json=new_accessibility, headers=auth_headers)

        assert response.status_code == 200
        settings = response.json()["settings"]

        assert settings["accessibility"]["fontSize"] == "small"
        assert settings["accessibility"]["highContrast"] is True
        assert settings["accessibility"]["reduceMotion"] is True

    def test_update_accessibility_invalid_font_size(self, client, auth_headers):
        """Test that invalid font size is rejected in PATCH."""
        new_accessibility = {
            "fontSize": "extra-large",
            "highContrast": False,
            "reduceMotion": False
        }
        response = client.patch("/api/settings/accessibility", json=new_accessibility, headers=auth_headers)

        assert response.status_code == 422  # Pydantic validation error


class TestPatchLanguage:
    """Test PATCH /api/settings/language endpoint."""

    def test_update_language_only(self, client, auth_headers):
        """Test updating only language settings."""
        new_language = {
            "interface": "fr",
            "practice": "de"
        }
        response = client.patch("/api/settings/language", json=new_language, headers=auth_headers)

        assert response.status_code == 200
        settings = response.json()["settings"]

        assert settings["language"]["interface"] == "fr"
        assert settings["language"]["practice"] == "de"

    def test_update_language_invalid_code(self, client, auth_headers):
        """Test that invalid language code is rejected."""
        new_language = {
            "interface": "x",
            "practice": "es"
        }
        response = client.patch("/api/settings/language", json=new_language, headers=auth_headers)

        assert response.status_code == 400
        assert "Invalid interface language code" in response.json()["detail"]


class TestResetSettings:
    """Test DELETE /api/settings endpoint."""

    def test_reset_settings(self, client, auth_headers):
        """Test resetting settings to defaults."""
        # Set custom settings
        custom_settings = {
            "notifications": {"email": False, "push": True, "streakReminders": False},
            "practice": {"dailyGoal": 30, "autoAdvance": False, "showHints": False, "showExplanations": False},
            "accessibility": {"fontSize": "large", "highContrast": True, "reduceMotion": True},
            "language": {"interface": "es", "practice": "fr"}
        }
        client.put("/api/settings", json=custom_settings, headers=auth_headers)

        # Reset settings
        response = client.delete("/api/settings", headers=auth_headers)
        assert response.status_code == 204

        # Verify defaults are restored
        response = client.get("/api/settings", headers=auth_headers)
        settings = response.json()["settings"]

        assert settings["notifications"]["email"] is True
        assert settings["practice"]["dailyGoal"] == 10
        assert settings["accessibility"]["fontSize"] == "medium"
        assert settings["language"]["interface"] == "en"


class TestExportImportSettings:
    """Test export and import endpoints."""

    def test_export_settings(self, client, auth_headers):
        """Test exporting settings."""
        # Set custom settings
        custom_settings = {
            "notifications": {"email": False, "push": True, "streakReminders": False},
            "practice": {"dailyGoal": 30, "autoAdvance": False, "showHints": False, "showExplanations": False},
            "accessibility": {"fontSize": "large", "highContrast": True, "reduceMotion": True},
            "language": {"interface": "es", "practice": "fr"}
        }
        client.put("/api/settings", json=custom_settings, headers=auth_headers)

        # Export settings
        response = client.get("/api/settings/export", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert "export_date" in data
        assert "user_id" in data
        assert "settings" in data
        assert "metadata" in data

        assert data["settings"]["practice"]["dailyGoal"] == 30
        assert data["settings"]["accessibility"]["fontSize"] == "large"

    def test_import_settings(self, client, auth_headers):
        """Test importing settings."""
        # Create settings to import
        import_settings = {
            "notifications": {"email": False, "push": True, "streakReminders": True},
            "practice": {"dailyGoal": 40, "autoAdvance": True, "showHints": False, "showExplanations": True},
            "accessibility": {"fontSize": "small", "highContrast": False, "reduceMotion": True},
            "language": {"interface": "fr", "practice": "de"}
        }

        response = client.post("/api/settings/import", json=import_settings, headers=auth_headers)

        assert response.status_code == 200
        settings = response.json()["settings"]

        assert settings["practice"]["dailyGoal"] == 40
        assert settings["accessibility"]["fontSize"] == "small"
        assert settings["language"]["interface"] == "fr"

    def test_export_import_roundtrip(self, client, auth_headers):
        """Test that export and import preserve settings."""
        # Set original settings
        original_settings = {
            "notifications": {"email": False, "push": True, "streakReminders": False},
            "practice": {"dailyGoal": 35, "autoAdvance": False, "showHints": True, "showExplanations": False},
            "accessibility": {"fontSize": "large", "highContrast": True, "reduceMotion": False},
            "language": {"interface": "es", "practice": "it"}
        }
        client.put("/api/settings", json=original_settings, headers=auth_headers)

        # Export
        export_response = client.get("/api/settings/export", headers=auth_headers)
        exported_settings = export_response.json()["settings"]

        # Reset
        client.delete("/api/settings", headers=auth_headers)

        # Import
        client.post("/api/settings/import", json=exported_settings, headers=auth_headers)

        # Verify settings match original
        response = client.get("/api/settings", headers=auth_headers)
        current_settings = response.json()["settings"]

        assert current_settings == exported_settings


class TestSettingsPersistence:
    """Test settings persistence across requests."""

    def test_settings_persist(self, client, auth_headers):
        """Test that settings persist across multiple requests."""
        # Set settings
        new_settings = {
            "notifications": {"email": False, "push": True, "streakReminders": True},
            "practice": {"dailyGoal": 25, "autoAdvance": False, "showHints": True, "showExplanations": False},
            "accessibility": {"fontSize": "large", "highContrast": False, "reduceMotion": True},
            "language": {"interface": "es", "practice": "pt"}
        }
        client.put("/api/settings", json=new_settings, headers=auth_headers)

        # Get settings multiple times
        for _ in range(3):
            response = client.get("/api/settings", headers=auth_headers)
            settings = response.json()["settings"]

            assert settings["practice"]["dailyGoal"] == 25
            assert settings["accessibility"]["fontSize"] == "large"
            assert settings["language"]["interface"] == "es"

    def test_multiple_updates(self, client, auth_headers):
        """Test multiple consecutive updates."""
        # First update
        client.patch("/api/settings/practice",
                    json={"dailyGoal": 20, "autoAdvance": True, "showHints": True, "showExplanations": True},
                    headers=auth_headers)

        # Second update
        client.patch("/api/settings/accessibility",
                    json={"fontSize": "small", "highContrast": True, "reduceMotion": False},
                    headers=auth_headers)

        # Third update
        client.patch("/api/settings/language",
                    json={"interface": "de", "practice": "ru"},
                    headers=auth_headers)

        # Verify all updates persisted
        response = client.get("/api/settings", headers=auth_headers)
        settings = response.json()["settings"]

        assert settings["practice"]["dailyGoal"] == 20
        assert settings["accessibility"]["fontSize"] == "small"
        assert settings["language"]["interface"] == "de"
