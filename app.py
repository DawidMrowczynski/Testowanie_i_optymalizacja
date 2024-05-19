from flask import Flask, render_template, jsonify, request
import requests
import logging
from logging.handlers import RotatingFileHandler
from memory_profiler import profile

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the log level

# Create file handler which logs even debug messages
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*100, backupCount=10)  # 100MB per file
file_handler.setLevel(logging.INFO)  # Ensure this matches the desired log level

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
@app.errorhandler(404)
@profile
def page_not_found(e):
    app.logger.error(f'Page not found: {e}', exc_info=True)
    return 'This page does not exist', 404

@app.errorhandler(500)
@profile
def internal_server_error(e):
    app.logger.error(f'Internal server error: {e}', exc_info=True)
    return 'Internal server error', 500

@app.after_request
@profile
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Funkcja pomocnicza do pobierania danych z API
@profile
def get_data(endpoint):
    response = requests.get(f"https://jsonplaceholder.typicode.com/{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        app.logger.error(f"Failed to fetch data from {endpoint}. Status code: {response.status_code}")
        return None

# Strona główna wyświetlająca posty
@app.route('/')
@profile
def show_posts():
    posts = get_data("posts")
    return render_template('home.html')

@app.route('/comments')
@profile
def show_comments():
    comments = get_data("comments")
    return render_template('comments.html', comments=comments)

@app.route('/albums')
@profile
def show_albums():
    albums = get_data("albums")
    return render_template('albums.html', albums=albums)

# Wyszukiwarka postów
@app.route('/', methods=['GET', 'POST'])
@profile
def search_posts():
    if request.method == 'POST':
        min_chars = request.form.get('min_chars')
        max_chars = request.form.get('max_chars')
        # Tutaj można przefiltrować posty na podstawie liczby znaków
        posts = get_data("posts")
        filtered_posts = [post for post in posts if len(post['body']) >= int(min_chars) and len(post['body']) <= int(max_chars)]
        return render_template('home.html', posts=filtered_posts)
    else:
        return render_template('home.html')
@app.route('/photos', methods=['GET', 'POST'])
@profile
def search_photos():
    if request.method == 'POST':
        amount = request.form.get('Amount_of_photos')
        photos = get_data("photos")
        filred_photos = photos[:int(amount)]
        return render_template('photos.html', photos=filred_photos)
    else:
        return render_template('photos.html')

@app.route('/photos')
@profile
def show_photos():
    photos = get_data("photos")
    return render_template('photos.html')
if __name__ == "__main__":
    app.run(debug=True)
