"""Models for book library and rating app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    profile_pic = db.Column(db.String(50))
    avg_rating = db.Column(db.Float)
    num_rating = db.Column(db.Integer)
    about_me = db.Column(db.String(150))

    # friends = db.relationship("friend", foreign_keys="[Friend.user_id]")
    ratings = db.relationship("Rating", back_populates="user")
    shelf = db.relationship("Shelf", back_populates="user")

    def __repr__(self):
        """Returns info about user."""

        return f'<User user_id={self.user_id} username={self.username}>'
    


class Book(db.Model):
    """A Book"""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    overview = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    cover_pic = db.Column(db.String)
    avg_rating = db.Column(db.Float)
    num_rating = db.Column(db.Integer)

    book_genre = db.relationship("BookGenre", back_populates="book")
    ratings = db.relationship("Rating", back_populates="book")
    bookshelf = db.relationship("BookShelf", back_populates="book")

    def __repr__(self):
        """Returns info about book."""

        return f'<Book book_id={self.book_id} title={self.title}>'
    
    def to_dict(self):
        return { 'book_id' : self.book_id,
                'title' : self.title,
                'author' : self.author,
                'overview' : self.overview,
                'publish_date' : self.publish_date,
                'cover_pic' : self.cover_pic,
                'avg_rating' : self.avg_rating,
                'num_rating' : self.num_rating
        }
    

class Genre(db.Model):
    """A book genre"""

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(15), unique=True)

    book_genre = db.relationship("BookGenre", back_populates="genre")

    def __repr__(self):
        """Returns info about genre."""

        return f'<Genre genre_id={self.genre_id} name={self.name}'
    

class BookGenre(db.Model):
    """A table to connect books to genres"""

    __tablename__ = "bookgenre"

    book_genre_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"))

    book = db.relationship("Book", back_populates="book_genre")
    genre = db.relationship("Genre", back_populates="book_genre")

    def __repr__(self):
        return f'<BookGenre book_genre_id={self.book_genre_id} book_id={self.book_id} genre_id={self.genre_id}>'


class Rating(db.Model):
    """A rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    score = db.Column(db.Integer)     #1-5
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) 

    book = db.relationship("Book", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} book_id={self.book_id}>'


class Shelf(db.Model):
    """A shelf users can store a collection of books on."""

    __tablename__ = "shelfs"

    shelf_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    shelf_name = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) 

    bookshelf = db.relationship("BookShelf", back_populates="shelf")
    user = db.relationship("User", back_populates="shelf")

    def __repr__(self):
        return f'<Shelf shelf_id={self.shelf_id} user_id={self.user_id}>'
    

class BookShelf(db.Model):
    """A shelf with the collection of books connection"""

    __tablename__ = "bookshelfs"

    bookshelf_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey("shelfs.shelf_id")) 
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))

    shelf = db.relationship("Shelf", back_populates="bookshelf")
    book = db.relationship("Book", back_populates="bookshelf")


# class Friend(db.Model):
#     """Two users who are connected as friends."""

#     __tablename__ = 'friends'

#     friend_id = db.Column(db.Integer,
#                         autoincrement= True,
#                         primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     friend_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

#     user = db.relationship("User", back_populates="user")
#     friend = db.relationship("User", back_populates="friend")

#     def __repr__(self):
#         return f'<Friend friend_id={self.friend_id} friend_1={self.user} friend_2={self.friend_id}>'


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)