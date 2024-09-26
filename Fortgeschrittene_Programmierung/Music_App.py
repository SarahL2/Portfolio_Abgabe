import csv  # Importiert das CSV-Modul, um mit CSV-Dateien zu arbeiten
import os   # Importiert das OS-Modul für Betriebssystemfunktionen
import time # Importiert das Time-Modul für Zeitmessung

songs = []  # Liste, die alle Songs speichern wird

# Klasse zur Darstellung eines Songs
class Song:
    def __init__(self, name, artist, album, genre, likes):
        self.name = name       # Name des Songs
        self.artist = artist   # Künstler des Songs
        self.album = album     # Album des Songs
        self.genre = genre     # Genre des Songs
        self.likes = likes     # Anzahl der Likes des Songs


    def __str__(self):
        # Gibt eine lesbare Darstellung des Songs zurück
        return f"{self.name} by {self.artist} - Album: {self.album}, Genre: {self.genre}, Likes: {self.likes}"

    def to_dict(self):
        # Wandelt das Songobjekt in ein Dictionary um
        return {
            'name': self.name,
            'artist': self.artist,
            'album': self.album,
            'genre': self.genre,
            'likes': self.likes
        }

    @staticmethod
    def from_dict(data):
        # Erstellt ein Songobjekt aus einem Dictionary
        return Song(data['name'], data['artist'], data['album'], data['genre'], data['likes'])

