import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__)) # Đường dẫn folder app
parent_dir = os.path.dirname(current_dir)                # Đường dẫn folder LibraryProject
env_path = os.path.join(parent_dir, '.env')
load_dotenv(env_path)

from db.connection import create_connection
from models.models import Borrower, Author, Book, Loan

from services.borrower_service import BorrowerService
from services.author_service import AuthorService
from services.book_service import BookService
from services.loan_service import LoanService
from services.dashboard_service import DashboardService
from services.report_service import ReportService

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Manager - MVC Architecture (All in App)")
        self.root.geometry("1100x750")

        # 1. KIỂM TRA KẾT NỐI DB
        test_conn = create_connection()
        if test_conn is None:
            messagebox.showerror("Lỗi Nghiêm Trọng", "Không thể kết nối đến Database!\nKiểm tra file .env hoặc MySQL server.")
            self.root.destroy()
            return
        else:
            test_conn.close()

        # 2. TẠO TAB CONTROL
        tab_control = ttk.Notebook(root)
        
        self.tab_dashboard = ttk.Frame(tab_control)
        self.tab_borrowers = ttk.Frame(tab_control)
        self.tab_authors = ttk.Frame(tab_control)
        self.tab_books = ttk.Frame(tab_control)
        self.tab_loans = ttk.Frame(tab_control)
        self.tab_reports = ttk.Frame(tab_control)

        tab_control.add(self.tab_dashboard, text='Dashboard')
        tab_control.add(self.tab_borrowers, text='Borrowers')
        tab_control.add(self.tab_authors, text='Authors')
        tab_control.add(self.tab_books, text='Books')
        tab_control.add(self.tab_loans, text='Loans')
        tab_control.add(self.tab_reports, text='Reports')
        tab_control.pack(expand=1, fill="both")

        self.setup_dashboard_tab()
        self.setup_borrower_tab()
        self.setup_authors_tab()
        self.setup_books_tab()
        self.setup_loans_tab()
        self.setup_reports_tab()

    # -------------------------------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------------------------------
    def setup_dashboard_tab(self):
        kpi_frame = ttk.LabelFrame(self.tab_dashboard, text="KPIs", padding=20)
        kpi_frame.pack(fill="x", padx=10, pady=5)

        self.lbl_total_borrowers = ttk.Label(kpi_frame, text="Bạn đọc: 0", font=("Arial", 12, "bold"))
        self.lbl_total_borrowers.pack(side="left", padx=20)
        
        self.lbl_total_books = ttk.Label(kpi_frame, text="Sách: 0", font=("Arial", 12, "bold"))
        self.lbl_total_books.pack(side="left", padx=20)

        self.lbl_active_loans = ttk.Label(kpi_frame, text="Đang mượn: 0", font=("Arial", 12, "bold"), foreground="blue")
        self.lbl_active_loans.pack(side="left", padx=20)

        self.lbl_overdue = ttk.Label(kpi_frame, text="Quá hạn: 0", font=("Arial", 12, "bold"), foreground="red")
        self.lbl_overdue.pack(side="left", padx=20)

        ttk.Button(kpi_frame, text="Refresh", command=self.refresh_dashboard).pack(side="right")
        
        self.chart_frame = ttk.Frame(self.tab_dashboard)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_dashboard()

    def refresh_dashboard(self):
        nb, nbook, nloan, nov = DashboardService.get_summary_stats()
        self.lbl_total_borrowers.config(text=f"Bạn đọc: {nb}")
        self.lbl_total_books.config(text=f"Sách: {nbook}")
        self.lbl_active_loans.config(text=f"Đang mượn: {nloan}")
        self.lbl_overdue.config(text=f"Quá hạn: {nov}")
        self.draw_chart()

    def draw_chart(self):
        for widget in self.chart_frame.winfo_children(): widget.destroy()
        statuses, counts = DashboardService.get_chart_data()
        if not statuses: return
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(statuses, counts, color=['green', 'orange', 'red'])
        ax.set_title("Trạng thái Mượn/Trả")
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # -------------------------------------------------------------------------
    # BORROWERS
    # -------------------------------------------------------------------------
    def setup_borrower_tab(self):
        frame = ttk.LabelFrame(self.tab_borrowers, text="Quản lý Bạn đọc", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        self.search_borrower = ttk.Entry(frame); self.search_borrower.pack(side="left", padx=5)
        ttk.Button(frame, text="Tìm", command=self.load_borrowers).pack(side="left")
        ttk.Label(frame, text="| Tên mới:").pack(side="left", padx=5)
        self.entry_borrower_name = ttk.Entry(frame); self.entry_borrower_name.pack(side="left")
        ttk.Button(frame, text="Thêm", command=self.add_borrower).pack(side="left", padx=5)
        ttk.Button(frame, text="Xóa", command=self.delete_borrower).pack(side="left", padx=5)
        ttk.Button(frame, text="Reset", command=lambda: [self.search_borrower.delete(0,tk.END), self.load_borrowers()]).pack(side="left")

        self.tree_borrowers = ttk.Treeview(self.tab_borrowers, columns=("ID", "Name"), show='headings')
        self.tree_borrowers.heading("ID", text="ID"); self.tree_borrowers.heading("Name", text="Name")
        self.tree_borrowers.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_borrowers()

    def load_borrowers(self):
        rows = Borrower.get_all(self.search_borrower.get().strip())
        self.tree_borrowers.delete(*self.tree_borrowers.get_children())
        if rows:
            for row in rows: self.tree_borrowers.insert("", "end", values=row)

    def add_borrower(self):
        success, msg = BorrowerService.add_borrower(self.entry_borrower_name.get())
        if success:
            messagebox.showinfo("OK", msg)
            self.entry_borrower_name.delete(0, tk.END)
            self.load_borrowers(); self.refresh_dashboard()
        else: messagebox.showwarning("Lỗi", msg)

    def delete_borrower(self):
        sel = self.tree_borrowers.focus()
        if not sel: return messagebox.showwarning("W", "Chọn dòng cần xóa")
        success, msg = BorrowerService.delete_borrower(self.tree_borrowers.item(sel, 'values')[0])
        if success:
            messagebox.showinfo("OK", msg)
            self.load_borrowers(); self.refresh_dashboard()
        else: messagebox.showerror("Lỗi", msg)

    # -------------------------------------------------------------------------
    # AUTHORS
    # -------------------------------------------------------------------------
    def setup_authors_tab(self):
        frame = ttk.LabelFrame(self.tab_authors, text="Tác giả", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        self.entry_author_name = ttk.Entry(frame, width=30); self.entry_author_name.pack(side="left", padx=5)
        ttk.Button(frame, text="Thêm", command=self.add_author).pack(side="left", padx=5)
        ttk.Button(frame, text="Xóa", command=self.delete_author).pack(side="left", padx=5)
        ttk.Button(frame, text="Reload", command=self.load_authors).pack(side="left", padx=5)
        self.tree_authors = ttk.Treeview(self.tab_authors, columns=("ID", "Name"), show='headings')
        self.tree_authors.heading("ID", text="ID"); self.tree_authors.heading("Name", text="Name")
        self.tree_authors.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_authors()

    def load_authors(self):
        rows = Author.get_all()
        self.tree_authors.delete(*self.tree_authors.get_children())
        if rows:
            for row in rows: self.tree_authors.insert("", "end", values=row)

    def add_author(self):
        success, msg = AuthorService.add_author(self.entry_author_name.get())
        if success:
            messagebox.showinfo("OK", msg); self.entry_author_name.delete(0, tk.END); self.load_authors()
        else: messagebox.showwarning("Lỗi", msg)

    def delete_author(self):
        sel = self.tree_authors.focus()
        if not sel: return messagebox.showwarning("W", "Chọn tác giả")
        success, msg = AuthorService.delete_author(self.tree_authors.item(sel, 'values')[0])
        if success: messagebox.showinfo("OK", msg); self.load_authors()
        else: messagebox.showerror("Lỗi", msg)

    # -------------------------------------------------------------------------
    # BOOKS
    # -------------------------------------------------------------------------
    def setup_books_tab(self):
        frame = ttk.LabelFrame(self.tab_books, text="Sách", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        self.search_book = ttk.Entry(frame); self.search_book.grid(row=0, column=1)
        ttk.Button(frame, text="Tìm", command=self.load_books).grid(row=0, column=2)
        ttk.Label(frame, text="Title:").grid(row=1, column=0)
        self.entry_book_title = ttk.Entry(frame); self.entry_book_title.grid(row=1, column=1)
        ttk.Label(frame, text="AuthorID:").grid(row=1, column=2)
        self.entry_book_aid = ttk.Entry(frame, width=5); self.entry_book_aid.grid(row=1, column=3)
        
        btn_f = ttk.Frame(frame); btn_f.grid(row=2, column=0, columnspan=4, pady=5)
        ttk.Button(btn_f, text="Thêm", command=self.add_book).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Sửa", command=self.update_book).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Xóa", command=self.delete_book).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Reset", command=lambda: [self.search_book.delete(0,tk.END), self.load_books()]).pack(side="left")

        self.tree_books = ttk.Treeview(self.tab_books, columns=("ID", "Title", "AID"), show='headings')
        self.tree_books.heading("ID", text="ID"); self.tree_books.heading("Title", text="Title"); self.tree_books.heading("AID", text="AuthorID")
        self.tree_books.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_books.bind("<<TreeviewSelect>>", self.on_book_select)
        self.load_books()

    def load_books(self):
        self.tree_books.delete(*self.tree_books.get_children())
        rows = Book.get_all(self.search_book.get().strip())
        if rows:
            for row in rows: self.tree_books.insert("", "end", values=row)

    def add_book(self):
        success, msg = BookService.add_book(self.entry_book_title.get(), self.entry_book_aid.get())
        if success:
            messagebox.showinfo("OK", msg); self.load_books(); self.refresh_dashboard()
            self.entry_book_title.delete(0, tk.END); self.entry_book_aid.delete(0, tk.END)
        else: messagebox.showerror("Lỗi", msg)

    def update_book(self):
        sel = self.tree_books.focus()
        if not sel: return messagebox.showwarning("W", "Chọn sách")
        bid = self.tree_books.item(sel, 'values')[0]
        success, msg = BookService.update_book(bid, self.entry_book_title.get(), self.entry_book_aid.get())
        if success: messagebox.showinfo("OK", msg); self.load_books(); self.refresh_dashboard()
        else: messagebox.showerror("Lỗi", msg)

    def delete_book(self):
        sel = self.tree_books.focus()
        if not sel: return messagebox.showwarning("W", "Chọn sách")
        success, msg = BookService.delete_book(self.tree_books.item(sel, 'values')[0])
        if success: messagebox.showinfo("OK", msg); self.load_books(); self.refresh_dashboard()
        else: messagebox.showerror("Lỗi", msg)

    def on_book_select(self, e):
        sel = self.tree_books.focus()
        if not sel: return
        v = self.tree_books.item(sel, 'values')
        self.entry_book_title.delete(0, tk.END); self.entry_book_title.insert(0, v[1])
        self.entry_book_aid.delete(0, tk.END)
        if v[2] != 'None': self.entry_book_aid.insert(0, v[2])

    # -------------------------------------------------------------------------
    # LOANS
    # -------------------------------------------------------------------------
    def setup_loans_tab(self):
        frame = ttk.LabelFrame(self.tab_loans, text="Mượn Trả", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        self.filter_status = ttk.Combobox(frame, values=["ALL", "Borrowed", "Returned", "Overdue"])
        self.filter_status.current(0); self.filter_status.pack(side="top", pady=5)
        ttk.Button(frame, text="Lọc", command=self.load_loans).pack(side="top")

        grid_f = ttk.Frame(frame); grid_f.pack(pady=5)
        ttk.Label(grid_f, text="BorrowerID:").grid(row=0, column=0); self.ent_lid_bid = ttk.Entry(grid_f); self.ent_lid_bid.grid(row=0, column=1)
        ttk.Label(grid_f, text="BookID:").grid(row=0, column=2); self.ent_lid_book = ttk.Entry(grid_f); self.ent_lid_book.grid(row=0, column=3)
        ttk.Label(grid_f, text="BorrowDate:").grid(row=1, column=0); self.ent_lid_bdate = ttk.Entry(grid_f); self.ent_lid_bdate.grid(row=1, column=1)
        ttk.Label(grid_f, text="DueDate:").grid(row=1, column=2); self.ent_lid_ddate = ttk.Entry(grid_f); self.ent_lid_ddate.grid(row=1, column=3)
        ttk.Label(grid_f, text="Status:").grid(row=2, column=0); 
        self.cb_status = ttk.Combobox(grid_f, values=["Borrowed", "Returned", "Overdue"]); self.cb_status.current(0); self.cb_status.grid(row=2, column=1)

        btn_f = ttk.Frame(frame); btn_f.pack(pady=5)
        ttk.Button(btn_f, text="Mượn Mới", command=self.add_loan).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Update", command=self.update_loan).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Xóa", command=self.delete_loan).pack(side="left", padx=5)
        ttk.Button(btn_f, text="Reload", command=self.load_loans).pack(side="left", padx=5)

        self.tree_loans = ttk.Treeview(self.tab_loans, columns=("LID", "BID", "BookID", "BDate", "DDate", "Status"), show='headings')
        for c in ["LID", "BID", "BookID", "BDate", "DDate", "Status"]: self.tree_loans.heading(c, text=c)
        self.tree_loans.pack(fill="both", expand=True, padx=10)
        self.tree_loans.bind("<<TreeviewSelect>>", self.on_loan_select)
        self.load_loans()

    def load_loans(self):
        rows = Loan.get_all(self.filter_status.get())
        self.tree_loans.delete(*self.tree_loans.get_children())
        if rows:
            for row in rows: self.tree_loans.insert("", "end", values=row)

    def add_loan(self):
        success, msg = LoanService.create_loan(
            self.ent_lid_bid.get(), self.ent_lid_book.get(), 
            self.ent_lid_bdate.get(), self.ent_lid_ddate.get(), self.cb_status.get()
        )
        if success:
            messagebox.showinfo("OK", msg); self.load_loans(); self.refresh_dashboard()
        else: messagebox.showerror("Lỗi", msg)

    def update_loan(self):
        sel = self.tree_loans.focus()
        if not sel: return messagebox.showwarning("W", "Chọn phiếu")
        lid = self.tree_loans.item(sel, 'values')[0]
        success, msg = LoanService.update_loan(
            lid, self.ent_lid_bid.get(), self.ent_lid_book.get(), 
            self.ent_lid_bdate.get(), self.ent_lid_ddate.get(), self.cb_status.get()
        )
        if success: messagebox.showinfo("OK", msg); self.load_loans(); self.refresh_dashboard()
        else: messagebox.showerror("Lỗi", msg)

    def delete_loan(self):
        sel = self.tree_loans.focus()
        if not sel: return messagebox.showwarning("W", "Chọn phiếu")
        if Loan.delete(self.tree_loans.item(sel, 'values')[0]):
            messagebox.showinfo("OK", "Đã xóa"); self.load_loans(); self.refresh_dashboard()
        else: messagebox.showerror("Lỗi", "Không xóa được")

    def on_loan_select(self, e):
        sel = self.tree_loans.focus(); 
        if not sel: return
        v = self.tree_loans.item(sel, 'values')
        self.ent_lid_bid.delete(0,tk.END); self.ent_lid_bid.insert(0,v[1])
        self.ent_lid_book.delete(0,tk.END); self.ent_lid_book.insert(0,v[2])
        self.ent_lid_bdate.delete(0,tk.END); self.ent_lid_bdate.insert(0,v[3])
        self.ent_lid_ddate.delete(0,tk.END); self.ent_lid_ddate.insert(0,v[4])
        self.cb_status.set(v[5])

    # -------------------------------------------------------------------------
    # REPORTS
    # -------------------------------------------------------------------------
    def setup_reports_tab(self):
        frame = ttk.Frame(self.tab_reports, padding=20); frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Xuất Báo Cáo (CSV)", font=("Arial", 14)).pack(pady=10)
        ttk.Button(frame, text="1. Danh sách mượn (Inner Join)", command=lambda: self.handle_export("INNER", "loans.csv")).pack(fill="x", pady=5)
        ttk.Button(frame, text="2. Tất cả bạn đọc (Left Join)", command=lambda: self.handle_export("LEFT", "borrowers.csv")).pack(fill="x", pady=5)
        ttk.Button(frame, text="3. Sách quá hạn (Overdue)", command=lambda: self.handle_export("OVERDUE", "overdue.csv")).pack(fill="x", pady=5)
        ttk.Button(frame, text="4. Full Data", command=lambda: self.handle_export("FULL", "full.csv")).pack(fill="x", pady=5)

    def handle_export(self, r_type, fname):
        f = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=fname)
        if not f: return
        success, msg = ReportService.export_report(r_type, f)
        if success: messagebox.showinfo("OK", msg)
        else: messagebox.showerror("Lỗi", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()