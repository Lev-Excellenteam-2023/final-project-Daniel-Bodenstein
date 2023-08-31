from sqlalchemy import select, update

from sql_tables import Upload, _session, Status


class sqldb:
    def get_uploads_by_status(self, status):
        query = select(Upload).where(Upload.status == status)
        with _session() as s:
            return s.execute(query).scalars().all()

    def update_uploadds_by_id_list(self, id_list, updates_dict):
        query = update(Upload).where(Upload.id.in_(id_list)).values(**updates_dict)
        with _session() as s:
            s.execute(query)
            s.commit()


if __name__ == '__main__':
    print(sqldb().get_uploads_by_status(status=Status.pending))
