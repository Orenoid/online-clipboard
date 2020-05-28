import uuid

from flask_restplus import fields
from sqlalchemy.sql import sqltypes


def generate_uuid() -> bytes:
    return uuid.uuid4().bytes



class MarshalMixin:
    # 用来给sqlalchemy模型自动生成序列化规则，供flask-restplus使用
    # 偷懒用的，不放心还是可以直接手写模型，没有影响

    type_mapper = {
        sqltypes.String: fields.String,
        sqltypes.TEXT: fields.String,
        sqltypes.Integer: fields.Integer,
        sqltypes.Numeric: fields.Float,
    }

    @classmethod
    def auto_marshaling_model(cls) -> dict:
        return {
            column.name: cls.type_mapper[type(column.type)] for column in cls.__table__.c
        }
