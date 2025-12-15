GET_ALL_LOANS = """
    SELECT LoanID, BorrowerID, BookID, BorrowedDate, DueDate, Status 
    FROM Loans
"""

GET_LOANS_BY_STATUS = """
    SELECT LoanID, BorrowerID, BookID, BorrowedDate, DueDate, Status 
    FROM Loans 
    WHERE Status = %s
"""

CHECK_BORROWER_ACTIVE = """
    SELECT 1 FROM Loans 
    WHERE BorrowerID = %s AND Status IN ('Borrowed', 'Overdue')
"""

GET_STATUS_COUNTS = """
    SELECT Status, COUNT(*) 
    FROM Loans 
    GROUP BY Status
"""

CHECK_BORROWER_OVERDUE = """
    SELECT 1 FROM Loans 
    WHERE BorrowerID = %s AND Status = 'Overdue'
"""

CHECK_BOOK_BUSY = """
    SELECT 1 FROM Loans 
    WHERE BookID = %s AND Status IN ('Borrowed', 'Overdue')
"""

CHECK_BOOK_BUSY_EXCLUDE_CURRENT = """
    SELECT 1 FROM Loans 
    WHERE BookID = %s AND Status IN ('Borrowed', 'Overdue') AND LoanID != %s
"""

INSERT_LOAN = """
    INSERT INTO Loans (BorrowerID, BookID, BorrowedDate, DueDate, Status) 
    VALUES (%s, %s, %s, %s, %s)
"""

UPDATE_LOAN = """
    UPDATE Loans 
    SET BorrowerID=%s, BookID=%s, BorrowedDate=%s, DueDate=%s, Status=%s 
    WHERE LoanID=%s
"""

DELETE_LOAN = "DELETE FROM Loans WHERE LoanID = %s"