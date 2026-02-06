from flask import Flask, g, request
from flask import render_template_string
import sqlite3


# Configure Flask
app = Flask(__name__)

# Database configuration
# Ensure 'dbfinal.db' is in the same folder as this script
DATABASE = 'dbfinal.db'

def connect_db():
    """
    Connects to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    """
    Retrieves the database connection for the current request.
    """
    if 'db' not in g:
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """
    Closes the database connection when the request ends.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def main_page():
    """
    Home page with basic database statistics.
    """
    db = get_db()
    stats = {
        "albums": db.execute("SELECT COUNT(*) AS total FROM Albuns").fetchone()["total"],
        "songs": db.execute("SELECT COUNT(*) AS total FROM Musicas").fetchone()["total"],
        "n_produtores": db.execute("SELECT COUNT(*) FROM (SELECT DISTINCT producer_id FROM Produtores)").fetchone()[0],
        "n_artistas": db.execute("SELECT COUNT(*) FROM (SELECT DISTINCT artist_id FROM Artistas)").fetchone()[0],
        "n_escritores": db.execute("SELECT COUNT(*) FROM (SELECT DISTINCT writer_id FROM Escritores)").fetchone()[0],
        "tags": db.execute("SELECT COUNT(*) FROM Tags").fetchone()[0],
    }
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Statistics</title>
            <style>
                body {
                    background-color: #FFD6CC; /* Light salmon background */
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Database Statistics</h1>
            <ul class="list-group mt-3">
                <li class="list-group-item">Albums: {{ stats['albums'] }}</li>
                <li class="list-group-item">Songs: {{ stats['songs'] }}</li>
                <li class="list-group-item">Producers: {{ stats['n_produtores'] }}</li>
                <li class="list-group-item">Artists: {{ stats['n_artistas'] }}</li>
                <li class="list-group-item">Writers: {{ stats['n_escritores'] }}</li>
                <li class="list-group-item">Tags: {{ stats['tags'] }}</li>
            </ul>
            <a href="/albums" class="btn" style="background-color: #9370DB; color: white;">View Albums</a>
            <a href="/songs" class="btn" style="background-color: #9370DB; color: white;">View Songs</a>
            <a href="/search" class="btn" style="background-color: #9370DB; color: white;">Search Albums & Songs</a>
            <a href="/person_search" class="btn" style="background-color: #9370DB; color: white;">Search People</a>
            <a href="/lyrics_search" class="btn" style="background-color: #9370DB; color: white;">Search Lyrics</a>
            <a href="/questions" class="btn" style="background-color: #9370DB; color: white;">Q&A</a>

            <div class="mt-5 text-center">
                <img src="{{ url_for('static', filename='taytay.jpg') }}" alt="Taytay Image" class="img-fluid">
            </div>
        </body>
        </html>
        """, stats=stats
    )


@app.route("/albums")
def list_albums():
    """
    Lists all albums with links for more details, excluding "No Album" entries.
    """
    db = get_db()
    albums = db.execute("""
        SELECT album_title, album_url 
        FROM Albuns 
        WHERE album_title != "Sem Album"
        ORDER BY album_title
    """).fetchall()
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Albums</title>
            <style>
                body {
                    background-color: #FFD6CC; 
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Albums</h1>
            <ul class="list-group mt-3">
                {% for album in albums %}
                    <li class="list-group-item">
                        <a href="{{ album['album_url'] }}" target="_blank">{{ album['album_title'] }}</a>
                    </li>
                {% endfor %}
            </ul>
            <a href="/" class="btn btn-secondary mt-3">Back</a>
        </body>
        </html>
        """, albums=albums
    )


