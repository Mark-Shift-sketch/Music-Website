from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import re
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'alkxctcegjjdvfbvgxzc'

MUSIC_FILES = [
    {
        "title": "Stairway To Heaven",
        "artist": "Led Zeppelin",
        "genre": "Rock",
        "file": "music/StairwayToHeaven.mp3"
    },
    {
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "genre": "Pop",
        "file": "music/ShapeofYou.mp3"
    },
    {
        "title": "Lose Yourself",
        "artist": "Eminem",
        "genre": "Rock",
        "file": "music/LoseYourself.mp3"
    },
    {
        "title": "Take Five",
        "artist": "Dave Brubeck",
        "genre": "Jazz",
        "file": "music/TakeFive.mp3"
    },
    {
        "title": "My Favorite Things from The Sound of Music",
        "artist": "Dave Brubeck",
        "genre": "Jazz",
        "file": "music/MyFavoriteThingsfromTheSoundofMusic(Official HD Video).mp3"
    },
    {
        "title": "Smells Like Teen Spirit",
        "artist": "Dave Brubeck",
        "genre": "Rock",
        "file": "music/NirvanaSmellsLikeTeenSpirit(Lyrics).mp3"
    },
    {
        "title": "So What",
        "artist": "Dave Brubeck",
        "genre": "Jazz",
        "file": "music/P!nkSoWhat(Official Video).mp3"
    },
    {
        "title": "Queen",
        "artist": "Bohemian Rhapsody",
        "genre": "Rock",
        "file": "music/QueenBohemianRhapsody(Official Video Remastered).mp3"
    },
    {
        "title": "Rolling In The Deep And Set Fire To The Rain",
        "artist": "Adele",
        "genre": "Pop",
        "file": "music/RollingInTheDeepAdele(Lyrics)SetFireToTheRainAdele(Lyrics).mp3"
    },
    {
        "title": "Moonlight Sonata",
        "artist": "Beethoven",
        "genre": "Classical",
        "file": "music/BeethovenMoonlightSonata(1st Movement).mp3"
    },
    {
        "title": "Canon In D",
        "artist": "Pachelbel",
        "genre": "Classical",
        "file": "music/CanoninDPachelbel.mp3"
    },
    {
        "title": "Hotels California",
        "artist": "Dave Brubeck",
        "genre": "Rock",
        "file": "music/EaglesHotelCalifornia(Live 1977)(Official Video)[HD].mp3"
    },
    {
        "title": "Sweet Child O Mine",
        "artist": "Gun N' Poses",
        "genre": "Rock",
        "file": "music/GunsNRosesSweetChildOMine(Lyrics).mp3"
    },
    {
        "title": "Like A Player",
        "artist": "Madonna",
        "genre": "Pop",
        "file": "music/MadonnaLikeAPrayer(Lyrics).mp3"
    },
    {
        "title": "Thriller",
        "artist": "Micheal Jackson",
        "genre": "Pop",
        "file": "music/MichaelJacksonThriller(Lyrics).mp3"
    },
    {
        "title": "All Blues",
        "artist": "Miles Bavis",
        "genre": "Jazz",
        "file": "music/MilesDavisAllBlues(Official Audio).mp3"
    },
    {
        "title": "Blue In Green",
        "artist": "Miles Davis",
        "genre": "Jazz",
        "file": "music/MilesDavisBlueInGreen(Official Audio).mp3"
    },
    {
        "title": "My Favorite Things from The Soud of Music",
        "artist": "unknow",
        "genre": "Jazz",
        "file": "music/MyFavoriteThingsfromTheSoundofMusic(Official HD Video).mp3"
    },
    {
        "title": "The Weeknd",
        "artist": "Blinding Lights",
        "genre": "Pop",
        "file": "music/TheWeekndBlindingLights(Lyrics).mp3"
    },
]

def get_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_songs_db():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL,
            file TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_playlists_db():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def init_playlist_songs_db():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlist_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER NOT NULL,
            song_id INTEGER NOT NULL,
            FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
            FOREIGN KEY(song_id) REFERENCES songs(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

init_users_db()
init_songs_db()
init_playlists_db()
init_playlist_songs_db()

def get_user_id(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result['id'] if result else None

def get_songs():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "artist": row[2], "genre": row[3], "file": row[4]} for row in rows]

