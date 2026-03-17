# Interviewer Notes — Solar Park Construction Manager

This document lists every intentional problem embedded in the project.
**Do not share this file with candidates.**

---

## Security Issues

### S1: Exposed secrets

Secrets such as `SECRET_KEY` are exposed via the `/config` endpoint, which is a critical security vulnerability. This allows attackers to easily access sensitive information that should be kept confidential. Secrets should **never** be exposed through API endpoints or any publicly accessible interface. Instead, they should be securely stored and accessed only by the application when necessary.

### S2: Password stored in plaintext in the database

Passwords are stored in plaintext in the database, which is a severe security vulnerability. If the database is compromised, attackers can easily access user passwords. Passwords should always be hashed using a strong hashing algorithm (e.g., bcrypt) before being stored in the database to protect user credentials.

Additionally, the password column is included in the `UserResponse` schema, which means that the API is exposing user passwords in its responses. This is another critical security issue.

### S3: User endpoint is unprotected

The `/user/{user_id}` endpoint is unprotected, allowing anyone to access user information without authentication. This can lead to unauthorized access to sensitive user data. Proper authentication and authorization mechanisms should be implemented to ensure that only authorized users can access this endpoint.

### S4: SQL injection vulnerability in user search endpoint

The `/users/search` endpoint is vulnerable to SQL injection attacks because it directly incorporates user input into the SQL query without proper sanitization. An attacker could manipulate the `query` parameter to execute arbitrary SQL commands, potentially compromising the database. To mitigate this vulnerability, parameterized queries or an ORM should be used to safely handle user input.

## Code Quality Issues

### Q1. Hardcoded default values for environment variables

The app contains several hardcoded default values for environment variables, such as `DATABASE_URL` and `ENV`. Some of them don't even agree with each other. Instead, the app should fail to start if required environment variables are not set.

### Q2: Missing timezones in datetime.now calls

The `datetime.now()` function is used without specifying a timezone, which can lead to issues when the application is deployed in different environments or when users are in different timezones. It is recommended to specify the `tz` parameter when calling `datetime.now()` to ensure that the application handles time correctly across different regions.

### Q3: Unclear units for database columns

The `location` and `energy_output` columns in the `SolarPark` model do not specify their units, which can lead to confusion for developers and users of the API. It is important to clearly document the expected units for these fields (e.g., `location` in latitude/longitude and `energy_output` in kWh) to ensure that data is correctly interpreted and used.

### Q4: No validation in Pydantic schemas

The Pydantic schemas do not include any validation for the fields, which can lead to invalid data being accepted by the API. For example, there is no validation to ensure that `energy_output` is a positive number or that `location` follows a specific format. Adding validation rules to the Pydantic schemas would help ensure that the API receives valid and consistent data.

## Architectural Issues

### A1. Database tables created at every app startup

The line `Base.metadata.create_all(bind=engine)` is called every time the app starts, which can lead to performance issues and potential data loss in production environments. In a real application, database migrations should be handled using a proper migration tool like Alembic.

### A2. Environment variables loaded after they are used

The .env file is loaded **after** the import of the database module, which reads the `DATABASE_URL` environment variable. This means that the database connection string will not be loaded from the .env file, and the app will fail to connect to the database. Additionally, the app configuration is never actually used anywhere.

### A3. Exported function defined in router file

The function `load_maintenance_records`, which is imported by other places in the app, is defined in the `maintenance.py` router file, which is not a good practice. This function should be moved to a separate utility module or service layer to keep the router file focused on handling HTTP requests and responses. This separation of concerns improves code organization and maintainability.

### A4. Complex side effects in the maintenance endpoint

The `create_maintenance_record` endpoint has complex side effects, such as notifying users, reticulating splines, restarting the solar park, and entangling qubits. This makes the endpoint difficult to understand and maintain. There are multiple options to decouple these side effects, such as using an event-driven architecture, implementing a service layer, or using background tasks to handle these operations asynchronously. This would improve the maintainability and scalability of the application.

### A5. Singleton instances of services

The services (e.g., `notification_service`, `power_management_service`, etc.) are instantiated as singletons at the module level. This can lead to issues with state management and testing, as these instances may maintain state that can affect other parts of the application. It would be better to use dependency injection to manage the lifecycle of these services, allowing for better testability and flexibility in how they are used throughout the application.
