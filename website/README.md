# Database Lab 2 — Login & To-Do Application

A responsive Flask + MySQL application for registering, logging in, and managing a private to-do list.

## Team members

- Member 1: **[Your full name]** — **[Your university ID]** — [what you implemented]
- Member 2 (if applicable): **[Partner full name]** — **[Partner university ID]** — [what they implemented]

Replace the placeholders before submission. If working alone, remove the second member.

## Technology

- Back end: Python 3, Flask
- Front end: HTML, CSS, JavaScript, Jinja templates
- Database: MySQL
- Password hashing: bcrypt
- Database access: PyMySQL with parameterized SQL

## Features

- R1: Register with name, email, password, and confirmation; duplicate email displays `Email Already Exists`; successful registration logs the user in.
- R2: Login, generic `Invalid email or password` error, and logout.
- R3: Login-protected private list, newest tasks first, with ownership enforced in SQL.
- R4–R7: Add, edit, mark done/not done, and delete tasks (with confirmation).
- R8: Browser-side and server-side validation for the required fields and task title length.
- R9: bcrypt password hashes, parameterized SQL, and session-derived user IDs.
- R10: Consistent responsive interface, visible feedback, and an empty-list state.

## Run from a fresh machine

1. Install Python 3.10+ and MySQL Server. Make sure the MySQL service is running.
2. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install packages: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and enter your local MySQL credentials and a long random `SESSION_SECRET`.
5. Run the schema in MySQL Workbench or from a terminal:
   `mysql -u root -p < database/schema.sql`
   **Warning:** the schema starts with `DROP DATABASE IF EXISTS registration`; it deletes and recreates that database.
6. Start the web server: `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.
8. Register an account, then add and manage tasks.

## Required screenshots

Save at least four real screenshots in `screenshots/` before submission:

1. `register-errors.png` — register page showing validation errors.
2. `login.png` — login page.
3. `todo-list.png` — list with several tasks, including one marked done.
4. `mobile.png` — application displayed in a phone-sized browser window (about 360 px wide).

Do not submit empty placeholder screenshots; capture them from your running application.

## README questions

### (a) Why do UPDATE and DELETE contain `AND user_id = ?`, and what changes if it is removed?

The task ID comes from a browser request and cannot be trusted by itself. The extra condition requires the task to belong to the currently logged-in user. If it is removed, a logged-in user who learns another task's ID could modify or delete that other user's task.

### (b) What happens if you insert a to-do for a `user_id` that does not exist, and which constraint is that?

MySQL rejects the insert because `todos.user_id` references `users.user_id`. This is the foreign-key (referential integrity) constraint.

### (c) Why store a hash and not the password?

A password hash is not the original password. bcrypt salts and deliberately slows hashing, making password guessing harder if the database is exposed. At login, the app verifies the typed password against the stored hash.

### (d) `name` is `NOT NULL`: why is an empty-name check still needed?

`NOT NULL` rejects SQL `NULL`, but an empty string (or a string containing only spaces) is still a non-NULL value. The application must check that the name contains actual text.

## Database structure

`database/schema.sql` creates the `registration` database and the `users` and `todos` tables. It is re-runnable, but drops the existing `registration` database first.

## Security notes

- Never commit `.env`; it contains local credentials and the session secret.
- `.env.example` contains placeholders only.
- SQL statements use parameters.
- Passwords are stored as bcrypt hashes.
- Task update/delete operations include the logged-in session's `user_id`.
- Change `SESSION_SECRET` before using the app beyond local development.

## Before submission

- [ ] Replace team member placeholders.
- [ ] Run the schema from a clean MySQL instance.
- [ ] Test register, login, logout, and every to-do action.
- [ ] Test required validation with JavaScript enabled and disabled.
- [ ] Capture the four required screenshots.
- [ ] Commit and push the complete project to GitHub.
- [ ] Be ready to explain every part of the code to the TA.
