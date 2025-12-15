GET_ALL_BORROWERS = "SELECT BorrowerID, BorrowerName FROM Borrowers"

SEARCH_BORROWERS = "SELECT BorrowerID, BorrowerName FROM Borrowers WHERE BorrowerName LIKE %s"

INSERT_BORROWER = "INSERT INTO Borrowers (BorrowerName) VALUES (%s)"

DELETE_BORROWER = "DELETE FROM Borrowers WHERE BorrowerID = %s"

CHECK_BORROWER_EXISTS = "SELECT 1 FROM Borrowers WHERE BorrowerID = %s"