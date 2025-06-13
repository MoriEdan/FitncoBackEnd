# -*- coding: utf-8 -*-
from flask_seeder import Seeder
from src.models.users_model import Users
import json
from src.utils.hash_util import hash_bcrypt


class UserSeeder(Seeder):

    def run(self):
        try:
            with open('seeds/jsons/user.json') as json_file:
                data = json.load(json_file)
            for row in data:
                db_row = Users(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    password=hash_bcrypt(row['password']),
                    role_id=row['role_id'],
                    gender=row['gender'],
                    phone=row['phone']
                )
                self.db.session.add(db_row)
        except Exception as e:
            print(e)
