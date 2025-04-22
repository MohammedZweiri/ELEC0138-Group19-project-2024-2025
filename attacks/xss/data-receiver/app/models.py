from datetime import datetime

from . import db


class CollectedData(db.Model):
    """Model for storing collected data from XSS attack."""
    __tablename__ = 'collected_data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(30), nullable=False,
                          default=lambda: datetime.now().isoformat())
    current_user = db.Column(db.String(100))
    access_token = db.Column(db.String(255))

    def __repr__(self):
        return f'<CollectedData {self.id}>'

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'current_user': self.current_user,
            'access_token': self.access_token,
        }
