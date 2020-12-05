from .. import db
from sqlalchemy.dialects.mysql import INTEGER


class Operations(db.Model):
    """
        model for operations
    """
    __tablename__ = 'operations'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    account_no = db.Column(db.String, nullable=False, unique=False)
    amount = db.Column(INTEGER, nullable=False)
    modified_date_time = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<account_no '{}'>".format(self.account_no)
