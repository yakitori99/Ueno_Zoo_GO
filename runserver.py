"""
This script runs the flaskwebapp application using a development server.
"""

from flaskwebapp import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)  # debug用
    # app.run(debug=False, host='0.0.0.0', port=80, threaded=True)  # 本番用
