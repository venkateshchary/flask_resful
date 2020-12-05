from .. import db
from sqlalchemy.dialects.mysql import INTEGER, DATE


class User(db.Model):
    """
        model for user
    """
    __tablename__ = 'User'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=False)
    password = db.Column(db.String,  nullable=False)
    account_no = db.Column(db.Integer, nullable=True, index=False)
    created_date = db.Column(DATE, index=False, nullable=True)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
