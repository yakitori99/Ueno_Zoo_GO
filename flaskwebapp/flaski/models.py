# coding: utf-8
from sqlalchemy import Column, Integer, Float, String, DateTime
# 自分で作ったdatabase.pyから読み込み
from flaskwebapp.flaski.database import Base
from datetime import datetime as dt


# Tableの情報
class animal_dict(Base):
    ## Table Name
    __tablename__ = "animal_dict"
    ## Column情報を設定
    # primary_key=Trueの場合、初期化時に勝手に連番が入る。もし連番にはしたくない場合は、autoincrementをFalseで指定する。
    id                  = Column(Integer, primary_key=True)
    animal_no           = Column(String, unique=False)  # 001-999 左0埋め3ケタにする
    animal_name         = Column(String, unique=False)
    animal_type         = Column(String, unique=False)
    body_length         = Column(String, unique=False)  # 体長
    weight              = Column(String, unique=False)  # 重さ
    description         = Column(String, unique=False)  # 概要、説明
    animal_a_tag        = Column(String, unique=False)  # 似ているポケモン　として表示するリンク(aタグ)
    timestamp           = Column(DateTime, default=dt.now())

    def __init__(self, animal_no=None, animal_name=None, animal_type=None, body_length=None,
                 weight=None, description=None, animal_a_tag=None, timestamp=None):
        '''デフォルトの値を設定'''
        self.animal_no = animal_no
        self.animal_name = animal_name
        self.animal_type = animal_type
        self.body_length = body_length
        self.weight = weight
        self.description = description
        self.animal_a_tag = animal_a_tag
        self.timestamp = timestamp


class registered_animal(Base):
    ## Table Name
    __tablename__ = "registered_animal"
    ## Column情報を設定
    # primary_key=Trueの場合、初期化時に勝手に連番が入る。もし連番にはしたくない場合は、autoincrementをFalseで指定する。
    id                  = Column(Integer, primary_key=True)
    register_user_id    = Column(String, unique=False)
    filepath            = Column(String, unique=False)
    animal_no           = Column(String, unique=False)  # 001-999 左0埋め3ケタにする
    confidence          = Column(Float, unique=False)
    timestamp           = Column(DateTime, default=dt.now())

    def __init__(self, register_user_id=None, filepath=None, animal_no=None,
                 confidence=None, timestamp=None):
        '''デフォルトの値を設定'''
        self.register_user_id = register_user_id
        self.filepath = filepath
        self.animal_no = animal_no
        self.confidence = confidence
        self.timestamp = timestamp
