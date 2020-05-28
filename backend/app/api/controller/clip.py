import uuid
from typing import List

from flask import request
from flask_restplus import Resource, marshal_with, Namespace

from app.api.error import CustomHTTPError
from app.api.util.http import response_wrapper, success_response
from app.model import Clip, db

clip_ns = Namespace('clip')


class Clips(Resource):
    method_decorators = [response_wrapper]

    @marshal_with(Clip.auto_marshaling_model())
    def get(self) -> List[Clip]:
        channel_name = request.args.get('channel_name', None)
        return Clip.query.filter_by(channel_name=channel_name).all()

    @clip_ns.expect(clip_ns.model('Clip', Clip.auto_marshaling_model()), validate=True)
    @marshal_with(Clip.auto_marshaling_model())
    def post(self) -> Clip:
        payload: dict = request.json
        new_clip = Clip(**payload)
        db.session.add(new_clip)
        db.session.commit()
        return new_clip

    def delete(self):
        clip_id = request.args.get('id')
        clip_id: bytes = uuid.UUID(hex=clip_id).bytes if clip_id else None

        affected_rows: int = Clip.query.filter_by(id=clip_id).delete()
        if affected_rows < 1:
            raise CustomHTTPError('Clip does not exist', 404)
        db.session.commit()
        return success_response


class ChannelClips(Resource):
    method_decorators = [response_wrapper]

    def delete(self):
        channel_name = request.args.get('channel_name')
        Clip.query.filter_by(channel_name=channel_name).delete()
        db.session.commit()
        return success_response
