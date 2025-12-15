# Library Management System (Python • Tkinter • MySQL)

## Overview

This project is a **desktop Library Management System** built with **Python**, **Tkinter** for the graphical user interface, and **MySQL** as the database backend. The application follows a **clean MVC-inspired architecture (Model – Service – View)** to clearly separate data access, business logic, and UI concerns.

The codebase is the result of **merging multiple modules into a single coherent system**, including database models, business services, GUI, reports, and automated tests. It is designed for educational use but structured closely to real-world software projects.

---

## Features

- **Borrower Management**
  - Add, delete, search borrowers
  - Business rule: borrowers with active or overdue loans cannot be deleted

- **Author Management**
  - Add and delete authors
  - Books may exist without an author (AuthorID = NULL)

- **Book Management**
  - Add, update, delete, search books by title
  - Business rule: books currently on loan cannot be deleted

- **Loan Management (Borrow / Return)**
  - Create, update, delete loan records
  - Business validations:
    - Due date must not be earlier than borrow date
    - Borrowers with overdue loans cannot borrow new books
    - A book can only be borrowed by one borrower at a time

- **Dashboard**
  - Total borrowers
  - Total books
  - Active loans
  - Overdue loans
  - Status bar chart using Matplotlib

- **Reports & CSV Export**
  - Inner join: current loans
  - Left join: all borrowers (including those without loans)
  - Overdue loans report
  - Full detailed report (Borrower + Book + Author + Loan)

- **Automated Unit Tests**
  - Full service-layer test coverage
  - Business rule validation using mocks

---


## Project Structure

- `db/`
  - `connection.py` – MySQL connection using environment variables
  - `schema.sql` – Database schema creation script
  - `seed.sql` – Initial sample data insertion script

- `app/models/`
  - BaseModel and domain models (Borrower, Author, Book, Loan, DashboardStats, Report)

- `app/queries/`
  - All raw SQL queries (CRUD, dashboard, reports)

- `app/services/`
  - Business logic and validation layer
  - Acts as a bridge between GUI and models

- `app/main.py`
  - Tkinter GUI and event handling

- `tests/`
  - Unit test suite using `unittest` and `mock`

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd library_management
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
```

### 3. Install dependencies

```bash
pip install mysql-connector-python python-dotenv matplotlib tkinter
```

---

## Database Setup

### 4. Create `.env` file

Create a `.env` file in the **Directory app**:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=1234
DB_NAME=library_db
```

---

### 5. Run `schema.sql`

The `schema.sql` file creates the database schema and tables.

```bash
mysql -u root -p < schema.sql
```



### 6. Run `seed.sql`

The `seed.sql` file inserts initial sample data.

```bash
mysql -u root -p library_db < seed.sql
```


## Running the Application

From the project root directory:

```bash
python app/main.py
```

If the database connection is successful, the Tkinter GUI will launch.

---

## Running Tests

```bash
python /test/test.py
```

Tests use mocks and do **not** require a live database connection.

---

## Architecture Notes

- Follows a **Model – Service – View** pattern
- Business rules are enforced at the service layer
- GUI never directly executes SQL queries
- Codebase is easy to extend with:
  - REST API (Flask / FastAPI)
  - ORM (SQLAlchemy)
  - Authentication & roles

---

## License

This project is intended for educational and internal use.

---

## Author

Developed by Hai Nguyen

Python • Tkinter • MySQL • MVC Architecture

## LinkToYoutube [https://youtube.com/@sonhai-hk1yz?si=B_CwOM4AAwVVb6vK]
