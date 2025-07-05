from db import DataBase
from schemas import IssueSchema
from sqlalchemy import or_, and_

from library import Library

class IssueManagement:
    def __init__(self):
        self.db = DataBase(table_name=IssueSchema.__tablename__, schema=IssueSchema)

    def create_issue(self, issue_data):
        """
        create_issue used to create a new issue in the database based on roles

        ROLES:
        reporter/ admin: can create issues
        maintainer: cannot create issues
        """

        if issue_data['role'] == "maintainer":
            return 403
        
        issue_id = Library.get_unique_hashed_data(issue_data.get("title") + issue_data.get("user_id"))
        issue_data = IssueSchema(
            issue_id=issue_id,
            title=issue_data.get("title"),
            description=issue_data.get("description"),
            status=issue_data.get("status", "open"),
            created_by=issue_data.get("user_id")
        )

        self.db.session.add(issue_data)
        self.db.session.commit()

        return 200

    def get_issue(self, issue_data):
        """
        get_issue used to retrive issues based on the user role and issue_id
        
        reporter: can get only their own issues
        maintainer/ admin: can get all issues
        """
        issue_id = issue_data.get("issue_id")
        is_get_all_issues = issue_data.get("get_all_issues", False)
        user_role = issue_data.get("user_role", "reporter")
        user_id = issue_data.get("user_id")


        if user_role == "reporter":
            if not is_get_all_issues:
                filter_data = and_(IssueSchema.issue_id == issue_id, IssueManagement.user_id == user_id)

            else:
                filter_data = IssueManagement.user_id == user_id
            
        elif user_role == "maintainer" or user_role == "admin":
            if is_get_all_issues:
                filter_data = None

            else:
                filter_data = IssueSchema.issue_id == issue_id

        
        issues = self.db.session.query(IssueSchema).filter(
            filter_data
        ).all()

        return issues
            
    def update_issue(self, issue_data):
        pass

    def delete_issue(self,  issue_data):
        pass