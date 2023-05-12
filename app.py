import flask, pymongo
from flask import render_template, request, redirect, url_for
from os import environ as env

app = flask.Flask(__name__)

def gen(cur):
    books = []
    for row in cur:
        book = {}
        book['Title'] = row['Title']
        if row['Status'] == '0':
            book['Status'] = "Reading"
        else:
            book['Status'] = "Read"
        book['Genre'] = row['Genre']
        book['Rating'] = row['Rating']
        book['Review'] = row['Review']
        books.append(book)
    return books
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
    books = gen(cur)
    client.close()

    return render_template("view.html", books=books)
    #return render_template("view.html", books=books, message=message['content'])

@app.route("/delete/<Title>", methods=['POST'])
def delete(Title):
    client = pymongo.MongoClient(env['URI'])
    db = client.get_database("books")
    coll = db.get_collection("book")
    coll.delete_one({'Title': Title})
    cur = coll.find()

    books = gen(cur)
    client.close()
    return render_template("view.html", books=books)

@app.route("/edit/<Title>", methods=['GET', 'POST'])
def edit(Title):
    if request.method == 'GET':
        return render_template("edit.html", Title=Title)
    title = request.form['Title']
    status = request.form['Status']
    genre = request.form['Genre']
    rating = request.form['Rating']
    review = request.form['Review']
    update = {}
    if len(title) > 0:
        update['Title'] = title
    if len(status) > 0:
        update['Status'] = status
    if len(genre) > 0:
        update['Genre'] = genre
    if len(rating) > 0:
        update['Rating'] = rating
    if len(review) > 0:
        update['Review'] = review
    client = pymongo.MongoClient(env['URI'])
    db = client.get_database("books")
    coll = db.get_collection("book")
    coll.update_one({"Title":Title}, {"$set": update})

    client.close()
    return redirect(url_for('view'))

if __name__ == '__main__':
    app.run()