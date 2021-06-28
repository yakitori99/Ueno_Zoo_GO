from flaskwebapp.flaski.database import db_session
# 自作したclass（テーブルと紐付いているもの）
from flaskwebapp.flaski.models import registered_animal

## テーブルの全データ削除
db_session.query(registered_animal).delete()
db_session.commit()

# idには連番、timestampは日時が勝手に入る(models.pyのデフォルト設定により)
# class名と初期化パラメータを指定して__init__()メソッドでインスタンス作成
c1 = registered_animal("yasu",
                       "/static/images/006_kangaroo_1.jpg",
                       "006",
                       0.8902)

c2 = registered_animal("yasu",
                       "/static/images/009_penguin_1.jpg",
                       "009",
                       0.8661)


db_session.add(c1)  # insert実行
db_session.add(c2)

db_session.commit()
