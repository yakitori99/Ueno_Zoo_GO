"""
This script runs the flaskwebapp application using a development server.
"""

from flaskwebapp import app
import os

if __name__ == '__main__':
    # 環境変数'PORT'があればherokuとみなし、そのポートでrun
    port_env = os.getenv('PORT')
    if port_env is None:
        # debug用
        port_num = 80
        app.run(debug=True,  host='0.0.0.0', port=port_num, threaded=True)
    else:
        # heroku用
        port_num = int(port_env)
        app.run(debug=False, host='0.0.0.0', port=port_num, threaded=True)