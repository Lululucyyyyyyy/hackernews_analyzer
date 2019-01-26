from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def resume():
	return render_template('analyzer.py')

if __name__ == "__main__":
	app.run()
