import hashlib
from datetime import datetime

class Library:

    @staticmethod
    def get_unique_hashed_data(data: str):

        timestamp = datetime.now().timestamp()
        data = str(data) + str(timestamp)

        data = data.encode('utf-8')
        sha256_hash = hashlib.sha256(data).hexdigest()
        return sha256_hash
    

    def schema_model_to_dict(obj):
        return {ele.name: getattr(obj, ele.name) for ele in obj.__table__.columns}