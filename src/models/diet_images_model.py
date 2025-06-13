# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class DietImages(BaseModel):
    __tablename__ = 'diet_images'

    id = db.Column(db.BigInteger(), primary_key=True)
    repeat_id = db.Column(db.ForeignKey('diet_repeats.id'), nullable=False)
    image = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, image, repeat_id):
        super().__init__()
        self.image = image
        self.repeat_id = repeat_id

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'image': self.image,
            'repeat_id': self.repeat_id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'repeat_id': self.repeat_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
