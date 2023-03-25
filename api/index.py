import flask, pymongo
from flask import render_template, request
from os import environ as env

app = flask.Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

    client = pymongo.MongoClient(env['URI'])
    db = client.get_database("books")
    coll = db.get_collection("book")
    Title = request.form['Title']
    Status = request.form['Status']
    Genre = request.form['Genre']
    Rating = request.form['Rating']
    Review = request.form['Review']
    if Status == '0':
        Rating = "-"
        Review = "-"

    coll.insert_one({"Title": Title, "Status": Status, "Genre": Genre, "Rating": Rating, "Review": Review})

    client.close()

    return render_template("index.html")

@app.route("/view")
def view(): 

    client = pymongo.MongoClient(env['URI'])
    db = client.get_database("books")
    coll = db.get_collection("book")
    cur = coll.find()

    books = []
    for row in cur:
        book = []
        book.append(row['Title'])
        if row['Status'] == 0:
            book.append("Reading")
        else:
            book.append("Read")
        book.append(row['Genre'])
        book.append(row['Rating'])
        book.append(row['Review'])
        books.append(book)
    client.close()
    return render_template("view.html", books=books)

if __name__ == '__main__':
    app.run()