def get_playlists(username):
    user_id = get_user_id(username)
    conn = sqlite3.connect('songs.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists WHERE user_id = ?", (user_id,))
    playlist_rows = cursor.fetchall()
    playlists = {}
    for pl in playlist_rows:
        playlist_id = pl['id']
        playlist_name = pl['name']
        cursor.execute("""
            SELECT s.* 
            FROM songs s 
            JOIN playlist_songs ps ON s.id = ps.song_id 
            WHERE ps.playlist_id = ?
        """, (playlist_id,))
        song_rows = cursor.fetchall()
        songs_list = [{"id": row[0], "title": row[1], "artist": row[2], "genre": row[3], "file": row[4]} for row in song_rows]
        playlists[playlist_name] = songs_list
    conn.close()
    return playlists

def populate_songs_db():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    for song in MUSIC_FILES:
        cursor.execute("SELECT id FROM songs WHERE title = ? AND artist = ?", (song['title'], song['artist']))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO songs (title, artist, genre, file) VALUES (?, ?, ?, ?)",
                (song['title'], song['artist'], song['genre'], song['file'])
            )
    conn.commit()
    conn.close()

populate_songs_db()


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    playlists = get_playlists(session['username'])
    #recent and suggested songs
    conn = sqlite3.connect('songs.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs ORDER BY id DESC LIMIT 3")
    recent_rows = cursor.fetchall()
    recent_songs = [{"id": row[0], "title": row[1], "artist": row[2], "genre": row[3], "file": row[4]} for row in recent_rows]
    cursor.execute("SELECT * FROM songs ORDER BY RANDOM() LIMIT 3")
    suggested_rows = cursor.fetchall()
    suggested_songs = [{"id": row[0], "title": row[1], "artist": row[2], "genre": row[3], "file": row[4]} for row in suggested_rows]
    conn.close()
    return render_template('dashboard.html',
                           username=session['username'],
                           playlists=playlists,
                           recent_songs=recent_songs,
                           suggested_songs=suggested_songs)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        
        if not confirm_password:
            return "Confirm password field is missing!"
        
        if not re.match(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
            return render_template("signup.html", message="Invalid email address")
        
        supported_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        if email.split('@')[1] not in supported_domains:
            return render_template('signup.html', message="Use Gmail, Yahoo, or Outlook")
        
        if password != confirm_password:
            return render_template('signup.html', message="Passwords do not match")
        
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
            return render_template('signup.html', message="Password must be at least 8 characters, contain 1 digit, and 1 uppercase letter")
        
        with get_db() as conn:
            # check email is already registered
            existing_email = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
            if existing_email:
                return render_template('signup.html', message="Email already used, please log in")
            
            #Check if the username already exists
            existing_username = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            if existing_username:
                return render_template('signup.html', message="Username already exists")
            
            conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            session['username'] = username
            
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

        
       

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', message="Invalid username or password")
    return render_template('login.html')

@app.route('/generate_artist_link/<username>/<artist_name>')
def generate_artist_link(username, artist_name):
    share_url = url_for('share_artist', username=username, artist_name=artist_name, _external=True)
    return {"share_url": share_url}


@app.route('/share_artist/<username>/<artist_name>')
def share_artist(username, artist_name):
    songs = get_songs()
    artist_songs = [song for song in songs if song["artist"].lower() == artist_name.lower()]
    if not artist_songs:
        return "No songs found for this artist.", 404
    return render_template('share_artist.html', username=username, artist_name=artist_name, songs=artist_songs)


@app.route('/share_song/<int:song_id>')
def share_song(song_id):
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, artist, file FROM songs WHERE id = ?", (song_id,))
    song = cursor.fetchone()
    conn.close()
    
    if not song:
        return "Song not found",
    
    song_data = {
        "title": song[0],
        "artist": song[1],
        "file": song[2],
        "share_url": url_for('static', filename=song[2], _external=True)
    }
    return render_template('share_song.html', song=song_data)
@app.route('/share_genre/<username>/<genre>')
def share_genre(username, genre):
    friend_username = request.args.get('friend_username', None)
    songs = get_songs()
    genre_songs = [song for song in songs if song["genre"].lower() == genre.lower()]
    if not genre_songs:
        return "No songs found for this genre.", 404
    return render_template('share_genre.html', username=username, genre=genre, songs=genre_songs, friend_username=friend_username)



@app.route('/web/<username>', methods=['GET', 'POST'])
def web_interface(username):
    session['username'] = username
    songs = get_songs()
    playlists = get_playlists(username)
    artist_name = request.args.get('artist_name', None)
    action = request.args.get('action', None)
    query = request.args.get('query', None)
    selected_genre = request.args.get('genre', None)
    playlist_name = request.args.get('playlist_name', None)
    song_id = request.args.get('song_id', None)
    playlist_target = request.args.get('playlist_target', None)
    user_id = get_user_id(username)

    if action == 'logout':
        session.clear()
        return redirect(url_for('login'))
    
    elif action == 'artistmusic' and artist_name:
        songs = get_songs()
        artist_songs = [song for song in songs if song["artist"].lower() == artist_name.lower()]
        return render_template('dashboard.html',  action='artistmusic', artist_name=artist_name, artist_songs=artist_songs, playlists=playlists)

    elif action == 'shareartist' and artist_name and request.args.get('friend_username'):
        friend_username = request.args.get('friend_username')
        songs = get_songs() 
        artist_songs = [song for song in songs if song["artist"].lower() == artist_name.lower()]
        return render_template('share_artist.html', username=session['username'], artist_name=artist_name, songs=artist_songs, friend_username=friend_username)

    elif action == 'allmusic':
        return render_template('dashboard.html', results=songs, playlists=playlists, action='allmusic', playlist_target=playlist_target)
    
    elif action == 'searchartist' and artist_name:
        matched_artists = list(set(song["artist"] for song in songs if artist_name.lower() in song["artist"].lower()))
        return render_template('dashboard.html', action='searchartist', search_results=matched_artists, playlists=playlists)



    elif action == 'genre' and selected_genre:
        if selected_genre.lower() == 'all music':
            # Return all songs when "All Music" is selected
            filtered_songs = songs
        else:
            filtered_songs = [song for song in songs if song['genre'].lower() == selected_genre.lower()]
        return render_template('dashboard.html', genre=selected_genre, results=filtered_songs, playlists=playlists)
    elif action == 'search' and query:
        if query.lower().startswith("artist:"):
            artist_name = query[7:].strip()
            results = [song for song in songs if song['artist'].lower() == artist_name.lower()]
        else:
            results = [song for song in songs
                if query.lower() in song['title'].lower() or query.lower() in song['artist'].lower()
            ]
        return render_template('dashboard.html', query=query, results=results, playlists=playlists)

    elif action == 'createplaylist' and playlist_name:
        conn = sqlite3.connect('songs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
        if cursor.fetchone():
            conn.close()
            return render_template('dashboard.html', error="Playlist already exists.", playlists=playlists)
        cursor.execute("INSERT INTO playlists (name, user_id) VALUES (?, ?)", (playlist_name, user_id))
        conn.commit()
        conn.close()
        playlists = get_playlists(username)
        #redirect to All Music view with the new playlist as target
        return redirect(url_for('web_interface', username=username, action='allmusic', playlist_target=playlist_name))

    elif action == 'addtoplaylist' and song_id:
        user_playlists = get_playlists(username)
        if not user_playlists:
            return render_template('dashboard.html', message="You have no Playlist Created.", playlists=user_playlists, results=songs)

        playlist_target = request.args.get('playlist_target', None)
        if not playlist_target:
            return render_template('dashboard.html', message="No Playlist Selected.", playlists=user_playlists, results=songs)
        conn = sqlite3.connect('songs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ? AND user_id = ?", (playlist_target, user_id))
        pl_row = cursor.fetchone()
        if pl_row:
            playlist_id = pl_row[0]
            cursor.execute("SELECT id FROM playlist_songs WHERE playlist_id = ? AND song_id = ?", (playlist_id, song_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
                conn.commit()
            message = f"Added song to {playlist_target}."
        else:
            message = "Playlist not found."

        conn.close()
        playlists = get_playlists(username)
        return render_template('dashboard.html',message=message, playlists=playlists, results=songs)

    elif action == 'viewplaylist' and playlist_name:
        playlists = get_playlists(username)
        results = playlists.get(playlist_name, [])
        return render_template('dashboard.html', playlist_name=playlist_name, results=results, playlists=playlists)
    elif action == 'deleteplaylist' and playlist_name:
        conn = sqlite3.connect('songs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
        pl_row = cursor.fetchone()
        if pl_row:
            playlist_id = pl_row[0]
            cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
            conn.commit()
            message = f"Playlist '{playlist_name}' deleted."
        else:
            message = "Playlist not found, try again!"
        conn.close()
        playlists = get_playlists(username)
        return render_template('dashboard.html', message=message, playlists=playlists, results=songs)
    elif action == 'remove_from_playlist' and playlist_name and song_id:
        conn = sqlite3.connect('songs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM playlists WHERE name = ? AND user_id = ?", (playlist_name, user_id))
        pl_row = cursor.fetchone()
        if pl_row:
            playlist_id = pl_row[0]
            cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = ? AND song_id = ?", (playlist_id, song_id))
            conn.commit()
        conn.close()
        playlists = get_playlists(username)
        results = playlists.get(playlist_name, [])
        return render_template('dashboard.html', playlist_name=playlist_name, results=results, playlists=playlists)

    return render_template('dashboard.html', results=songs, playlists=playlists)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/check_user/<friend_username>')
def check_user(friend_username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (friend_username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"exists": True}
    else:
        return {"exists": False}

@app.route('/share/<username>/<playlist_name>')
def share_playlist(username, playlist_name):
    playlists = get_playlists(username)
    playlist = playlists.get(playlist_name, [])
    return render_template('share.html', username=username, playlist_name=playlist_name, songs=playlist)

if __name__ == '__main__':
    app.run(debug=True)