@app.route("/songs")
def list_songs():
    """
    Lists all songs organized by date (ascending) with links for details.
    """
    db = get_db()
    # Convert date to standard ISO format during sorting
    songs = db.execute("""
        SELECT song_title, song_url, date 
        FROM Musicas 
        ORDER BY STRFTIME('%Y-%m-%d', SUBSTR(date, 7, 4) || '-' || SUBSTR(date, 4, 2) || '-' || SUBSTR(date, 1, 2)) ASC
    """).fetchall()
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Songs</title>
            <style>
                body {
                    background-color: #FFD6CC;
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Songs</h1>
            <ul class="list-group mt-3">
                {% for song in songs %}
                    <li class="list-group-item">
                        <a href="{{ song['song_url'] }}" target="_blank">{{ song['song_title'] }}</a>
                        <small class="text-muted">({{ song['date'] }})</small>
                    </li>
                {% endfor %}
            </ul>
            <a href="/" class="btn btn-secondary mt-3">Back</a>
        </body>
        </html>
        """, songs=songs
    )


@app.route("/search")
def search():
    """
    Allows searching for songs or albums by title.
    """
    query = request.args.get("q", "").strip()
    db = get_db()
    songs = db.execute("SELECT song_title, song_url FROM Musicas WHERE song_title LIKE ?", (f"%{query}%",)).fetchall() if query else []
    albums = db.execute("SELECT album_title, album_url FROM Albuns WHERE album_title LIKE ?", (f"%{query}%",)).fetchall() if query else []

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Search Albums & Songs</title>
            <style>
                 body {
                    background-color: #FFD6CC;
                }
                .btn-purple {
                    background-color: #9370DB;
                    color: white;
                    border-color: #9370DB;
                }
                .btn-purple:hover {
                    background-color: #7A5DC7;
                    border-color: #7A5DC7;
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Search Albums & Songs</h1>
            <form method="get" action="/search" class="mt-3">
                <input type="text" name="q" class="form-control" placeholder="Enter title..." value="{{ query }}">
                <button type="submit" class="btn btn-purple mt-3">Search</button>
            </form>
            {% if query %}
                <h3 class="mt-4">Results for "{{ query }}"</h3>
                <h4>Albums</h4>
                <ul class="list-group">
                    {% for album in albums %}
                        <li class="list-group-item">
                            <a href="{{ album['album_url'] }}" target="_blank">{{ album['album_title'] }}</a>
                        </li>
                    {% endfor %}
                </ul>
                <h4 class="mt-4">Songs</h4>
                <ul class="list-group">
                    {% for song in songs %}
                        <li class="list-group-item">
                            <a href="{{ song['song_url'] }}" target="_blank">{{ song['song_title'] }}</a>
                        </li>
                    {% endfor %}
                </ul>
            {% endif %}
            <a href="/" class="btn btn-secondary mt-3">Back</a>
        </body>
        </html>
        """, query=query, songs=songs, albums=albums
    )


