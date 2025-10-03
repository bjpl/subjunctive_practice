# Platform Abstraction Layer Architecture

## Overview

The Platform Abstraction Layer provides a clean separation between business logic and platform-specific implementations, enabling true platform independence for the Subjunctive Practice application.

## Architecture Principles

### 1. Dependency Inversion
- Business logic depends on abstractions, not concrete implementations
- Platform-specific code implements abstract interfaces
- Dependencies flow inward toward business logic

### 2. Interface Segregation
- Each abstraction has a focused, single responsibility
- Interfaces are minimal and cohesive
- Clients only depend on methods they actually use

### 3. Factory Pattern
- Factories create platform-specific instances
- Platform selection happens at configuration time
- Runtime platform switching supported

### 4. Dependency Injection
- ServiceContainer manages dependencies
- Configuration-driven service resolution
- Supports singleton and factory patterns

## Core Abstractions

### IUIRenderer
**Purpose**: Platform-agnostic UI rendering

**Implementations**:
- **Desktop**: `PyQtUIRenderer` - Renders to PyQt widgets
- **Web**: `ReactUIRenderer` - Generates React component specs

**Key Features**:
- Component-based UI model
- Event handling abstraction
- Modal/dialog support
- Navigation abstraction

**Usage Example**:
```python
from src.shared.abstractions import IUIRenderer, UIComponent, UIComponentType

# Platform-agnostic button creation
button = UIComponent(
    component_id='submit_btn',
    component_type=UIComponentType.BUTTON,
    properties={'text': 'Submit', 'enabled': True}
)

# Render on current platform
renderer = container.resolve(IUIRenderer)
rendered = renderer.render(button)
```

### IDataStore
**Purpose**: Platform-agnostic data persistence

**Implementations**:
- **Desktop**: `SQLiteDataStore` - Local SQLite database
- **Web Backend**: `PostgreSQLDataStore` - PostgreSQL database
- **Web Frontend**: `APIDataStore` - RESTful API client

**Key Features**:
- CRUD operations
- Query filtering and sorting
- Transaction support
- Caching layer

**Usage Example**:
```python
from src.shared.abstractions import IDataStore, QueryFilter, QueryOptions

# Platform-agnostic data access
data_store = container.resolve(IDataStore)

await data_store.connect()

# Create record
user_id = await data_store.create('users', {
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Query with filters
filters = [QueryFilter(field='active', operator='eq', value=True)]
options = QueryOptions(filters=filters, limit=10)
users = await data_store.query('users', options)
```

### ILogger
**Purpose**: Platform-agnostic logging

**Implementations**:
- **Desktop**: `FileLogger` - Rotating file logs
- **Web Backend**: `ConsoleLogger` - Structured console logs
- **Web Frontend**: `BrowserLogger` - Browser console logs

**Key Features**:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Contextual logging
- Exception tracking
- Flexible formatting

**Usage Example**:
```python
from src.shared.abstractions import ILogger

logger = container.resolve(ILogger)

# Add persistent context
logger.add_context('user_id', '12345')
logger.add_context('session_id', 'abc-def')

# Log with automatic context
logger.info("User logged in")
logger.error("Failed to save data", exception=ex, context={'record_id': '789'})
```

### IEventBus
**Purpose**: Platform-agnostic event handling

**Implementations**:
- **Desktop**: `InMemoryEventBus` - Synchronous in-process events
- **Web Backend**: `RedisEventBus` - Distributed pub/sub via Redis
- **Web Frontend**: `BrowserEventBus` - Browser custom events

**Key Features**:
- Subscribe/publish pattern
- Wildcard event matching
- Priority-based handlers
- Pause/resume support

**Usage Example**:
```python
from src.shared.abstractions import IEventBus, Event

event_bus = container.resolve(IEventBus)

# Subscribe to events
def on_user_login(event: Event):
    user_id = event.data['user_id']
    print(f"User {user_id} logged in")

event_bus.subscribe('user.login', on_user_login)

# Publish events
event_bus.publish(Event(
    event_type='user.login',
    data={'user_id': '12345', 'timestamp': '2025-10-02'}
))

# Wildcard subscriptions
event_bus.subscribe('user.*', on_any_user_event)
```

## Dependency Injection System

### ServiceContainer

The `ServiceContainer` class manages dependencies and creates platform-specific instances:

```python
from src.shared.abstractions.base import Platform, PlatformConfig
from src.shared.abstractions.service_container import ServiceContainer
from src.shared.abstractions import ILogger, IDataStore

# Create configuration
config = PlatformConfig(
    platform=Platform.DESKTOP,
    debug_mode=True,
    log_level='DEBUG'
)

# Create container
container = ServiceContainer(config)

# Register services
container.register_factory(ILogger, LoggerFactory())
container.register_factory(IDataStore, DataStoreFactory())

# Resolve services
logger = container.resolve(ILogger)
data_store = container.resolve(IDataStore)
```

### Platform Selection

The `PlatformSelector` provides utilities for platform detection and configuration:

```python
from src.shared.abstractions.platform_selector import PlatformSelector, quick_setup

# Auto-detect platform
platform = PlatformSelector.detect_platform()

# Load configuration
config = PlatformSelector.load_config('config.json')

# Quick setup (convenience method)
container = quick_setup(
    platform=Platform.WEB,
    api_url='https://api.example.com',
    api_key='secret'
)
```

