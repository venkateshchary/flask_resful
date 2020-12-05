from .. import db
from sqlalchemy.dialects.mysql import INTEGER


class OperationsHistory(db.Model):
    """
        model for operations history
    """
    __tablename__ = 'operations_history'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    account_no = db.Column(db.String, nullable=False, unique=False)
    created_date_time = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<account_no '{}'>".format(self.account_no)