@app.route("/person_search")
def person_search():
    """
    Search for people and display tabs for songs where they worked as producers, artists, or writers.
    """
    query = request.args.get("q", "").strip()
    db = get_db()
    results = {"produtor": [], "artista": [], "escritor": []}
    error_message = None

    try:
        if query:
            # Function to fetch data by role
            def get_songs_by_role(role_table, role_column):
                return db.execute(f"""
                    SELECT 
                        Musicas.song_title AS song_title,
                        Musicas.song_url AS song_url,
                        GROUP_CONCAT(DISTINCT ArtistasPeople.person) AS artistas,
                        GROUP_CONCAT(DISTINCT EscritoresPeople.person) AS escritores,
                        GROUP_CONCAT(DISTINCT ProdutoresPeople.person) AS produtores
                    FROM Pessoas
                    JOIN {role_table} AS RoleTable ON Pessoas.person_id = RoleTable.{role_column}
                    JOIN Musicas ON Musicas.song_id = RoleTable.song_id
                    LEFT JOIN Artistas ON Artistas.song_id = Musicas.song_id
                    LEFT JOIN Escritores ON Escritores.song_id = Musicas.song_id
                    LEFT JOIN Produtores ON Produtores.song_id = Musicas.song_id
                    LEFT JOIN Pessoas AS ArtistasPeople ON Artistas.artist_id = ArtistasPeople.person_id
                    LEFT JOIN Pessoas AS EscritoresPeople ON Escritores.writer_id = EscritoresPeople.person_id
                    LEFT JOIN Pessoas AS ProdutoresPeople ON Produtores.producer_id = ProdutoresPeople.person_id
                    WHERE Pessoas.person LIKE ?
                    GROUP BY Musicas.song_id
                    ORDER BY Musicas.song_title
                """, (f"%{query}%",)).fetchall()

            # Retrieve data for each role
            results["produtor"] = get_songs_by_role("Produtores", "producer_id")
            results["artista"] = get_songs_by_role("Artistas", "artist_id")
            results["escritor"] = get_songs_by_role("Escritores", "writer_id")

    except sqlite3.Error as e:
        error_message = f"Error accessing database: {e}"

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Search People</title>
            <style>
                 body {
                    background-color: #FFD6CC;
                }
                .btn-purple {
                    background-color: #9370DB;
                    color: white;
                    border-color: #9370DB;
                }
                .btn-purple:hover {
                    background-color: #7A5DC7;
                    border-color: #7A5DC7;
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Search People</h1>
            <form method="get" action="/person_search" class="mt-3">
                <input type="text" name="q" class="form-control" placeholder="Enter person's name..." value="{{ query }}">
                <button type="submit" class="btn btn-purple mt-3">Search</button>
            </form>
            {% if error_message %}
                <div class="alert alert-danger mt-4">{{ error_message }}</div>
            {% endif %}
            {% if query %}
                <h3 class="mt-4">Results for "{{ query }}"</h3>
                <ul class="nav nav-tabs" id="rolesTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="produtor-tab" data-bs-toggle="tab" data-bs-target="#produtor" type="button" role="tab">Producer</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="artista-tab" data-bs-toggle="tab" data-bs-target="#artista" type="button" role="tab">Artist</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="escritor-tab" data-bs-toggle="tab" data-bs-target="#escritor" type="button" role="tab">Writer</button>
                    </li>
                </ul>
                <div class="tab-content mt-3">
                    {% for role, role_results in results.items() %}
                        <div class="tab-pane fade {% if loop.first %}show active{% endif %}" id="{{ role }}" role="tabpanel">
                            {% if role_results %}
                                <ul class="list-group">
                                    {% for result in role_results %}
                                        <li class="list-group-item">
                                            <strong>Song:</strong> <a href="{{ result['song_url'] }}" target="_blank">{{ result['song_title'] }}</a><br>
                                            <strong>Producers:</strong> {{ result['produtores'] or 'None' }}<br>
                                            <strong>Artists:</strong> {{ result['artistas'] or 'None' }}<br>
                                            <strong>Writers:</strong> {{ result['escritores'] or 'None' }}
                                        </li>
                                    {% endfor %}
                                </ul>
                            {% else %}
                                <p>No songs found for this role.</p>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
            <a href="/" class="btn btn-secondary mt-3">Back</a>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """, query=query, results=results, error_message=error_message
    )

@app.route("/lyrics_search")
def lyrics_search():
    """
    Search lyrics by content in the 'Letras' table.
    """
    query = request.args.get("q", "").strip()
    db = get_db()
    lyrics_results = []

    if query:
        try:
            lyrics_results = db.execute("""
                SELECT 
                    Musicas.song_title, 
                    Musicas.song_url, 
                    Letras.song_lyrics 
                FROM Musicas
                JOIN Letras ON Musicas.song_id = Letras.lyrics_id
                WHERE Letras.song_lyrics LIKE ?
            """, (f"%{query}%",)).fetchall()
        except sqlite3.Error as e:
            return f"<p>Error accessing database: {e}</p>"

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Search Lyrics</title>
            <style>
                 body {
                    background-color: #FFD6CC;
                }
                .btn-purple {
                    background-color: #9370DB;
                    color: white;
                    border-color: #9370DB;
                }
                .btn-purple:hover {
                    background-color: #7A5DC7;
                    border-color: #7A5DC7;
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Search Lyrics</h1>
            <form method="get" action="/lyrics_search" class="mt-3">
                <input type="text" name="q" class="form-control" placeholder="Enter word or phrase..." value="{{ query }}">
                <button type="submit" class="btn btn-purple mt-3">Search</button>
            </form>
            {% if query %}
                <h3 class="mt-4">Results for "{{ query }}"</h3>
                {% if lyrics_results %}
                    <ul class="list-group mt-3">
                        {% for lyric in lyrics_results %}
                            <li class="list-group-item">
                                <strong>Song:</strong> <a href="{{ lyric['song_url'] }}" target="_blank">{{ lyric['song_title'] }}</a><br>
                                <strong>Lyric:</strong> {{ lyric['song_lyrics'] }}
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p class="text-muted">No results found.</p>
                {% endif %}
            {% endif %}
            <a href="/" class="btn btn-secondary mt-3">Back</a>
        </body>
        </html>
        """, query=query, lyrics_results=lyrics_results
    )

