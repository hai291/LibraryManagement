GET_ALL_AUTHORS = "SELECT AuthorID, AuthorName FROM Authors"

INSERT_AUTHOR = "INSERT INTO Authors (AuthorName) VALUES (%s)"

DELETE_AUTHOR = "DELETE FROM Authors WHERE AuthorID = %s"