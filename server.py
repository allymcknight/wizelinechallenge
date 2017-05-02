from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Url
import os

app = Flask(__name__)


app.secret_key = "BLARGBLARG"
#avoid error message
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('home.html')


@app.route('/new_url', methods=['POST'])
def create_new_url():
    """Creates a new shorter url and adds to db"""

    original_url = request.form.get('original_url')
    custom_url = request.form.get('custom_url')

    row = Url.query.filter_by(original_url=original_url).first()

    if row:
        return "This URL is already in our system. This is the shortened URL:  " + row.shortened_url

    if custom_url:
        custom_row = Url.query.filter_by(shortened_url=custom_url).first()

        if custom_row:

            flash("We're sorry, that custom shortened url is already taken")
            return redirect('/')
        else:

            new_shortened = Url(original_url=original_url, shortened_url=custom_url)
            db.session.add(new_shortened)
            db.session.commit()
            return custom_url



    new_shortened = Url(original_url=original_url)
    db.session.add(new_shortened)
    db.session.commit()

    new_shortened.shortened_url = hex(int(new_shortened.id))
    db.session.commit()

    return new_shortened.shortened_url


@app.route('/<short_url>')
def return_original_route(short_url):
    """Gets shortened url and returns original from DB"""

    url_info = Url.query.filter_by(shortened_url=short_url).first()

    if url_info:
        return redirect(url_info.original_url)

    else:
        return render_template('not-here.html')



@app.route('/all_urls')
def show_all_urls():
    """Shows a list of all submitted URLs"""

    urls = Url.query.all()

    return render_template('all_urls.html', urls=urls)

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app, 'postgresql:///urlshorten')

    DebugToolbarExtension(app)

    app.run()

