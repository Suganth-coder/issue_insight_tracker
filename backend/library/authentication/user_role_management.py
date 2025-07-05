from db import DataBase
from schemas import UserRoles

class UserRoleManagement:
    def __init__(self):
        self.db = DataBase(table_name=UserRoles.__tablename__, schema=UserRoles)
        result = self.db.check_connection()

        self.privilege_code = {
            "reporter": 1,
            "maintainer": 2,
            "admin": 3,
        }
        

    def add_user_role(self, user_id, email, role="reporter"):
        if role not in self.privilege_code:
            return 400

        user_role = UserRoles(
            user_id=user_id,
            email=email,
            role=role,
            privilege_code=self.privilege_code[role]
        )

        self.db.session.add(user_role)
        self.db.session.commit()

        return 200

    def get_user_role(self, email):

        user_query = self.db.session.query(UserRoles).filter(
            UserRoles.email == email
        ).all()

        return 404 if len(user_query) == 0 else user_query[0].role

        