## Configuration

### Configuration File Format

```json
{
  "platform": "desktop",
  "debug_mode": true,
  "log_level": "INFO",
  "cache_enabled": true,
  "async_enabled": false,
  "database_path": "app_data.db",
  "log_dir": "logs",
  "log_file": "app.log"
}
```

### Environment Variables

- `PLATFORM`: Override platform (desktop, web, cli)
- `DEBUG`: Enable debug mode (true/false)
- `LOG_LEVEL`: Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Factory Pattern

Factories create platform-specific instances based on configuration:

```python
from src.shared.abstractions.factories import (
    UIRendererFactory,
    DataStoreFactory,
    LoggerFactory,
    EventBusFactory
)

# Create factory
logger_factory = LoggerFactory()

# Check platform support
supports_web = logger_factory.supports_platform(Platform.WEB)

# Create instance
logger = logger_factory.create(config)
```

## Platform-Specific Adapters

### Desktop Adapters (PyQt)

Located in `src/desktop_app/adapters/`:

- `pyqt_ui_renderer.py` - PyQt widget rendering
- `sqlite_data_store.py` - SQLite persistence
- `file_logger.py` - File-based logging
- `in_memory_event_bus.py` - In-process events

### Web Adapters (FastAPI/React)

Located in `src/web/adapters/`:

- `react_ui_renderer.py` - React component specs
- `api_data_store.py` - API client for backend
- `console_logger.py` - Structured console logging
- `browser_event_bus.py` - Browser custom events

## Integration Patterns

### Business Logic Layer

Business logic should only depend on abstractions:

```python
class ExerciseService:
    """Service for managing exercises (platform-independent)."""

    def __init__(
        self,
        data_store: IDataStore,
        logger: ILogger,
        event_bus: IEventBus
    ):
        self.data_store = data_store
        self.logger = logger
        self.event_bus = event_bus

    async def create_exercise(self, exercise_data: dict) -> str:
        """Create a new exercise."""
        self.logger.info("Creating exercise", context={'type': exercise_data.get('type')})

        # Save to data store (platform-agnostic)
        exercise_id = await self.data_store.create('exercises', exercise_data)

        # Publish event (platform-agnostic)
        self.event_bus.publish(Event(
            event_type='exercise.created',
            data={'exercise_id': exercise_id}
        ))

        return exercise_id
```

### Application Initialization

```python
from src.shared.abstractions.platform_selector import quick_setup
from src.shared.abstractions import ILogger, IDataStore, IEventBus

# Initialize platform
container = quick_setup(config_path='config.json')

# Create services with resolved dependencies
exercise_service = ExerciseService(
    data_store=container.resolve(IDataStore),
    logger=container.resolve(ILogger),
    event_bus=container.resolve(IEventBus)
)

# Business logic works identically across platforms
await exercise_service.create_exercise({'type': 'subjunctive', 'difficulty': 'medium'})
```

## Testing Strategy

### Unit Tests
- Test abstractions independently
- Mock platform-specific implementations
- Verify interface contracts

### Integration Tests
- Test cross-platform compatibility
- Verify platform switching
- Test shared business logic

### Platform-Specific Tests
- Test each adapter implementation
- Verify platform-specific behavior
- Test edge cases

## Migration Guide

### Converting Existing Code

**Before** (Platform-specific):
```python
# Desktop-specific code
from PyQt6.QtWidgets import QPushButton

button = QPushButton("Submit")
button.clicked.connect(on_submit)
```

**After** (Platform-agnostic):
```python
# Platform-agnostic code
from src.shared.abstractions import UIComponent, UIComponentType, UIEventType

button = UIComponent(
    component_id='submit_btn',
    component_type=UIComponentType.BUTTON,
    properties={'text': 'Submit'}
)
button.add_event_handler(UIEventType.CLICK, on_submit)

renderer = container.resolve(IUIRenderer)
rendered = renderer.render(button)
```

## Performance Considerations

1. **Abstraction Overhead**: Minimal - interfaces are lightweight
2. **Factory Creation**: One-time cost at initialization
3. **Container Resolution**: Fast dictionary lookups
4. **Event Delivery**: Optimized for each platform

## Benefits

1. **Platform Independence**: Business logic works across desktop, web, and CLI
2. **Testability**: Easy to mock dependencies for testing
3. **Maintainability**: Clear separation of concerns
4. **Flexibility**: Switch platforms via configuration
5. **Extensibility**: Add new platforms by implementing interfaces

## Future Enhancements

1. **Mobile Support**: Add iOS/Android adapters
2. **Cloud Logging**: Add CloudWatch/Datadog logger implementations
3. **Distributed Events**: Add Kafka/RabbitMQ event bus implementations
4. **GraphQL Data Store**: Add GraphQL client adapter
5. **Async UI Updates**: Add reactive UI rendering support

## References

- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
- [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)
- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)
- [Interface Segregation](https://en.wikipedia.org/wiki/Interface_segregation_principle)

## Version History

- **v1.0.0** (2025-10-02): Initial abstraction layer implementation
  - Core abstractions: IUIRenderer, IDataStore, ILogger, IEventBus
  - Desktop adapters: PyQt implementations
  - Web adapters: FastAPI/React implementations
  - Dependency injection system
  - Platform selection and configuration
