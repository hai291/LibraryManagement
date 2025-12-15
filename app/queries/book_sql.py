GET_ALL_BOOKS = """
    SELECT BookID, BookTitle, IFNULL(AuthorID, 'None') 
    FROM Books
"""

SEARCH_BOOKS_BY_TITLE = """
    SELECT BookID, BookTitle, IFNULL(AuthorID, 'None') 
    FROM Books 
    WHERE BookTitle LIKE %s
"""

INSERT_BOOK = "INSERT INTO Books (BookTitle, AuthorID) VALUES (%s, %s)"

UPDATE_BOOK = "UPDATE Books SET BookTitle=%s, AuthorID=%s WHERE BookID=%s"

DELETE_BOOK = "DELETE FROM Books WHERE BookID = %s"

CHECK_BOOK_EXISTS = "SELECT 1 FROM Books WHERE BookID = %s"