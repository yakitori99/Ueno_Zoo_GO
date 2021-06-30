"""
This script runs the flaskwebapp application using a development server.
"""

from flaskwebapp import app
import os

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=80, threaded=True)  # debug用
    # app.run(debug=False, host='0.0.0.0', port=80, threaded=True)  # 本番用
    
    ## heroku本番用
    # 環境変数'PORT'があれば、そのポートでrun
    port_env = os.getenv('PORT')
    if port_env is None:
        port_num = 80
    else:
        port_num = int(port_env)
    app.run(debug=False, host='0.0.0.0', port=port_num, threaded=True)