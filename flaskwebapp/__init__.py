"""
The flask application package.
"""
import os
from flask import Flask
## appという名前でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

# flaskのsessionを利用するためにsecret_keyを指定
app.secret_key = os.urandom(24)

## flaskwebappフォルダのviwes.pyをインポート
## ※このインポートは、Flaskオブジェクトのインスタンス化の後に行う。（でないとエラーになるとのこと。）
import flaskwebapp.views