# Klasse zur Darstellung einer Playlist
class Playlist:
    def __init__(self, name):
        self.name = name          # Name der Playlist
        self.songs = []           # Liste der Songs in der Playlist

    def add_song(self, song):
        # Fügt einen Song zur Playlist hinzu
        self.songs.append(song)

    def __str__(self):
        # Gibt eine lesbare Darstellung der Playlist zurück
        return f"Playlist: {self.name}, Songs: {len(self.songs)}"

    def to_dict(self):
        # Wandelt die Playlist in ein Dictionary um
        return {
            'name': self.name,
            'songs': [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        # Erstellt eine Playlist aus einem Dictionary
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist

# Hauptklasse der Musik-App
class MusicApp:
    def __init__(self, data_file='songs_10000'): # Bitte hier den Dateipfad zur csv angeben wenn diese nicht im selben Ordner ist 
        self.data_file = data_file  # Dateipfad zur Datendatei
        self.playlists = []          # Liste der Playlists
        self.songs = []              # Liste der Songs
        self.load_data()             # Lädt die Daten beim Start

    def load_data(self):
        # Lädt Songs und Playlists aus einer CSV-Datei
        with open(self.data_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file) # CSV-Leser initialisieren

            loading_playlists = False # Flag, um zu erkennen, ob Playlists geladen werden
            
            for row in csv_reader:
                if row == []:
                    loading_playlists = True # Leere Zeile signalisiert den Übergang zu Playlists
                    continue
                    continue

                elif not loading_playlists:
                    # Erstellt ein Songobjekt aus der Zeile und fügt es der Liste hinzu
                    song_objekt = Song(row[0],row[1],row[2],row[3],row[4])
                    songs.append(song_objekt)
                else:
                    # Handhabt das Laden von Playlists
                    playlist_name = row[0]   # Name der Playlist
                    song_title = row[1]      # Titel des Songs

                    # Sucht nach der Playlist mit dem entsprechenden Namen
                    playlist = next((p for p in self.playlists if p.name == playlist_name), None)

                    if not playlist:
                        # Wenn die Playlist nicht existiert, wird sie erstellt
                        playlist = Playlist(playlist_name)
                        self.playlists.append(playlist)

                    # Fügt Songs zur Playlist hinzu, falls sie vorhanden sind
                    for playlist in self.playlists:
                        for s in songs:
                            if s.name == song_title and s not in playlist.songs:                         
                                playlist.add_song(s)

        print('Data succesfully loaded') # Bestätigung, dass die Daten erfolgreich geladen wurden
    
    def save_data(self):
        # Speichert Songs und Playlists in einer CSV-Datei
        with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file) # CSV-Schreiber initialisieren
            for song in songs:
                writer.writerow([song.name,song.artist,song.album,song.genre,song.likes])
            
            writer.writerow([]) # Fügt eine leere Zeile zwischen Songs und Playlists hinzu

            for playlist in self.playlists:
                for song in playlist.songs:
                    writer.writerow([playlist.name, song.name]) # Schreibt Playlist-Songs in die Datei                  


        print('Data saved successfully.') # Bestätigung, dass die Daten erfolgreich gespeichert wurden

    def add_song(self):
        # Fügt einen neuen Song hinzu
        name = input("Enter song name: ")
        artist = input("Enter artist name: ")
        album = input("Enter album name: ")
        genre = input("Enter genre: ")
        likes = input('Enter your likes: ')
        song = Song(name, artist, album, genre, likes)
        songs.append(song) # Fügt den Song der Liste hinzu
        print(f"Added song: {song}") # Bestätigung, dass der Song hinzugefügt wurde



    def create_playlist(self):
        # Erstellt eine neue Playlist
        name = input("Enter playlist name: ")
        playlist = Playlist(name) # Erstellt die Playlist
        self.playlists.append(playlist) # Fügt die Playlist der Liste hinzu
        print(f"Created playlist: {playlist}") # Bestätigung, dass die Playlist erstellt wurde

    def add_song_to_playlist(self):
        # Fügt einen Song zu einer bestehenden Playlist hinzu
        playlist_name = input('Enter the name of the playlist: ')
        for playlist in self.playlists:
            if playlist.name == playlist_name:
                song_name = input('Enter the song to be added: ')
                for s in songs:
                    if s.name == song_name:                         
                        playlist.add_song(s) # Fügt den Song zur Playlist hinzu
                        print(f"Added {s.name} to playlist {playlist.name}") # Bestätigung
                    else:
                        print('Song not found') # Wenn der Song nicht gefunden wird

            else:
                print('Playlist not found') # Wenn die Playlist nicht gefunden wird


    def bubble_sort(self,songs,key):
        # Sortiert die Songs mithilfe des Bubble-Sort-Algorithmus
        n = len(songs)
        for i in range(n):
            swapped = False # Flag für den Tausch
        
            for j in range(0, n-i-1):
                if key == 'likes': 
                    # Sortiert nach Likes
                    if int(getattr(songs[j], key)) < int(getattr(songs[j+1], key)):
                        songs[j], songs[j+1] = songs[j+1], songs[j] 
                        swapped = True
                else:
                    # Sortiert nach anderen Kriterien
                    if getattr(songs[j], key) > getattr(songs[j+1], key):  
                        songs[j], songs[j+1] = songs[j+1], songs[j]
                        swapped = True
            if not swapped:
                break # Wenn kein Tausch stattgefunden hat, ist die Liste sortiert
        
        
    def search_songs(self):
        # Sucht nach Songs
        print('1. Linear Search')
        print('2. Binary Serach')
        searching_algorithm = input('Enter the searching algorithm: ')


        if searching_algorithm == '1':
            # Linearer Suchalgorithmus
            print("Sort by:")
            print("1. Title")
            print("2. Artist")
            print("3. Album")
            print("4. Genre")
        
            sort_input = input("Enter the number for the sort criteria: ")
            if sort_input == '1':
                key = 'name'
            elif sort_input == '2':
                key = 'artist'
            elif sort_input == '3':
                key = 'album'
            elif sort_input == '4':
                key = 'genre'
            else:
                print("Invalid choice. No sorting applied.")
                return
            
            search_value = input(f"Enter the {key} to search for: ")

            def linear_search(songs, key, search_value):
                start_time = time.time() # Startzeit für die Suche
                matches = [] # Liste für gefundene Übereinstimmungen
                for song in songs:
                    if getattr(song, key).lower() == search_value.lower(): # Vergleich der Werte
                        matches.append(song) # Fügt gefundene Songs hinzu
                end_time = time.time()  
                print(f"Linear Search completed in {end_time - start_time:.6f} seconds") # Zeit für die Suche
                return matches
            
            matching_songs = linear_search(songs, key, search_value)

            if matching_songs:
                print(f"Found {len(matching_songs)} song(s)") # Anzahl gefundener Songs
                for song in matching_songs:
                    print(song) # Gibt die gefundenen Songs aus
            else:
                print("No songs found") # Wenn keine Songs gefunden werden

        if searching_algorithm == '2':
            # Binärer Suchalgorithmus
            print("Sort by:")
            print("1. Title")
            print("2. Artist")
            print("3. Album")
            print("4. Genre")
        
            sort_input = input("Enter the number for the sort criteria: ")
            if sort_input == '1':
                key = 'name'
            elif sort_input == '2':
                key = 'artist'
            elif sort_input == '3':
                key = 'album'
            elif sort_input == '4':
                key = 'genre'
            else:
                print("Invalid choice. No sorting applied.")
                return
            
            search_value = input(f"Enter the {key} to search for: ")

            self.bubble_sort(songs,key) # Sortiert die Songs bevor die binäre Suche durchgeführt wird

            def binary_search(songs, key, search_value):
                start_time = time.time() # Startzeit für die Suche
                low = 0
                high = len(songs) - 1

                while low <= high:
                    mid = (low + high) // 2 # Bestimmt den mittleren Index
                    if getattr(songs[mid], key).lower() == search_value.lower():
                        end_time = time.time()  
                        print(f"Binary Search completed in {end_time - start_time:.6f} seconds")  # Zeit für die Suche
                        return mid # Gibt den Index des gefundenen Songs zurück
                    elif getattr(songs[mid], key).lower() < search_value.lower():
                        low = mid + 1 # Sucht in der rechten Hälfte 
                    else:
                        high = mid - 1  # Sucht in der linken Hälfte
                end_time = time.time()  
                print(f"Binary Search completed in {end_time - start_time:.6f} seconds")
                return -1 # Wenn kein Song gefunden wurde
            index = binary_search(songs,key,search_value)

            if index != -1:
                print(f"Song found: {songs[index]}") # Gibt den gefundenen Song aus
            else:
                print("No songs found") # Wenn kein Song gefunden wurde


    def sort_songs(self):
        # Sortiert die Songs
        print('1. Bubble Sort')
        print('2. Merge Sort')
        sorting_algorithm = input('Enter the sorting algorithm: ')
        
        if sorting_algorithm == '1':
            # Bubble Sort
            print("Sort by:")
            print("1. Title")
            print("2. Artist")
            print("3. Album")
            print("4. Genre")
            print('5. Likes')
        
            sort_input = input("Enter the number for the sort criteria: ")
            if sort_input == '1':
                key = 'name'
            elif sort_input == '2':
                key = 'artist'
            elif sort_input == '3':
                key = 'album'
            elif sort_input == '4':
                key = 'genre'
            elif sort_input == '5':
                key = 'likes'
            else:
                print("Invalid choice. No sorting applied.")
                return
            start_time = time.time()    
            self.bubble_sort(songs,key) # Führt den Bubble Sort durch
            end_time = time.time()
            print(f"Bubble Sort completed in {end_time - start_time:.6f} seconds") # Zeit für den Sortiervorgang

        elif sorting_algorithm == '2':
            # Merge Sort
            print("Sort by:")
            print("1. Title")
            print("2. Artist")
            print("3. Album")
            print("4. Genre")
            print('5. Likes')
        
            sort_input = input("Enter the number for the sort criteria: ")
            if sort_input == '1':
                key = 'name'
            elif sort_input == '2':
                key = 'artist'
            elif sort_input == '3':
                key = 'album'
            elif sort_input == '4':
                key = 'genre'
            elif sort_input == '5':
                key = 'likes'
            else:
                print("Invalid choice. No sorting applied.")
                return
            
            # Funktion für den Merge Sort
            def merge_sort_songs(songs, key):
                if len(songs) <= 1:
                    return songs # Rückgabe, wenn nur ein Element vorhanden ist

                mid = len(songs) // 2 # Bestimmt die Mitte der Liste
                left_half = merge_sort_songs(songs[:mid], key) # Rekursive Sortierung der linken Hälfte
                right_half = merge_sort_songs(songs[mid:], key) # Rekursive Sortierung der rechten Hälfte

                return merge(left_half, right_half, key) # Führt die beiden Hälften zusammen

            # Funktion zum Zusammenführen von zwei sortierten Listen
            def merge(left, right, key):
                sorted_list = []
                while left and right:  # Solange beide Listen Elemente haben
                    if key == 'likes':
                        if int(getattr(left[0], key)) >= int(getattr(right[0], key)):
                            sorted_list.append(left.pop(0)) # Fügt das Element von der linken Liste hinzu
                        else:
                            sorted_list.append(right.pop(0)) # Fügt das Element von der rechten Liste hinzu
                    else:
                        if getattr(left[0], key) <= getattr(right[0], key):
                            sorted_list.append(left.pop(0))
                        else:
                            sorted_list.append(right.pop(0))


                sorted_list.extend(left)  # Fügt alle verbleibenden Elemente der linken Liste hinzu
                sorted_list.extend(right)  # Fügt alle verbleibenden Elemente der rechten Liste hinzu
        
        
                return sorted_list
            
            start_time = time.time()
            songs[:] = merge_sort_songs(songs,key) # Führt den Merge Sort durch
            end_time = time.time()
            print(f"Merge Sort completed in {end_time - start_time:.6f} seconds") # Zeit für den Sortiervorgang

    def display_all_songs(self):
        # Gibt alle Songs in der Liste aus
        for song in songs:
            print(song)

    def display_playlists(self):
        # Gibt alle Playlists aus
        if not self.playlists:
            print('No playlist available') # Wenn keine Playlists vorhanden sind
        else: 
            for playlist in self.playlists:
                print(playlist) # Gibt jede Playlist aus
    

    def main_menu(self):
        # Hauptmenü der App
        while True:
            print("\n--- Music App ---")
            print("1. Add New Song") # Option, um einen neuen Song hinzuzufügen
            print("2. Create Playlist") # Option, um eine neue Playlist zu erstellen
            print("3. Add Song to Playlist") # Option, um einen Song zur Playlist hinzuzufügen
            print("4. Search Songs") # Option, um nach Songs zu suchen
            print("5. Sort Songs") # Option, um Songs zu sortieren
            print("6. Display All Songs") # Option, um alle Songs anzuzeigen
            print("7. Display Playlists") # Option, um alle Playlists anzuzeigen
            print("8. Exit") # Option, um die App zu beenden

            choice = input("Enter your choice: ") # Benutzer wählt eine Option

            match choice:
                case '1':
                    self.add_song() # Fügt einen neuen Song hinzu
                case '2':
                    self.create_playlist() # Erstellt eine neue Playlist
                case '3':
                    self.add_song_to_playlist() # Fügt einen Song zur Playlist hinzu
                case '4':
                    self.search_songs() # Sucht nach Songs
                case '5':
                    self.sort_songs() # Sortiert die Songs
                case '6':
                    self.display_all_songs() # Zeigt alle Songs an
                case '7':
                    self.display_playlists() # Zeigt alle Playlists an
                case '8':
                    self.save_data() # Speichert die Daten
                    print('Exiting the app') # Bestätigung, dass die App beendet wird
                    break
                case _:
                    print('Invalid choise. Try again.') # Wenn die Eingabe ungültig ist


if __name__ == "__main__":
    app = MusicApp() # Erstellt eine Instanz der Musik-App
    app.main_menu() # Öffnet das Hauptmenü
