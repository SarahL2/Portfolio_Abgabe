import csv
import os
import time

songs= []

class Song:
    def __init__(self, name, artist, album, genre, likes):
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.likes = likes


    def __str__(self):
        return f"{self.name} by {self.artist} - Album: {self.album}, Genre: {self.genre}, Likes: {self.likes}"

    def to_dict(self):
        return {
            'name': self.name,
            'artist': self.artist,
            'album': self.album,
            'genre': self.genre,
            'likes': self.likes
        }

    @staticmethod
    def from_dict(data):
        return Song(data['name'], data['artist'], data['album'], data['genre'], data['likes'])

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __str__(self):
        return f"Playlist: {self.name}, Songs: {len(self.songs)}"

    def to_dict(self):
        return {
            'name': self.name,
            'songs': [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist

class MusicApp:
    def __init__(self, data_file='C:\\Users\\Admin\\visiual_studio_code_projects\\Fortgeschrittene Programmierung\\Toth\\Musik_App\\songs_10000'):
        self.data_file = data_file
        self.playlists = []
        self.songs = []
        self.load_data()

    def load_data(self):
        with open(self.data_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)

            loading_playlists = False
            
            for row in csv_reader:
                if row == []:
                    loading_playlists = True
                    continue

                elif not loading_playlists:
                    song_objekt = Song(row[0],row[1],row[2],row[3],row[4])
                    songs.append(song_objekt)
                else:
                    playlist_name = row[0]
                    song_title = row[1]

                    playlist = next((p for p in self.playlists if p.name == playlist_name), None)

                    if not playlist:
                        playlist = Playlist(playlist_name)
                        self.playlists.append(playlist)

                    for playlist in self.playlists:
                        for s in songs:
                            if s.name == song_title and s not in playlist.songs:                         
                                playlist.add_song(s)

        print('Data succesfully loaded')
    
    def save_data(self):
        with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for song in songs:
                writer.writerow([song.name,song.artist,song.album,song.genre,song.likes])
            
            writer.writerow([])

            for playlist in self.playlists:
                for song in playlist.songs:
                    writer.writerow([playlist.name, song.name])                   


        print('Data saved successfully.')

    def add_song(self):
        name = input("Enter song name: ")
        artist = input("Enter artist name: ")
        album = input("Enter album name: ")
        genre = input("Enter genre: ")
        likes = input('Enter your likes: ')
        song = Song(name, artist, album, genre, likes)
        songs.append(song)
        print(f"Added song: {song}")


    def create_playlist(self):
        name = input("Enter playlist name: ")
        playlist = Playlist(name)
        self.playlists.append(playlist)
        print(f"Created playlist: {playlist}")

    def add_song_to_playlist(self):
        playlist_name = input('Enter the name of the playlist: ')
        for playlist in self.playlists:
            if playlist.name == playlist_name:
                song_name = input('Enter the song to be added: ')
                for s in songs:
                    if s.name == song_name:                         
                        playlist.add_song(s)
                        print(f"Added {s.name} to playlist {playlist.name}")
                    else:
                        print('Song not found')

            else:
                print('Playlist not found')


    def bubble_sort(self,songs,key):
        n = len(songs)
        for i in range(n):
            swapped = False
        
            for j in range(0, n-i-1):
                if key == 'likes':
                    if int(getattr(songs[j], key)) < int(getattr(songs[j+1], key)):
                        songs[j], songs[j+1] = songs[j+1], songs[j] 
                        swapped = True
                else:
                    if getattr(songs[j], key) > getattr(songs[j+1], key):  
                        songs[j], songs[j+1] = songs[j+1], songs[j]
                        swapped = True
            if not swapped:
                break
        
        
    def search_songs(self):
        print('1. Linear Search')
        print('2. Binary Serach')
        searching_algorithm = input('Enter the searching algorithm: ')


        if searching_algorithm == '1':
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
                start_time = time.time()
                matches = []
                for song in songs:
                    if getattr(song, key).lower() == search_value.lower():
                        matches.append(song)
                end_time = time.time()  
                print(f"Linear Search completed in {end_time - start_time:.6f} seconds")
                return matches
            
            matching_songs = linear_search(songs, key, search_value)

            if matching_songs:
                print(f"Found {len(matching_songs)} song(s)")
                for song in matching_songs:
                    print(song)
            else:
                print("No songs found")

        if searching_algorithm == '2':
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

            self.bubble_sort(songs,key)

            def binary_search(songs, key, search_value):
                start_time = time.time()
                low = 0
                high = len(songs) - 1

                while low <= high:
                    mid = (low + high) // 2
                    if getattr(songs[mid], key).lower() == search_value.lower():
                        end_time = time.time()  
                        print(f"Binary Search completed in {end_time - start_time:.6f} seconds")
                        return mid  
                    elif getattr(songs[mid], key).lower() < search_value.lower():
                        low = mid + 1  
                    else:
                        high = mid - 1  
                end_time = time.time()  
                print(f"Binary Search completed in {end_time - start_time:.6f} seconds")
                return -1 
            index = binary_search(songs,key,search_value)

            if index != -1:
                print(f"Song found: {songs[index]}")
            else:
                print("No songs found")


    def sort_songs(self):
        print('1. Bubble Sort')
        print('2. Merge Sort')
        sorting_algorithm = input('Enter the sorting algorithm: ')
        
        if sorting_algorithm == '1':

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
            self.bubble_sort(songs,key)
            end_time = time.time()
            print(f"Bubble Sort completed in {end_time - start_time:.6f} seconds")

        elif sorting_algorithm == '2':
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
            

            def merge_sort_songs(songs, key):
                if len(songs) <= 1:
                    return songs

                mid = len(songs) // 2
                left_half = merge_sort_songs(songs[:mid], key)
                right_half = merge_sort_songs(songs[mid:], key)

                return merge(left_half, right_half, key)

            def merge(left, right, key):
                sorted_list = []
                while left and right:
                    if key == 'likes':
                        if int(getattr(left[0], key)) >= int(getattr(right[0], key)):
                            sorted_list.append(left.pop(0))
                        else:
                            sorted_list.append(right.pop(0))
                    else:
                        if getattr(left[0], key) <= getattr(right[0], key):
                            sorted_list.append(left.pop(0))
                        else:
                            sorted_list.append(right.pop(0))


                sorted_list.extend(left)
                sorted_list.extend(right)
        
                return sorted_list
            
            start_time = time.time()
            songs[:] = merge_sort_songs(songs,key)
            end_time = time.time()
            print(f"Merge Sort completed in {end_time - start_time:.6f} seconds")
    

    def display_all_songs(self):
        for song in songs:
            print(song)

    def display_playlists(self):
        if not self.playlists:
            print('No playlist available')
        else: 
            for playlist in self.playlists:
                print(playlist)
    

    def main_menu(self):
        while True:
            print("\n--- Music App ---")
            print("1. Add New Song")
            print("2. Create Playlist")
            print("3. Add Song to Playlist")
            print("4. Search Songs")
            print("5. Sort Songs")
            print("6. Display All Songs")
            print("7. Display Playlists")
            print("8. Exit")

            choice = input("Enter your choice: ")

            match choice:
                case '1':
                    self.add_song()
                case '2':
                    self.create_playlist()
                case '3':
                    self.add_song_to_playlist()
                case '4':
                    self.search_songs()
                case '5':
                    self.sort_songs()
                case '6':
                    self.display_all_songs()
                case '7':
                    self.display_playlists()
                case '8':
                    self.save_data()
                    print('Exiting the app')
                    break
                case _:
                    print('Invalid choise. Try again.')


if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()