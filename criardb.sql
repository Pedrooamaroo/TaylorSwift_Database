
        CREATE TABLE Albuns (
            album_id INTEGER PRIMARY KEY,
            album_title VARCHAR(1000),
            album_url VARCHAR(2000),
            category VARCHAR(500)
        )
    
    
    CREATE TABLE Numeros (
            song_id INTEGER,
            album_id INTEGER,
            number INT NOT NULL,
            PRIMARY KEY(song_id, album_id),
            FOREIGN KEY (album_id) REFERENCES Albuns(album_id),
            FOREIGN KEY (song_id) REFERENCES Musicas(song_id)
        )
    
    CREATE TABLE Musicas (
            song_id INTEGER PRIMARY KEY,
            song_title VARCHAR(1000),
            views INTEGER,
            date DATE,
            song_url VARCHAR(2000),
            album_id INTEGER,
            lyrics_id INTEGER,
            FOREIGN KEY (album_id) REFERENCES Albuns(album_id)
        )
    
    CREATE TABLE Pessoas (
            person_id INTEGER PRIMARY KEY,
            person VARCHAR(50)
        )

    CREATE TABLE Produtores (
            song_id INTEGER,
            producer_id INTEGER,
            PRIMARY KEY (song_id, producer_id),
            FOREIGN KEY (song_id) REFERENCES Musicas(song_id),
            FOREIGN KEY (producer_id) REFERENCES Pessoas(person_id)
        )
    
        CREATE TABLE Artistas (
            song_id INTEGER,
            artist_id INTEGER,
            PRIMARY KEY (song_id, artist_id),
            FOREIGN KEY (song_id) REFERENCES Musicas(song_id),
            FOREIGN KEY (artist_id) REFERENCES Pessoas(person_id)
        )
    
    CREATE TABLE Escritores (
            song_id INTEGER,
            writer_id INTEGER,
            PRIMARY KEY (song_id, writer_id),
            FOREIGN KEY (song_id) REFERENCES Musicas(song_id),
            FOREIGN KEY (writer_id) REFERENCES Pessoas(person_id)
        )
    
    CREATE TABLE Letras (
            lyrics_id INTEGER PRIMARY KEY,
            song_lyrics VARCHAR(200000)
        )

    
    CREATE TABLE Tags (
            tag_id INTEGER PRIMARY KEY,
            tag VARCHAR(1000)
        )
    
    
        CREATE TABLE Descricoes (
            song_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (song_id, tag_id),
            FOREIGN KEY (song_id) REFERENCES Musicas(song_id),
            FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
        )
    """