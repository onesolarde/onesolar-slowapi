
# OneSolar SlowAPI

This project is intended to be used during our interview process. It contains intentional bugs and architectural issues that we want you to identify and discuss.

It is not intended as a *test*, and there are no clear right answers. The goal is to start a productive discussion about code quality and architecture, and see how you approach problem-solving and code review. We encourage you to think out loud and share your thoughts as you go through the code. Feel free to take notes or add comments to the codebase as you review it. If you have questions, don't hesitate to ask! We want to see how you communicate and collaborate, not just how you code.

We are explicitly **not** asking you to identify syntax errors or typos, but rather to focus on higher-level issues such as code organization, design patterns, separation of concerns, maintainability, and security. This means that you can ignore linter warnings or formatting issues from your IDE. We also ask you to disable any AI code assistants such as GitHub Copilot, as they may distract you and disrupt your thought process.

After you finished reading this README, we will give you **15 minutes** to go through the codebase and make notes. As stated before, feel free to ask questions or share your thoughts during this process. After the 15 minutes are up, we will have a discussion about the codebase and the issues you identified.

## Project Layout

- `app/`: This is the main application directory. It contains services, database models, schemas, and routers.
  - `routers/`: This directory contains the API route handlers for different resources such as users, solar parks, and maintenance records.
  - `services/`: This directory contains various services that are used by the routers to perform specific tasks such as sending notifications or managing power.
  - `database.py`: This file contains the database connection and session management code.
  - `models.py`: This file contains the SQLAlchemy models for the database tables.
  - `schemas.py`: This file contains the Pydantic schemas for request and response validation.
- `main.py`: This is the entry point of the application where the FastAPI app is created and the routers are included.
- `tests/`: This directory is intended for tests.
