from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload, subqueryload

from sql_tables import User, Upload, _session, Status


class SqlQueries:

    def add_upload(self, upload):
        _session.add(upload)
        _session.commit()
        _session.refresh(upload)

    def get_upload(self, id):
        my_query = select(Upload).where(Upload.id == id)
        upload = _session.execute(my_query).scalar()
        return upload

    def add_user(self, user):
        _session.add(user)
        _session.commit()
        _session.refresh(user)

    def get_user_by_query(self, query):
        upload = _session.execute(query).scalar()
        return upload

    def get_user_by_id(self, id):
        query = select(User).where(User.id == id)
        return self.get_user_by_query(query)

    def get_user_by_email(self, email):
        query = select(User).where(User.email == email)
        return self.get_user_by_query(query)

    def add_upload_to_user_by_email(self, email, upload):
        query = select(User).where(User.email == email)
        with _session() as s:
            user = s.execute(query).scalar()

            if not user:
                raise ValueError("User with this email does not exist.")

            user.uploads.append(upload)
            s.commit()
            s.refresh(upload)
        return upload


if __name__ == '__main__':
    db = SqlQueries()

    new_upload = Upload(
        filename="example.txt",
        upload_time=datetime.utcnow(),
        status=Status.PENDING
    )

    new_user = User(
        email="danielboden111@gmail.com"
    )
    print(new_user)
    db.add_user(new_user)
    u = db.add_upload_to_user_by_email('danielboden111@gmail.com', new_upload)
    print(u)
