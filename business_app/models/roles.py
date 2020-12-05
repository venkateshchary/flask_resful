from .. import db
from sqlalchemy.dialects.mysql import INTEGER


class Roles(db.Model):
    """
        model for roles
    """
    __tablename__ = 'roles'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    role_name = db.Column(db.String, nullable=False, unique=False)

    def __repr__(self):
        return "<role '{}'>".format(self.role_name)
