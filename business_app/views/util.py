

def prepare_vo(row):
    """method to get json data from table row"""
    response = {}
    for column in row.__table__.columns:
        if column.name not in ['password', 'salt', 'nonce']:
            if column.name in ['date', 'hour', 'video_time']:
                response[column.name] = str(getattr(row, column.name))
            else:
                response[column.name] = getattr(row, column.name)
    return response