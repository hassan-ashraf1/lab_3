# Lab 3 - Foreign Keys and Simple SQL

Hassan Ashraf   2304026
Moustafa Bahaa  2304039


## Problem 1 - COMPANY Database

This part creates the COMPANY database with three tables:

- DEPARTMENT
- EMPLOYEE
- PROJECT

Foreign keys are used to connect the tables and maintain referential integrity.

The SQL files are:

- problem1_DDL.sql
- problem1_DML.sql
- problem1_Answers.txt

## Problem 2 - Library Database

This part creates a Library database with two tables:

- AUTHOR
- BOOK

The BOOK table references AUTHOR using author_id.

ON DELETE CASCADE is used so when an author is deleted, their books are also deleted.

The website supports:

- Show authors and books
- Add authors and books
- Edit authors and books
- Delete books
- Delete authors

## How to Run

1. Run problem1_DDL.sql.
2. Run problem1_DML.sql.
3. Run problem2_DDL.sql.
4. Run problem2_DML.sql.
5. Open the website folder.
6. Install the requirements:

   py -m pip install -r requirements.txt

7. Create a .env file and enter the MySQL configuration.
8. Run the website:

   py app.py

9. Open the website in the browser and go to the Library page.