@app.route("/questions")
def questions():
    """
    Page with Questions and Answers.
    """
    db = get_db()
    queries = [
        # Question 1
        {
            "question": "Which song has the most views?",
            "query": """
                SELECT song_title as Title, views AS Views
                FROM Musicas
                WHERE views = (
                    SELECT MAX(views)
                    FROM Musicas
                )
            """
        },
        # Question 2
        {
            "question": "Which album has over 10 songs and more than 20 million combined views?",
            "query": """
                SELECT a.album_title as Title, SUM(m.views) AS Total_Views
                FROM Albuns a
                JOIN Musicas m ON a.album_id = m.album_id
                GROUP BY a.album_id, Title
                HAVING COUNT(m.song_id) > 10 
                AND SUM(m.views) > 20000000
            """
        },
        # Question 3
        {
            "question": "Which album has the highest average views per song?",
            "query": """
                SELECT Titulo as Title, avg_views AS Average_Views
                FROM (
                    SELECT a.album_title AS Titulo, AVG(m.views) AS avg_views
                    FROM Albuns a
                    JOIN Musicas m ON a.album_id = m.album_id
                    GROUP BY a.album_id, a.album_title
                ) AS AlbumAvg
                WHERE avg_views = (
                    SELECT MAX(avg_views)
                    FROM (
                        SELECT AVG(m.views) AS avg_views
                        FROM Albuns a
                        JOIN Musicas m ON a.album_id = m.album_id
                        GROUP BY a.album_id
                    ) AS AvgCalculation
                )
            """
        },
        # Question 4
        {
            "question": "Which songs have more than one writer?",
            "query": """
                SELECT m.song_title as Title, COUNT(e.writer_id) AS Writer_Count
                FROM Musicas m
                JOIN Escritores e ON m.song_id = e.song_id
                GROUP BY m.song_id, Title
                HAVING COUNT(e.writer_id) > 1
            """
        },
        # Question 5
        {
            "question": "What are the most used tags?",
            "query": """
                SELECT Tag, Contagem as Count
                FROM (
                    SELECT t.tag AS Tag, COUNT(*) AS Contagem
                    FROM Descricoes d
                    JOIN Tags t ON d.tag_id = t.tag_id
                    GROUP BY t.tag
                ) AS TagCounts
                WHERE Contagem = (
                    SELECT MAX(Contagem)
                    FROM (
                        SELECT COUNT(*) AS Contagem
                        FROM Descricoes d
                        JOIN Tags t ON d.tag_id = t.tag_id
                        GROUP BY t.tag
                    ) AS MaxTagCounts
                )
            """
        },
        # Question 7
        {
            "question": "How many songs are in each album?",
            "query": """
                SELECT a.album_title as Title, COUNT(m.song_id) AS Count
                FROM Albuns a
                LEFT JOIN Musicas m ON a.album_id = m.album_id
                GROUP BY a.album_id, a.album_title
            """
        },
        # Question 8
        {
            "question": "Which albums have songs with over 1 million views?",
            "query": """
                SELECT DISTINCT a.album_title as Title
                FROM Albuns a
                JOIN Musicas m ON a.album_id = m.album_id
                WHERE m.views > 1000000
            """
        },
        # Question 9
        {
            "question": "What is the most popular album category (based on total views)?",
            "query": """
                SELECT Categoria as Category, total_views AS Views
                FROM (
                    SELECT a.category AS Categoria, SUM(m.views) AS total_views
                    FROM Albuns a
                    JOIN Musicas m ON a.album_id = m.album_id
                    GROUP BY a.category
                ) AS CategoriaViews
                WHERE total_views = (
                    SELECT MAX(total_views)
                    FROM (
                        SELECT SUM(m.views) AS total_views
                        FROM Albuns a
                        JOIN Musicas m ON a.album_id = m.album_id
                        GROUP BY a.category
                    ) AS MaxCategoriaViews
                )
            """
        },
        # Question 10
        {
            "question": "Which songs have more than one tag associated?",
            "query": """
                SELECT m.song_title as Title, COUNT(d.tag_id) AS Count
                FROM Musicas m
                JOIN Descricoes d ON m.song_id = d.song_id
                GROUP BY m.song_id, Title
                HAVING COUNT(d.tag_id) > 1
            """
        }
    ]

    results = []
    for idx, q in enumerate(queries):
        try:
            result = db.execute(q["query"]).fetchall()
            results.append({
                "question_number": idx + 1, 
                "question": q["question"],
                "result": result
            })
        except sqlite3.Error as e:
            results.append({
                "question_number": idx + 1,
                "question": q["question"],
                "result": f"Error: {e}"
            })

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Q&A</title>
            <style>
                body {
                    background-color: #FFD6CC;
                }
            </style>
        </head>
        <body class="container">
            <h1 class="mt-4">Questions & Answers</h1>
            <ul class="list-group mt-3">
                {% for q in results %}
                    <li class="list-group-item">
                        <strong>Question {{ q.question_number }}: {{ q.question }}</strong>
                        <br>
                        <table class="table table-bordered mt-3">
                            <thead>
                                <tr>
                                    {% for column in q.result[0].keys() %}
                                        <th>{{ column }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in q.result %}
                                    <tr>
                                        {% for value in row %}
                                            <td>{{ value }}</td>
                                        {% endfor %}
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </li>
                {% endfor %}
            </ul>
            <a href="/" class="btn btn-secondary mt-3">Back</a>
        </body>
        </html>
        """, results=results
    )


if __name__ == "__main__":

    app.run(debug=True)
