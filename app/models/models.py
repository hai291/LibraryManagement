from db.connection import create_connection
from queries import borrower_sql, author_sql, book_sql, loan_sql, dashboard_sql, report_sql

class BaseModel:
    @staticmethod
    def _get_connection():
        return create_connection()

    @classmethod
    def fetch_all(cls, query, params=()):
        """Dùng cho SELECT lấy nhiều dòng"""
        conn = cls._get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()

    @classmethod
    def fetch_one(cls, query, params=()):
        """Dùng cho SELECT lấy 1 dòng hoặc kiểm tra tồn tại"""
        conn = cls._get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            conn.close()

    @classmethod
    def execute(cls, query, params=()):
        """Dùng cho INSERT, UPDATE, DELETE"""
        conn = cls._get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False
        finally:
            conn.close()

# =========================================================================
# MODEL: BORROWERS
# =========================================================================
class Borrower(BaseModel):
    @staticmethod
    def get_all(search_term=""):
        if search_term:
            return BaseModel.fetch_all(borrower_sql.SEARCH_BORROWERS, (f"%{search_term}%",))
        else:
            return BaseModel.fetch_all(borrower_sql.GET_ALL_BORROWERS)

    @staticmethod
    def add(name):
        return BaseModel.execute(borrower_sql.INSERT_BORROWER, (name,))

    @staticmethod
    def delete(bid):
        return BaseModel.execute(borrower_sql.DELETE_BORROWER, (bid,))

    @staticmethod
    def exists(bid):
        return BaseModel.fetch_one(borrower_sql.CHECK_BORROWER_EXISTS, (bid,)) is not None

# =========================================================================
# MODEL: AUTHORS
# =========================================================================
class Author(BaseModel):
    @staticmethod
    def get_all():
        return BaseModel.fetch_all(author_sql.GET_ALL_AUTHORS)

    @staticmethod
    def add(name):
        return BaseModel.execute(author_sql.INSERT_AUTHOR, (name,))

    @staticmethod
    def delete(aid):
        return BaseModel.execute(author_sql.DELETE_AUTHOR, (aid,))

# =========================================================================
# MODEL: BOOKS
# =========================================================================
class Book(BaseModel):
    @staticmethod
    def get_all(search_term=""):
        if search_term:
            return BaseModel.fetch_all(book_sql.SEARCH_BOOKS_BY_TITLE, (f"%{search_term}%",))
        else:
            return BaseModel.fetch_all(book_sql.GET_ALL_BOOKS)

    @staticmethod
    def add(title, author_id):
        # Xử lý logic author_id rỗng ngay tại đây hoặc service
        aid = author_id if author_id and str(author_id).isdigit() else None
        return BaseModel.execute(book_sql.INSERT_BOOK, (title, aid))
    
    @staticmethod
    def update(bid, title, author_id):
        aid = author_id if author_id and str(author_id).isdigit() else None
        return BaseModel.execute(book_sql.UPDATE_BOOK, (title, aid, bid))

    @staticmethod
    def delete(bid):
        return BaseModel.execute(book_sql.DELETE_BOOK, (bid,))
    
    @staticmethod
    def exists(bid):
        return BaseModel.fetch_one(book_sql.CHECK_BOOK_EXISTS, (bid,)) is not None

# =========================================================================
# MODEL: LOANS
# =========================================================================
class Loan(BaseModel):
    @staticmethod
    def get_all(status_filter="ALL"):
        if status_filter != "ALL":
            return BaseModel.fetch_all(loan_sql.GET_LOANS_BY_STATUS, (status_filter,))
        else:
            return BaseModel.fetch_all(loan_sql.GET_ALL_LOANS)
    def check_borrower_has_active_loan(borrower_id):
        return BaseModel.fetch_one(loan_sql.CHECK_BORROWER_ACTIVE, (borrower_id,)) is not None
    @staticmethod
    def get_status_counts():
        return BaseModel.fetch_all(loan_sql.GET_STATUS_COUNTS)

    @staticmethod
    def check_borrower_has_overdue(borrower_id):
        return BaseModel.fetch_one(loan_sql.CHECK_BORROWER_OVERDUE, (borrower_id,)) is not None

    @staticmethod
    def check_book_is_borrowed(book_id, exclude_loan_id=None):
        if exclude_loan_id:
            return BaseModel.fetch_one(loan_sql.CHECK_BOOK_BUSY_EXCLUDE_CURRENT, (book_id, exclude_loan_id)) is not None
        else:
            return BaseModel.fetch_one(loan_sql.CHECK_BOOK_BUSY, (book_id,)) is not None

    @staticmethod
    def add(bid, book_id, bdate, ddate, status):
        return BaseModel.execute(loan_sql.INSERT_LOAN, (bid, book_id, bdate, ddate, status))

    @staticmethod
    def update(lid, bid, book_id, bdate, ddate, status):
        return BaseModel.execute(loan_sql.UPDATE_LOAN, (bid, book_id, bdate, ddate, status, lid))

    @staticmethod
    def delete(lid):
        return BaseModel.execute(loan_sql.DELETE_LOAN, (lid,))

# =========================================================================
# MODEL: DASHBOARD 
# =========================================================================
class DashboardStats:
    @staticmethod
    def get_kpis():
        conn = create_connection()
        if not conn: return 0, 0, 0, 0
        cursor = conn.cursor()
        try:
            cursor.execute(dashboard_sql.COUNT_BORROWERS)
            nb = cursor.fetchone()[0]
            
            cursor.execute(dashboard_sql.COUNT_BOOKS)
            nbook = cursor.fetchone()[0]
            
            cursor.execute(dashboard_sql.COUNT_ACTIVE_LOANS)
            nloan = cursor.fetchone()[0]
            
            cursor.execute(dashboard_sql.COUNT_OVERDUE_LOANS)
            nov = cursor.fetchone()[0]
            
            return nb, nbook, nloan, nov
        finally:
            conn.close()

# =========================================================================
# MODEL: REPORTS
# =========================================================================
class Report:
    @staticmethod
    def execute_custom_query(query_type):
        conn = create_connection()
        if not conn: return [], []
        
        cursor = conn.cursor()
        sql = ""
        
        if query_type == "INNER": sql = report_sql.REPORT_INNER_JOIN
        elif query_type == "LEFT": sql = report_sql.REPORT_LEFT_JOIN
        elif query_type == "OVERDUE": sql = report_sql.REPORT_OVERDUE
        elif query_type == "FULL": sql = report_sql.REPORT_FULL_DETAILS
        else: return [], []

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            col_names = [i[0] for i in cursor.description] if cursor.description else []
            return col_names, rows
        except Exception as e:
            print(f"Report Error: {e}")
            return [], []
        finally:
            conn.close()