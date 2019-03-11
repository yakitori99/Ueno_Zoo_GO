from flaskwebapp.flaski.database import db_session
# 自作したclass（テーブルと紐付いているもの）
from flaskwebapp.flaski.models import registered_animal

## テーブルの全データ削除
db_session.query(registered_animal).delete()
db_session.commit()

# idには連番、timestampは日時が勝手に入る(models.pyのデフォルト設定により)
# class名と初期化パラメータを指定して__init__()メソッドでインスタンス作成
c1 = registered_animal("user1",
                       "/static/images/kangaroo_test1.jpg",
                       "006",
                       0.9111)

c2 = registered_animal("user1",
                       "/static/images/penguin_test1.jpg",
                       "009",
                       0.8111)


db_session.add(c1)  # insert実行
db_session.add(c2)

db_session.commit()
