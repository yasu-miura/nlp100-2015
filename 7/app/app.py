# coding:utf-8
from flask import Flask, render_template, request
import artistsdao


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/artist", methods=["POST"])
def artist():
    name = request.form["name"]
    another_name = request.form["another-name"]
    res = ""
    if another_name == "":
        artists = artistsdao.get_artists_by_name(name)
        for artist in artists:
            res += str(artist) + "<br><br>"
    elif name == "":
        artists = artistsdao.get_artists_by_another_name(another_name)
        for artist in artists:
            res += str(artist) + "<br><br>"
    else:
        artists = artistsdao.get_artists_by_name_and_another_name(name, another_name)
        for artist in artists:
            res += str(artist) + "<br><br>"
    return res


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
