"""
This script runs the flaskwebapp application using a development server.
"""

from flaskwebapp import app
import os

if __name__ == '__main__':
    # 環境変数'PORT'があればheroku/AWSとみなし、そのポートを使う&httpsを使う
    port_env = os.getenv('PORT')
    if port_env is None:
        # debug用
        port_num = 8080
        app.config['use_https'] = False
        app.run(debug=True,  host='0.0.0.0', port=port_num, threaded=True)
    else:
        # heroku/AWS用
        port_num = int(port_env)
        app.config['use_https'] = True
        app.run(debug=False, host='0.0.0.0', port=port_num, threaded=True)