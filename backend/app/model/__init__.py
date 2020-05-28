import uuid

from flask_sqlalchemy import SQLAlchemy
from flask_restplus import fields
from .util import generate_uuid, MarshalMixin

db = SQLAlchemy()


class Clip(db.Model, MarshalMixin):
    physical_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.BINARY, unique=True, default=generate_uuid, nullable=False)
    text = db.Column(db.TEXT, nullable=False)
    channel_name = db.Column(db.String(255))

    @classmethod
    def auto_marshaling_model(cls) -> dict:
        class ClipId(fields.Raw):
            def format(self, value: bytes) -> str:
                return uuid.UUID(bytes=value).hex

        return {
            'id': ClipId(readonly=True),
            'text': fields.String(required=True),
            'channel_name': fields.String(required=False)
        }
