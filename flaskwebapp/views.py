# coding: utf-8
from flask import render_template, request, redirect, session, url_for
import os
import numpy as np
import datetime
import math

from io import BytesIO

# ファイル一覧取得用
import glob

# 画像操作用
import cv2

# for GOOGLE_CLOUD_VISION_API
import requests
import base64
import json

# ランダム文字列生成用
import random
import string

# DB操作用
from sqlalchemy import desc, distinct, text

## ローカルライブラリをimport
# __init__.pyのapp(flaskオブジェクト)をimport
from flaskwebapp import app

from flaskwebapp.flaski.database import db_session
from flaskwebapp.flaski.models import animal_dict, registered_animal

import flaskwebapp.logger as logger  # for test
log = logger.Logger('test_log')  # for test
# log.debug('test_debug_log')  # for debug

import flaskwebapp.config as conf

### 設定読み込み
# ファイルアップロード先フォルダ
UPLOAD_FOLDER = conf.UPLOAD_FOLDER
# NO IMAGEのファイルパス
NO_IMAGE_PATH = conf.NO_IMAGE_PATH
# アップロードを許可する拡張子
ALLOWED_EXTENSIONS = conf.ALLOWED_EXTENSIONS

# getするしきい値
SCORE_THRESH = conf.SCORE_THRESH

# animal_name:animal_no(3桁)
ANIMAL_NAME_NO_DICT = conf.ANIMAL_NAME_NO_DICT

## for GoogleCloudVisionAPI start
GOOGLE_CLOUD_VISION_API_URL = conf.GOOGLE_CLOUD_VISION_API_URL
GCV_API_KEY = conf.GCV_API_KEY
# GOOGLE_CLOUD_VISION_APIのdetectionのtype, 結果jsonのkey名称
GCV_DETECTION_TYPE = conf.GCV_DETECTION_TYPE
GCV_DETECTION_RESULT_NAME = conf.GCV_DETECTION_RESULT_NAME
# APIから取得する最大数
GCV_API_NUM_MAX_RESULTS = conf.GCV_API_NUM_MAX_RESULTS
## for GoogleCloudVisionAPI end

## for Paginage
NUM_PER_PAGE_PHOTO_LIBRARY = conf.NUM_PER_PAGE_PHOTO_LIBRARY

### 関数定義
def get_scheme():
    # httpかhttpsのどちらを使うか、configの値によって設定
    if app.config['use_https'] is True:
        scheme = 'https'
    else:
        scheme = 'http'
    return scheme

def convert_file_to_b64_string(file_path):
    '''
    ファイルをbase64にエンコードする
    # GOOGLE_CLOUD_VISION_APIへ渡すときの指定がbase64 encodeのため
    '''
    with open(file_path, "rb") as f:
        img_byte = f.read()
    return base64.b64encode(img_byte)


