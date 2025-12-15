REPORT_INNER_JOIN = """
    SELECT B.BorrowerName, Bk.BookTitle, L.Status 
    FROM Loans L 
    JOIN Borrowers B ON L.BorrowerID = B.BorrowerID 
    JOIN Books Bk ON L.BookID = Bk.BookID;
"""

REPORT_LEFT_JOIN = """
    SELECT B.BorrowerName, Bk.BookTitle, L.Status 
    FROM Borrowers B 
    LEFT JOIN Loans L ON B.BorrowerID = L.BorrowerID 
    LEFT JOIN Books Bk ON L.BookID = Bk.BookID;
"""

REPORT_OVERDUE = """
    SELECT L.LoanID, B.BorrowerName, Bk.BookTitle, L.DueDate, L.Status 
    FROM Loans L 
    JOIN Borrowers B ON L.BorrowerID = B.BorrowerID 
    JOIN Books Bk ON L.BookID = Bk.BookID 
    WHERE L.Status = 'Overdue' 
       OR (L.Status = 'Borrowed' AND L.DueDate < CURDATE());
"""

REPORT_FULL_DETAILS = """
    SELECT B.BorrowerName, Bk.BookTitle, A.AuthorName, L.BorrowedDate, L.DueDate, L.Status
    FROM Loans L
    JOIN Borrowers B ON L.BorrowerID = B.BorrowerID
    JOIN Books Bk ON L.BookID = Bk.BookID
    LEFT JOIN Authors A ON Bk.AuthorID = A.AuthorID
"""