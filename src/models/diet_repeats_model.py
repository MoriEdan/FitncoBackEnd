# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class DietRepeats(BaseModel):
    __tablename__ = 'diet_repeats'

    id = db.Column(db.BigInteger(), primary_key=True)
    diet_id = db.Column(db.ForeignKey('diets.id'), nullable=False)
    repeat = db.Column(db.Integer, unique=False, nullable=False)
    diets = db.relationship('Diets', primaryjoin='Diets.id == DietRepeats.diet_id')
    images = db.relationship('DietImages', primaryjoin='DietRepeats.id == DietImages.repeat_id', cascade='delete')

    def __init__(self, repeat, diet_id):
        super().__init__()
        self.repeat = repeat
        self.diet_id = diet_id

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'repeat': self.repeat,
            'diet_id': self.diet_id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'repeat': self.repeat,
            'diet_id': self.diet_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
