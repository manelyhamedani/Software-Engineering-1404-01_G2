# Wiki Service  
**Team: NullTerminated**

---

## Overview

The Wiki Service, developed by Team NullTerminated, is a structured
content management module designed to handle geographical and
informational articles within the main system.

This service provides a complete article lifecycle management system,
including categorization, tagging, revision history tracking,
internal article linking, reference management, reporting mechanisms,
and user interaction features such as following articles and
receiving notifications.

It is implemented as a dedicated Django application integrated
within the Core system and operates under the unified project
architecture.

---

## Architecture

The Wiki Service is implemented as a dedicated Django application
within the Core system and follows the service-oriented architecture
defined for the overall platform.

It is mounted under the `/team6/` URL namespace,
allowing it to operate as a modular component
while remaining fully integrated with the Core routing
and authentication system.

All components are executed inside Docker containers.
The Core container hosts the Django runtime,
while Team6 includes a Gateway (Nginx) container
as part of the standardized deployment structure.

During development, the service operates using Django's
default database configuration within the project environment.

---

## Project Structure

The Team6 module is organized as a standard Django application
with a clear separation of concerns between models, views,
services, templates, and routing.

```
team6/
├── models.py              # Data models (articles, tags, categories, revisions, etc.)
├── views.py               # Core view logic and request handling
├── urls.py                # URL routing for the service
├── services/              # Internal service logic (search, notifications, etc.)
├── templates/team6/       # HTML templates
├── migrations/            # Database schema migrations
├── templatetags/          # Custom template utilities
├── gateway.conf           # Nginx configuration for the service gateway
└── README.md              # Service documentation
```

The service follows Django best practices by separating
business logic from routing and presentation layers,
ensuring maintainability and scalability.

---

## How to Run

The project is containerized using Docker and can be executed using the provided shell scripts.

To start the entire system (Core + all team services):

```
./linux_scripts/up-all.sh
```

After successful startup, the Core service will be available at:

http://localhost:8000/

The Wiki Service (Team6) can be accessed via:

http://localhost:8000/team6/

To start only the Team6 Gateway container:

```
./linux_scripts/up-team.sh 6
```

In this case, the Gateway will be exposed at:

http://localhost:9126/

Note: The Wiki application itself runs inside the Core container and is mounted under the `/team6/` route.

## URL Structure

## Database

## Features

## Integration with Core

## Notes for Developers
