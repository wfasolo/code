import time

import templates.previsao as prevv
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect

app = Flask(__name__, template_folder='templates')

wsgi_app = app.wsgi_app


@app.route('/')
def hello_world():
    return 'Página inicial!'


@app.route("/teste")
def index():
    return render_template('temp-plot.html')
    #redirect("https://www.pythonanywhere.com/user/wfasolo/files/home/wfasolo/temp-plot.html", code=302)


for i in range(10):

    prevv.prev()
    time.sleep(30)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
