from .. import db
from sqlalchemy.dialects.mysql import INTEGER


class Permissions(db.Model):
    """
        model for Permissions
    """
    __tablename__ = 'permissions'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    role_id = db.Column(INTEGER, nullable=False, unique=False)
    user_id = db.Column(INTEGER, nullable=False, unique=False)

    def __repr__(self):
        return "<role '{}'>".format(self.role_name)