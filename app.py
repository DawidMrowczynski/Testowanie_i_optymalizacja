from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"



@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Funkcja pomocnicza do pobierania danych z API
def get_data(endpoint):
    response = requests.get(f"https://jsonplaceholder.typicode.com/{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        app.logger.error(f"Failed to fetch data from {endpoint}. Status code: {response.status_code}")
        return None

# Strona główna wyświetlająca posty
@app.route('/')
def show_posts():
    posts = get_data("posts")
    return render_template('posts.html', posts=posts)

# API do ustawiania liczby wyświetlanych elementów
@app.route('/api/set-display-count', methods=['POST'])
def set_display_count():
    data = request.json
    # Tutaj można zapisać nową liczbę wyświetlanych elementów
    return jsonify({"message": "Display count set successfully"})

# Wyszukiwarka postów
@app.route('/search', methods=['GET', 'POST'])
def search_posts():
    if request.method == 'POST':
        min_chars = request.form.get('min_chars')
        max_chars = request.form.get('max_chars')
        # Tutaj można przefiltrować posty na podstawie liczby znaków
        posts = get_data("posts")
        filtered_posts = [post for post in posts if len(post['body']) >= int(min_chars) and len(post['body']) <= int(max_chars)]
        return render_template('posts.html', posts=filtered_posts)
    else:
        return render_template('search.html')



if __name__ == "__main__":
    app.run(debug=True)
