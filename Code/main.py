from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html', **{'greeting':'Hello from Flask!'})

if __name__ == '__main__':
    app.run(debug=True)
