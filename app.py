# app.py
import os
from flask import Flask
#
app = Flask(__name__)
#
@app.route("/")
def hello():
    return "Hello World!"
#
# run after setup
def main():
    """main
    """
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port)
#
if __name__ == '__main__':
    main()
#
# EOF