import pymysql


class SQL:
    def __init__(self, user, host, password, db, charset='utf8mb4'):
        self.user = user
        self.host = host
        self.password = password
        self.database = db
        self.charset = charset

    def conn(self):
        db = pymysql.connect(user=self.user, host=self.host,
                             password=self.password, db=self.database,
                             charset=self.charset)
        return db

    def close(self, db):
        db.commit()
        db.close()