"""Models and database functions for Wizeline project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#####################################################################
# Model definitions

class Url(db.Model):
    """User of ratings website."""

    __tablename__ = "urls"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    original_url = db.Column(db.String(450), nullable=False)
    shortened_url = db.Column(db.String(400), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Url id=%s original=%s>" % (self.id,
                                               self.original_url)

#####################################################################
# Helper functions

def connect_to_db(app, db_uri):
    """Connect the database in Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app,'postgresql:///urlshorten')
    print "Connected to DB."