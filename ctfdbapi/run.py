# WSGI Server for Development
# Use this during development vs. apache. Can view via [url]:8001
# Run using virtualenv. 'env/bin/python run.py'

#https://github.com/coxley/flask-file-structure/blob/master/flask.wsgi

from app import app

#db.create_all()

app.run(host='0.0.0.0', port=5000, debug=True)