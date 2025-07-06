from db import DataBase
from schemas import SchedulerDBSchema
from sqlalchemy import or_, and_

from library.issues import IssueManagement

class StatsScheduler:
    def __init__(self):
        self.db = DataBase(table_name=SchedulerDBSchema.__tablename__, schema=SchedulerDBSchema)
        self.issue_management = IssueManagement()

    def log_daily_stats(self):
        result = self.issue_management.get_issue({
            "get_all_issues": True,
            "role":"admin"
        })
        

        total_issues = len(result)
        total_open = 0
        total_triaged = 0
        total_in_progress = 0
        total_done = 0
        
        total_severity_low = 0
        total_severity_medium = 0
        total_severity_high = 0
        total_severity_critical = 0
        
        for issue in result:
            status = issue.get('status', '').lower()
            if status == 'open':
                total_open += 1
            elif status == 'triaged':
                total_triaged += 1
            elif status == 'in_progress':
                total_in_progress += 1
            elif status == 'done':
                total_done += 1
            

            severity = issue.get('severity', '').lower() if issue.get('severity') else None
            if severity == 'low':
                total_severity_low += 1
            elif severity == 'medium':
                total_severity_medium += 1
            elif severity == 'high':
                total_severity_high += 1
            elif severity == 'critical':
                total_severity_critical += 1
        

        daily_stats = {
            "total_issues": total_issues,
            "total_issues_open": total_open,
            "total_issues_triaged": total_triaged,
            "total_issues_in_progress": total_in_progress,
            "total_issues_done": total_done,
            "total_issues_severity_low": total_severity_low,
            "total_issues_severity_medium": total_severity_medium,
            "total_issues_severity_high": total_severity_high,
            "total_issues_severity_critical": total_severity_critical
        }
        
        stats_data = SchedulerDBSchema(**daily_stats)
        self.db.session.add(stats_data)
        self.db.session.commit()

        return daily_stats