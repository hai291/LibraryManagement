# services/dashboard_service.py
from models.models import DashboardStats, Loan

class DashboardService:
    @staticmethod
    def get_summary_stats():
        """
        Lấy số liệu tổng quan cho Dashboard.
        Trả về: (nb, nbook, nloan, nov)
        """

        return DashboardStats.get_kpis()

    @staticmethod
    def get_chart_data():
        """
        Lấy dữ liệu để vẽ biểu đồ
        Trả về: (statuses, counts)
        """
        data = Loan.get_status_counts()
        if not data:
            return [], []
        
        statuses = [row[0] for row in data]
        counts = [row[1] for row in data]
        return statuses, counts