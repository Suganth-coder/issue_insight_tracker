from db import DataBase
from schemas import IssueDBSchema
from sqlalchemy import or_, and_

from library import Library

class IssueManagement:
    def __init__(self):
        self.db = DataBase(table_name=IssueDBSchema.__tablename__, schema=IssueDBSchema)

    def create_issue(self, issue_data):
        """
        create_issue used to create a new issue in the database based on roles

        reporter/ admin: can create issues
        maintainer: cannot create issues

        @return 403 | 200 
        """

        if issue_data['role'] == "maintainer":
            return 403

        issue_id = Library.get_unique_hashed_data(issue_data.get("title") + issue_data.get("user_id"))
        issue_data = IssueDBSchema(
            issue_id=issue_id,
            title=issue_data.get("title"),
            s3_object_key=issue_data.get("s3_object_key"),
            description=issue_data.get("description"),
            status=issue_data.get("status", "open"),
            created_by=issue_data.get("user_id")
        )

        self.db.session.add(issue_data)
        self.db.session.commit()

        return {'code':200, 'issue_id':issue_id}
    

    def get_issue(self, issue_data):
        """
        get_issue used to retrive issues based on the user role and issue_id
        
        reporter: can get only their own issues
        maintainer/ admin: can get all issues

        @return list()
        """
        issue_id = issue_data.get("issue_id")
        is_get_all_issues = issue_data.get("get_all_issues", False)
        user_role = issue_data.get("role", "reporter")
        user_id = issue_data.get("user_id")
        need_objects = issue_data.get("need_objects", False)

        issues = None

        if user_role == "reporter":
            if not is_get_all_issues:
                filter_data = and_(IssueDBSchema.issue_id == issue_id, IssueDBSchema.created_by == user_id)

            else:
                filter_data = IssueDBSchema.created_by == user_id
            
        elif user_role == "maintainer" or user_role == "admin":
            if is_get_all_issues:
                issues = self.db.session.query(IssueDBSchema).all()

            else:
                filter_data = IssueDBSchema.issue_id == issue_id

        if issues is None:
            issues = self.db.session.query(IssueDBSchema).filter(
                filter_data
            ).all()
        

        return [Library.schema_model_to_dict(issue) for issue in issues] if not need_objects else issues
            
    def update_issue(self, issue_data):
        """
        update issue used to update an existing issue based on the user role

        reporter: cannot update issues
        maintainer: can update status and severity
        admin: can update all fields

        @return 404 | 200
        """
        issue_id = issue_data.get("issue_id")
        user_role = issue_data.get("role", "reporter")
        user_id = issue_data.get("user_id")

        self.role_access = {
            "reporter":[],
            "maintainer": ["status", "severity"],
            "admin": ["title", "description", "status", "severity", "s3_object_key"]
        }
        result = self.get_issue({
            "issue_id": issue_id,
            "get_all_issues": False,
            "user_role": user_role,
            "user_id": user_id,
            "need_objects": True,
            "role": user_role
        })

        if len(result) == 0:
            return 404
        
        issue = result[0]

        if issue_data.get("title") and "title" in self.role_access[user_role]:
            issue.title = issue_data.get("title")

        if issue_data.get("description") and "description" in self.role_access[user_role]:
            issue.description = issue_data.get("description")

        if issue_data.get("status") and "status" in self.role_access[user_role]:
            issue.status = issue_data.get("status")

        if issue_data.get("severity") and "severity" in self.role_access[user_role]:
            issue.severity = issue_data.get("severity")

        if issue_data.get("s3_object_key") and "s3_object_key" in self.role_access[user_role]:
            issue.s3_object_key = issue_data.get("s3_object_key")
        
        self.db.session.add(issue)
        self.db.session.commit()

        return 200

    def delete_issue(self,  issue_data):
        """
        delete_issue used to delete an existing issue based on the user role

        reporter/maintainer: cannot delete issues
        admin: can delete issues

        @return 403 | 404 | 200
        """
        issue_id = issue_data.get("issue_id")
        user_role = issue_data.get("role", "reporter")

        if user_role != "admin":
            return 403
        
        result = self.get_issue({
            "issue_id": issue_id,
            "get_all_issues": False,
            "role": user_role,
            "need_objects": True
        })

        if len(result) == 0:
            print('Issue not found for deletion')
            return 404
        
        issue = result[0]
        self.db.session.delete(issue)
        self.db.session.commit()

        return 200