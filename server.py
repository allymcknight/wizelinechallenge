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

    return "<html><body>Placeholder for the homepage.</body></html>"



@app.route('/new_url', methods=['POST'])
def create_new_url():
    """Creates a new shorter url and adds to db"""

    original_url = request.form.get('orig_url')
    custom_url = request.form.get('custom_url')


   
    return redirect('/accomplishments/%s'% str(user.user_id))


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

