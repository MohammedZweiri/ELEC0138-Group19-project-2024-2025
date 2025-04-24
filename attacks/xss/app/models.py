from . import db


class CollectedData(db.Model):
    """Model for storing collected data from XSS attack."""
    __tablename__ = 'collected_data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50), nullable=False)
    current_user = db.Column(db.String(100), nullable=True)
    access_token = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<CollectedData id={self.id}, user={self.current_user}>'

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'current_user': self.current_user,
            'access_token': self.access_token,
        }


class AppState(db.Model):
    """Model representing application state."""
    __tablename__ = 'app_state'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<AppState key={self.key}, value={self.value}>'
