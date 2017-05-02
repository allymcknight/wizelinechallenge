from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Url
import os
import validators

app = Flask(__name__)


app.secret_key = "iupon4si0870oiniOGUH$*"
#avoid error message
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Renders home/search page"""

    return render_template('home.html')


@app.route('/new_url', methods=['POST'])
def create_new_url():
    """Creates a new shorter url and adds to db"""

    original_url = request.form.get('original_url')

    #Checks to see if inputted url is valid
    if not validators.url(original_url):
        return render_template('not_valid_url.html')



    custom_url = request.form.get('custom_url')

    row = Url.query.filter_by(original_url=original_url).first()

    if row:
        flash("This URL is already in our system. This is the shortened URL:  ")
        return render_template('result.html', shortened_url=row.shortened_url)

    if custom_url:
        if custom_url[:2] == "0x":
            flash("Please choose another custom url.")
            return redirect('/')
        custom_row = Url.query.filter_by(shortened_url=custom_url).first()

        if custom_row:

            flash("We're sorry, that custom shortened url is already taken")
            return redirect('/')
        else:

            new_shortened = Url(original_url=original_url, shortened_url=custom_url)
            db.session.add(new_shortened)
            db.session.commit()
            return render_template('result.html', shortened_url=custom_url)



    new_shortened = Url(original_url=original_url)
    db.session.add(new_shortened)
    db.session.commit()

    new_shortened.shortened_url = hex(int(new_shortened.id))
    db.session.commit()

    return render_template('result.html', shortened_url=new_shortened.shortened_url)



@app.route('/<short_url>')
def return_original_route(short_url):
    """Gets shortened url and returns original from DB"""

    url_info = Url.query.filter_by(shortened_url=short_url).first()

    if url_info:
        return redirect(url_info.original_url)

    else:
        return render_template('not-here.html')


@app.route('/analytics')
def show_data():

    urls = Url.query.all()

    created_count = 0

    for url in urls:
        if url.shortened_url[:2]=="0x":
            created_count +=1

    custom_count = len(urls)-created_count

    return render_template('analytics.html', custom_count=custom_count, created_count=created_count, total=len(urls))

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

