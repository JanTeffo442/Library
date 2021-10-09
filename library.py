import os
from flask import Flask 
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

user_name = os.environ.get('DB_USER')
pass_word = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
server_name = os.environ.get('SERVER_NAME')

#Initiate app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user_name}:{pass_word}@{server_name}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFCATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Create database model
class Library(db.Model):

	__tablename__ = 'books'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(150))
	edition = db.Column(db.String(30))
	authors = db.Column(db.String(200))
	isbn = db.Column(db.String(30))

	def __init__(self, title, edition, authors, isbn):

		self.title = title
		self.edition = edition
		self.authors = authors
		self.isbn = isbn

#db.create_all() #creates database table

class BookSchema(ma.Schema):
	class Meta:
		fields = ("title","edition","authors","isbn")

book = BookSchema()
books = BookSchema(many=True)

#Create routes
@app.route('/library/v1/books/all', methods=['GET'])
def book_list():

	list_of_books = Library.query.all()
	search_result = books.dump(list_of_books)

	return jsonify(search_result)

@app.route('/library/v1/books/add_books', methods=['POST'])
def add_books():
	title = request.json['title']
	edition = request.json['edition']
	authors = request.json['authors']
	isbn = request.json['isbn']

	add_book = Library(title, edition, authors, isbn)
	db.session.add(add_book)
	db.session.commit()
	return book.jsonify(add_book)

@app.route('//library/v1/books/book_id/<id>', methods=['GET'])
def find(id):
	single_book = Library.query.get(id)
	return book.jsonify(single_book)

@app.route('/library/v1/books/update_book/<id>', methods=['PUT'])
def update(id):
	edit_book = Library.query.get(id)

	title = request.json['title']
	edition = request.json['edition']
	authors = request.json['authors']
	isbn = request.json['isbn']

	edit_book.title = title
	edit_book.edition = edition
	edit_book.authors = authors
	edit_book.isbn = isbn

	db.session.commit()
	return book.jsonify(edit_book)

@app.route('/library/v1/books/delete_book/<id>', methods=['DELETE'])
def delete_book(id):

	del_book = Library.query.get('id')
	db.session.delete(del_book)

	return book.jsonify(del_book)

if __name__ == '__main__':
	app.run(debug=True)

