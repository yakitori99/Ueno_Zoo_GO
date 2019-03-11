# coding: utf-8
## 概要：DBの初期設定を行うためのファイル
# 参考：https://qiita.com/yshi12/items/9502c6232e96d7dfa29d
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# dbファイル名と保存先を指定
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
# sqliteを指定して、テーブルのcreateを指定。
engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=True)

## Sessionの作成
# bindにテーブルcreateを指定。
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine
                                         )
                            )
# declarative_baseのインスタンス生成。
Base = declarative_base()
# 実行用のセッション格納？
Base.query = db_session.query_property()


## FlaskアプリがSQLAlchemyを使えるようにするための初期化
def init_db():
    Base.metadata.create_all(bind=engine)