def request_cloud_vison_api(image_base64):
    '''
    base64エンコード済の画像ファイルを受け取り、Google Cloud Vision APIを用いてオブジェクトの推論を行う関数
    [in]   :base64エンコード済の画像ファイル
    [out1] :推論結果の確信度（result['score']）--float32
    [out2] :推論結果のanimal_name（result['name']）--str
    '''
    api_url = GOOGLE_CLOUD_VISION_API_URL + '?key='+ GCV_API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_base64.decode('utf-8')
            },
            'features': [{
                'maxResults': GCV_API_NUM_MAX_RESULTS,
                'type': GCV_DETECTION_TYPE,
            }]
        }]
    })
    # API POST
    try:
        res = requests.post(api_url, data=req_body)
    except Exception as e:
        log.debug("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    res_dict = res.json()

    animal_name = ''
    max_score = 0
    # 結果が存在しない場合はデフォルト値をリターン
    if 'responses' in res_dict.keys() and len(res_dict['responses']) >= 1 and GCV_DETECTION_RESULT_NAME in res_dict['responses'][0].keys():
        results = res_dict['responses'][0][GCV_DETECTION_RESULT_NAME]
        # 結果が存在する場合、ANIMAL_NAME_NO_DICTに名前がある and scoreが最大のアニマルをgetする
        for result in results:
            if result['name'] in ANIMAL_NAME_NO_DICT.keys():
                if result['score'] > max_score:
                    animal_name = result['name']
                    max_score = result['score']

    return max_score, animal_name


def allowed_file(filename):
    '''
    受け取ったファイル名の右端が、. + 「許可した拡張子」の場合のみTrueを返す関数
    [in]  :filename(文字列)
    [out] :True / False
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_random_string(num_of_chara=16):
    '''
    半角英数を組み合わせて、指定した長さのランダム文字列を生成して返す関数
    [in]  :生成するランダム文字列の長さ（int型）
    [out] :生成したランダム文字列(str型)
    '''
    # string.ascii_letters:半角英字（大文字or小文字）
    # string.digits:半角数字
    random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(num_of_chara)])
    return random_str


def resize_img(img, max_length=800):
    '''
    画像データ（numpy.ndarray型）を受け取り、長いほうの辺がmax_lengthを超える場合は、
    縦横比を維持したまま長いほうの辺がmax_lengthになるようリサイズして返す関数
    [in]  :画像データ（numpy.ndarray型）
    [out] :リサイズ後の画像データ(numpy.ndarray型)
    '''
    # 元のサイズを保存
    org_height, org_width = img.shape[:2]
    # height, widthのうち長い方を取得
    if org_height >= org_width:
        big_side = org_height
    else:
        big_side = org_width
    # 長いほうの辺がmax_lengthを超える場合はリサイズ（圧縮）する
    if big_side > max_length:
        # 長いほうの辺をmax_lengthに縮小する縮尺を算出
        resized_scale = max_length / big_side
        # リサイズ後のheight, widthの長さを算出
        resized_height = int(org_height * resized_scale)
        resized_width = int(org_width * resized_scale)
        # ファイルをリサイズ（圧縮）
        resized_img = cv2.resize(img, (resized_width, resized_height))
    else:
        resized_img = img

    return resized_img


def get_distinct_user_names():
    '''
    重複しないuser_nameのリスト(user_nameの昇順)を、registered_animalテーブルから取得して返す
    [in]  :なし
    [out] :重複しないuser_nameのリスト
    '''
    # 重複を除いてユーザ名(register_user_id)を全て取得
    records = db_session.query(distinct(registered_animal.register_user_id)
                               ).order_by(registered_animal.register_user_id)

    # リストへ格納
    user_names = []
    for record in records:
        user_names.append(record[0])

    return user_names


def get_animal_dict_order_by_animal_no():
    '''
    animal_dict から全件をanimal_no順に取得し、辞書をリストに格納し、リストを返す
    [in]  :なし
    [out] :animal_dict全件（辞書型を要素に持つリスト）
    '''
    records = db_session.query(animal_dict).order_by(animal_dict.animal_no)

    contents = []  # このリストの各行に、animal_dictの辞書型データを入れる
    for record in records:
        mydict = {}
        mydict.setdefault('animal_no',    record.animal_no)
        mydict.setdefault('animal_name',  record.animal_name)
        mydict.setdefault('animal_type',  record.animal_type)
        mydict.setdefault('body_length',  record.body_length)
        mydict.setdefault('weight',       record.weight)
        mydict.setdefault('description',  record.description)
        mydict.setdefault('animal_a_tag', record.animal_a_tag)
        contents.append(mydict)

    return contents


def get_one_registered_animal_by_animal_no_and_register_user_id(animal_no, user_id):
    '''
    registered_animal からanimal_noとregister_user_idを条件にデータを検索し、timestampが最新の1件を辞書型で返す
    検索結果が0件の場合は、'No Data'という情報の入った辞書型を返す
    [in1] :animal_no
    [in2] :user_id
    [out] :registered_animal 1件（辞書型、中身は全てstr）
    '''
    record = db_session.query(registered_animal
                              ).filter(text('animal_no = :animal_no and register_user_id = :user_id')
                                       ).params(animal_no=animal_no, user_id=user_id
                                                ).order_by(desc(registered_animal.timestamp)).first()

    mydict = {}
    if record is None:
        mydict.setdefault('register_user_id', 'No Data')
        mydict.setdefault('filepath',          NO_IMAGE_PATH)
        mydict.setdefault('confidence',       'No Data')
        mydict.setdefault('animal_no',        'No Data')
        mydict.setdefault('timestamp',        'No Data')
    else:
        mydict.setdefault('register_user_id', record.register_user_id)
        mydict.setdefault('filepath',         record.filepath)
        mydict.setdefault('confidence',       '{:.2%}'.format(record.confidence))
        mydict.setdefault('animal_no',        record.animal_no)
        mydict.setdefault('timestamp',        record.timestamp.strftime('%Y/%m/%d'))

    return mydict


def get_registered_animals_by_animal_no(animal_no, page):
    '''
    registered_animal からanimal_noを条件にデータを検索し、
    timestampの降順にソートして、辞書をリストに格納してリストを返す
    -- 1ページあたりの表示件数分のみ取得する
    ※検索結果が0件の場合はとりあえず考慮しない（初期データとして、必ず1アニマル1件以上登録するため）
    [in1] :animal_no
    [in2] :page--表示するページ番号(int, 1スタート)
    [out1] :registered_animalの複数件（辞書型を要素に持つリスト、中身は全てstr））
    [out2] :num_records--DB内の一致するレコード数
    '''
    # 1ページあたりの表示件数
    num_per_page = NUM_PER_PAGE_PHOTO_LIBRARY

    records = db_session.query(registered_animal
                               ).filter(text('animal_no = :animal_no')
                                        ).params(animal_no=animal_no
                                                 ).order_by(desc(registered_animal.timestamp)
                                                            ).limit(num_per_page
                                                                    ).offset((page-1)*num_per_page)

    contents = []  # このリストの各行に、registered_animalの辞書型データを入れる
    for record in records:
        mydict = {}
        mydict.setdefault('id',               record.id)
        mydict.setdefault('register_user_id', record.register_user_id)
        mydict.setdefault('filepath',         record.filepath)
        mydict.setdefault('confidence',       '{:.2%}'.format(record.confidence))
        mydict.setdefault('animal_no',        record.animal_no)
        mydict.setdefault('timestamp',        record.timestamp.strftime('%Y/%m/%d'))
        contents.append(mydict)

    # 件数を取得
    num_records = db_session.query(registered_animal
                                   ).filter(text('animal_no = :animal_no')
                                            ).params(animal_no=animal_no
                                                     ).count()
    return contents, num_records


def get_registered_animals_all(page):
    '''
    registered_animal から全てのデータを検索し、
    timestampの降順にソートして、辞書をリストに格納してリストを返す
    -- 1ページあたりの表示件数分のみ取得する
    ※検索結果が0件の場合はとりあえず考慮しない（初期データとして、必ず1アニマル1件以上登録するため）
    [in]  :page--表示するページ番号(int, 1スタート)
    [out1] :registered_animalの複数件（辞書型を要素に持つリスト、中身は全てstr））
    [out2] :num_records--DB内の一致するレコード数
    '''
    # 1ページあたりの表示件数
    num_per_page = NUM_PER_PAGE_PHOTO_LIBRARY
    # 表示するページの要素を取得
    records = db_session.query(registered_animal
                               ).order_by(desc(registered_animal.timestamp)
                                          ).limit(num_per_page
                                                  ).offset((page-1)*num_per_page)

    contents = []  # このリストの各行に、registered_animalの辞書型データを入れる
    for record in records:
        mydict = {}
        mydict.setdefault('id',               record.id)
        mydict.setdefault('register_user_id', record.register_user_id)
        mydict.setdefault('filepath',         record.filepath)
        mydict.setdefault('confidence',       '{:.2%}'.format(record.confidence))
        mydict.setdefault('animal_no',        record.animal_no)
        mydict.setdefault('timestamp',        record.timestamp.strftime('%Y/%m/%d'))
        contents.append(mydict)

    # 件数を取得
    num_records = db_session.query(registered_animal).count()

    return contents, num_records


### URLアクセス時の処理定義
## / (Home) # TOPページとAboutページを統合した
@app.route('/')
def home():
    return render_template('about.html')


## GET画面 -> got, escapedへ遷移する
@app.route('/get', methods=['GET', 'POST'])
def get_animal():
    if request.method == 'POST':
        # HTTPリクエストから、input type="file" のオブジェクト（ファイルデータの入った辞書）を取り出す
        file = request.files['file']
        if file and allowed_file(file.filename):
            # ランダム文字列 + 元の拡張子でランダムファイル名を生成
            random_filename = create_random_string(20) + '.' + file.filename.rsplit('.', 1)[1]

            # ファイルパスを文字列として保存
            file_path = os.path.join(UPLOAD_FOLDER, random_filename)

            ## ファイルを圧縮
            # BytesIOで読み込んでOpenCVで扱える型にする
            f = file.stream.read()
            binary_file = BytesIO(f)
            file_bytes = np.asarray(bytearray(binary_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            # ファイルをリサイズ（圧縮）
            resized_img = resize_img(img, 800)

            # ファイルを保存
            # ランダム文字列なので重複はほぼありえない。（なお、もし同名のファイルがある場合、上書き保存する挙動）
            cv2.imwrite('flaskwebapp'+ file_path, resized_img)

            # Google Cloud Vision APIを用いた推論
            image_b64 = convert_file_to_b64_string('flaskwebapp'+ file_path)
            confidence, animal_name = request_cloud_vison_api(image_b64)

            ## toast(≒メッセージウインドウ)を表示するjavascript
            if animal_name!='':
                ## get animal
                animal_no = ANIMAL_NAME_NO_DICT[animal_name]

                # 推論結果のラベルを用いて、DBからアニマルデータ検索
                record = animal_dict.query.filter_by(animal_no=animal_no).first()

                # 辞書型にアニマルデータを入れる
                content = {}
                content.setdefault('animal_no',    record.animal_no)
                content.setdefault('animal_name',  record.animal_name)
                content.setdefault('animal_type',  record.animal_type)
                content.setdefault('body_length',  record.body_length)
                content.setdefault('weight',       record.weight)
                content.setdefault('description',  record.description)
                content.setdefault('animal_a_tag', record.animal_a_tag)
                
                if confidence >= SCORE_THRESH:
                    # toast表示
                    toast_js = "M.toast({html: 'やったー！', classes: 'amber darken-4'});" \
                               "M.toast({html: '" + record.animal_name \
                               + " をゲットした！', classes: 'amber darken-4'});"

                    return render_template('got_animal.html', file_path=file_path,
                                           content=content, confidence=confidence, toast_js=toast_js)
                else:
                    # escaped(animel_nameはある)
                    toast_js = "M.toast({html: '逃げられた・・・', classes: 'grey darken-1'});"

                    return render_template('escaped.html', file_path=file_path,
                                           content=content, confidence=confidence, toast_js=toast_js)
            
            else:
                ## escaped(animel_nameなし)
                # 辞書型にアニマルデータを入れる
                content = {}
                content.setdefault('animal_no',   '―')
                content.setdefault('animal_name', '')

                toast_js = "M.toast({html: '逃げられた・・・', classes: 'grey darken-1'});"

                return render_template('escaped.html', file_path=file_path,
                                       content=content, confidence=confidence, toast_js=toast_js)


        else:
            # 許可していない拡張子の場合（クライアントサイドでもjsでチェックするが、念の為サーバサイドでもチェックする）
            # toast(メッセージウインドウ)を表示するjavascript
            toast_js = "M.toast({html: '許可されていないファイル拡張子です。', classes: 'grey darken-1'});" \
                       "M.toast({html: 'アップロード可能な拡張子はjpg, jpeg, png, bmpです。'," \
                       " classes: 'grey darken-1'});"

            return render_template('get_animal.html', toast_js=toast_js)

    else:
        # POSTでない場合
        return render_template('get_animal.html')


## アニマル図鑑へ登録
@app.route('/register', methods=['POST'])
def register():
    # formからデータを取得
    register_user_id = request.form['register_user_id']
    filepath         = request.form['register_filepath']
    animal_no        = request.form['animal_no']
    confidence       = float(request.form['confidence'])
    # UTCを日本時間に変換(処理するPC/サーバの時刻に関わらず、日本時間を取得)
    timestamp = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

    # インサート
    record = registered_animal(register_user_id, filepath, animal_no, confidence, timestamp)
    db_session.add(record)
    db_session.commit()

    # toast(≒メッセージウインドウ)を表示するjavascript
    toast_js = "M.toast({html: '" + request.form['animal_name'] \
               + " を図鑑に登録しました！', classes: 'amber darken-4'});"
    # toast_jsをセッションに格納
    session['toast_js_registered'] = toast_js

    # 登録したユーザ名の、アニマル図鑑画面へ遷移
    return redirect(url_for('my_animal_index', _external=True, _scheme=get_scheme(),
                            selected_user_name=register_user_id))


### アニマル図鑑　ニックネーム選択（ユーザ選択）
@app.route('/my_animal_index')
def my_animal_search():
    ## user_namesのselectリスト生成用データ
    # 重複を除いてユーザ名(register_user_id)を全て取得し、リストへ格納
    user_names = get_distinct_user_names()

    return render_template('my_animal_search.html', user_names=user_names)


## アニマル図鑑　ユーザ別の図鑑
@app.route('/my_animal_index/<selected_user_name>')
def my_animal_index(selected_user_name=None):
    # URLの末尾(/より後ろ)からselected_user_name（ニックネーム）を取得
    # animal_dictのリストを取得
    dict_animals = get_animal_dict_order_by_animal_no()
    # 指定したユーザの登録した全アニマルを1件ずつ取得（存在しないアニマルは'No Data'）
    my_animals = []
    for dict_animal in dict_animals:
        my_animal = get_one_registered_animal_by_animal_no_and_register_user_id(dict_animal['animal_no'],
                                                                                selected_user_name)
        my_animals.append(my_animal)

    ## (捕まえた数)/(アニマル全種類数)の文字列を生成
    # my_animalsリスト（中身は辞書）から、timestampだけのリストを生成 # リスト内包表記とgetメソッドで、任意のキーの値を抽出してリスト化
    timestamp_list = [my_animal.get('timestamp') for my_animal in my_animals]
    # アニマル全種類数
    num_all_animal = len(timestamp_list)
    # 捕まえた数
    num_got_animal = num_all_animal - timestamp_list.count("No Data")
    # (捕まえた数)/(アニマル全種類数)の文字列
    str_num_animal = str(num_got_animal) + "/" + str(num_all_animal)

    ## user_namesのselectリスト生成用データ
    # 重複を除いてユーザ名(register_user_id)を全て取得し、リストへ格納
    user_names = get_distinct_user_names()

    # セッションからメッセージを取得し、セッションから削除
    toast_js = session.get('toast_js_registered')  # 存在しない場合はNoneが返される
    session.pop('toast_js_registered', None)
    # セッションにメッセージが存在しなかった場合は、Noneではなく空文字を返す
    if toast_js is None:
        toast_js = ""

    return render_template('my_animal_index.html',
                           animals_data=zip(dict_animals, my_animals),
                           str_num_animal=str_num_animal, num_got_animal=num_got_animal,
                           user_names=user_names, selected_user_name=selected_user_name,
                           toast_js=toast_js)


### フォトライブラリ　アニマル選択
@app.route('/photo_library')
def photo_library_search():
    # フォトライブラリは、デフォルトで全アニマルを検索する
    # - '/photo_library'への遷移は'/photo_library/ALL/1'へリダイレクトする
    return redirect(url_for('photo_library_show', _external=True, _scheme=get_scheme(),
                            selected_animal_no='ALL', page='1'))


### フォトライブラリ　アニマル表示
@app.route('/photo_library/<selected_animal_no>/<page>')
def photo_library_show(selected_animal_no=None, page=1):
    page = int(page)

    ## animalsのselectリスト生成用データ
    # animal_dictのリストを取得
    dict_animals = get_animal_dict_order_by_animal_no()

    # URLの末尾(/より後ろ)から'ALL'またはselected_animal_no（アニマルNo）を取得
    if selected_animal_no == 'ALL':
        # 'ALL'ならば全アニマルを取得
        registered_animals, num_records = get_registered_animals_all(page)

    else:
        # アニマルNoをキーにでregistered_animalテーブルを検索
        registered_animals, num_records = get_registered_animals_by_animal_no(selected_animal_no, page)
    
    # 表示するページ番号
    num_pages = math.ceil(num_records/NUM_PER_PAGE_PHOTO_LIBRARY)
    # ページネーションは5つまで表示する
    if num_pages <= 5:
        p_start = 1
        p_end   = num_pages
    else:
        if page <= 3:
            p_start = 1
            p_end   = 5
        elif num_pages-2 <= page:
            p_start = num_pages-4
            p_end   = num_pages
        else:
            p_start = page-2
            p_end   = page+2

    return render_template('photo_library_show.html',
                           dict_animals=dict_animals, registered_animals=registered_animals,
                           selected_animal_no=selected_animal_no,
                           page=page, num_pages=num_pages,
                           p_start=p_start, p_end=p_end)


## publoc_photos（メニューにはないページとする。存在する全画像を表示する）
@app.route('/public_photos')
def public_photos():
    file_paths = []
    file_names = glob.glob('flaskwebapp/static/images/*')
    for file_name in file_names:
        good_file_path = file_name.replace('flaskwebapp/', '')
        # 許可された拡張子のファイルのみ処理
        if allowed_file(good_file_path):
            file_paths.append(good_file_path)
    ## 説明：
    # pythonのコマンド実行時は、runserver.pyの階層がカレントディレクトリになっている
    # →パス指定は、flaskwebapp/…から始める必要がある
    # webからファイル参照などする場合は、views.pyの階層がカレントディレクトリになっている(通常のflaskWebアプリと同じ)
    # →パス指定は、static/…から始める必要がある

    return render_template('public_photos.html', file_paths=file_paths)


## error handling 500(Internal Server Error)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500
