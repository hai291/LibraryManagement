DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;

CREATE TABLE Authors (
    AuthorID INT AUTO_INCREMENT PRIMARY KEY,
    AuthorName VARCHAR(255) NOT NULL
);

CREATE TABLE Books (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    BookTitle VARCHAR(255) NOT NULL,
    AuthorID INT,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE SET NULL
);

CREATE TABLE Borrowers (
    BorrowerID INT AUTO_INCREMENT PRIMARY KEY,
    BorrowerName VARCHAR(255) NOT NULL
);

CREATE TABLE Loans (
    LoanID INT AUTO_INCREMENT PRIMARY KEY,
    BorrowerID INT NOT NULL,
    BookID INT NOT NULL,
    BorrowedDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    Status ENUM('Borrowed', 'Returned', 'Overdue') NOT NULL DEFAULT 'Borrowed',
    FOREIGN KEY (BorrowerID) REFERENCES Borrowers(BorrowerID) ON DELETE CASCADE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (BorrowedDate <= DueDate)
);