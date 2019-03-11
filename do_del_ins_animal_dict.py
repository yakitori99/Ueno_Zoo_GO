from flaskwebapp.flaski.database import db_session
# 自作したclass（テーブルと紐付いているもの）
from flaskwebapp.flaski.models import animal_dict

## テーブルの全データ削除
db_session.query(animal_dict).delete()
db_session.commit()

## レコードをインサート
# idには連番、timestampは日時が勝手に入る(models.pyのデフォルト設定により)
# class名と初期化パラメータを指定して__init__()メソッドでインスタンス作成
c1  = animal_dict('001', 'ニホンザル',
                  'ちのうアニマル',
                  '0.6m', '10kg',
                  '日本では身近な動物。知能が高く、群れを作って生活する。稀に温泉に入っている姿が目撃される。',
                  '<a href="https://www.pokemon.jp/zukan/detail/056.html" target="_blank" rel="noopener noreferrer">マンキー <i class="fas fa-external-link-alt"></i></a>')
c2  = animal_dict('002', 'パンダ',
                  'しろくろアニマル',
                  '1.2m', '120kg',
                  '上野動物園の人気者。好物は竹。1日の半分は食事をして、残りの半分は寝て過ごしている。',
                  '<a href="https://www.pokemon.jp/zukan/detail/674.html" target="_blank" rel="noopener noreferrer">ヤンチャム <i class="fas fa-external-link-alt"></i></a>')
c3  = animal_dict('003', 'カワウソ',
                  'およぎアニマル',
                  '0.5m', '4kg',
                  '哺乳類であるが泳ぎが得意で、水中に6～8分ほど潜っていることができる。毛皮に空気を溜め込み、水に浮くこともできるらしい。',
                  '<a href="https://www.pokemon.jp/zukan/detail/418.html" target="_blank" rel="noopener noreferrer">ブイゼル <i class="fas fa-external-link-alt"></i></a>')
c4  = animal_dict('004', 'ゴリラ',
                  'きんにくアニマル',
                  '1.6m', '160kg',
                  '力が非常に強く、握力は500kg以上。知能も高く、群れを作って生活する。デリケートな性格で、下痢になりやすい。',
                  '<a href="https://www.pokemon.jp/zukan/detail/289.html" target="_blank" rel="noopener noreferrer">ケッキング <i class="fas fa-external-link-alt"></i></a>')
c5  = animal_dict('005', 'キリン',
                  'くびながアニマル',
                  '4.2m', '800kg',
                  '首の長さは2m以上。まつ毛も長い。臆病な性格で、野生では睡眠時間は1日1時間程度。',
                  '<a href="https://www.pokemon.jp/zukan/detail/203.html" target="_blank" rel="noopener noreferrer">キリンリキ <i class="fas fa-external-link-alt"></i></a>')
c6  = animal_dict('006', 'カンガルー',
                  'ふくろアニマル',
                  '1.5m', '80kg',
                  'ジャンプ力があり、最高時速70kmほどで移動することができる。後ろには進めない。メスはお腹の袋で子育てをする。お腹の袋はとても臭いらしい。',
                  '<a href="https://www.pokemon.jp/zukan/detail/115.html" target="_blank" rel="noopener noreferrer">ガルーラ <i class="fas fa-external-link-alt"></i></a>')
c7  = animal_dict('007', 'スマトラトラ',
                  'もようアニマル',
                  '2.5m', '140kg',
                  '野生では、インドネシアのスマトラ島にのみ生息しているトラ。群れを作らず、単独で行動する。トラのなかでは最も小さいが、狩りが得意でシカやイノシシ、ワニも食べる。',
                  '<a href="https://www.pokemon.jp/zukan/detail/243.html" target="_blank" rel="noopener noreferrer">ライコウ <i class="fas fa-external-link-alt"></i></a>')
c8  = animal_dict('008', 'アジアゾウ',
                  'ながはなアニマル',
                  '6.0m', '4000kg',
                  '体が大きく、陸上で最大の動物。15～20頭ほどの群れで生活する。知能が高く、鼻で絵を描けるものもいる。',
                  '<a href="https://www.pokemon.jp/zukan/detail/231.html" target="_blank" rel="noopener noreferrer">ゴマゾウ <i class="fas fa-external-link-alt"></i></a>')
c9  = animal_dict('009', 'ケープペンギン',
                  'みずとびアニマル',
                  '0.6m', '3kg',
                  '鳥類であるが飛ぶことはできず、その代わりに水中を飛ぶように泳ぐことができる。野生では唯一アフリカに生息するペンギン。他のペンギンと比べて臆病な性格で、寒いのは苦手。',
                  '<a href="https://www.pokemon.jp/zukan/detail/393.html" target="_blank" rel="noopener noreferrer">ポッチャマ <i class="fas fa-external-link-alt"></i></a>')
c10 = animal_dict('010', 'レッサーパンダ',
                  'ちょくりつアニマル',
                  '0.6m', '5kg',
                  '群れを作らず、単独で生活する。縄張り意識が強く、ライバルに出会うと二本足で立ち、前足を上げて威嚇する。威嚇する姿は、とてもかわいいと言われている。',
                  '<a href="https://www.pokemon.jp/zukan/detail/760.html" target="_blank" rel="noopener noreferrer">キテルグマ <i class="fas fa-external-link-alt"></i></a>')


# insert実行
db_session.add(c1)
db_session.add(c2)
db_session.add(c3)
db_session.add(c4)
db_session.add(c5)
db_session.add(c6)
db_session.add(c7)
db_session.add(c8)
db_session.add(c9)
db_session.add(c10)

# commit実行
db_session.commit()
