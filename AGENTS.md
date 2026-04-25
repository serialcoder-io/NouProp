# AGENTS.md

## Project Overview

This is a Django web application with the following stack:

* Django (backend)
* HTMX (for dynamic interactions)
* TailwindCSS and DaisyUI (UI styling)
* Django Cotton (reusable components)
* Django Allauth (authentication)

The project is structured into multiple apps:

* users
* reports
* listings
* locations

The database and core backend structure are considered stable.

---

## Project Structure

### Global Templates

A project-level `templates/` directory is used for shared UI.

Structure:

```text
templates/
│
├── cotton/
│   ├── components/
│   │   ├── ui/
│   │   └── ...
│   ├── partials/
│   └── icons/
```

* components/: reusable Django Cotton components
* components/ui/: base UI elements (buttons, inputs, etc.)
* partials/: reusable template fragments (navbar, footer, etc.)
* icons/: icon components

---

### App-Level Templates

Each app (users, reports, listings, locations) has its own `templates/` directory.

These are used for:

* app-specific pages
* app-specific components when necessary

Reuse rules:

* Use global components when possible
* Only create app-level components if they are truly specific to that app

---

## Strict Rules

### Database and Models

* Do not modify any `models.py` files
* The database schema is considered complete
* Do not introduce new fields, tables, or relationships

### Migrations

* Do not create, edit, delete, or run migrations
* Do not generate migrations under any circumstances

---

## Backend Guidelines

* Keep business logic in views or services, not in templates
* Follow consistent patterns (CBV or FBV per feature)
* Do not introduce breaking changes to existing flows

---

## HTMX Guidelines

* Prefer HTMX over custom JavaScript
* Use attributes such as `hx-get`, `hx-post`, `hx-target`, `hx-swap`
* For HTMX requests, return partial templates instead of full pages

---

## UI and Styling

* Use TailwindCSS and DaisyUI only
* Avoid custom CSS unless necessary
* Maintain visual consistency with existing components

---

## Components

* Use Django Cotton for reusable components
* Before creating a new component, check if one already exists
* Place reusable components in:

  * global: templates/cotton/components/
  * app-specific: inside the app templates directory

---

## Templates

* Keep templates simple and readable
* Avoid complex logic inside templates
* Use partials for repeated sections

---

## Authentication

* Authentication is handled by Django Allauth
* Do not replace or rewrite authentication logic
* Only extend if necessary and without breaking existing behavior

---

## What to Avoid

* Do not modify models or migrations
* Do not add unnecessary dependencies
* Do not duplicate components
* Do not introduce unnecessary JavaScript
* Do not change the project structure without reason

---

## What Is Allowed

* Adding new views and templates
* Building new features on top of existing logic
* Creating reusable components when needed
* Improving UI using the existing system

---

## General Principles

* Prefer reuse over duplication
* Prefer consistency over new patterns
* Prefer simple solutions over complex ones

---

## Final Instruction

Work within the existing architecture.
Do not modify the foundation (database, models, migrations).
Extend the project by adding features, not by changing core structures.
