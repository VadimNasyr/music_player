import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import pygame
import requests

window = tk.Tk()
window.title("Music Player")
window.geometry("960x540")
icon_path = "icon.ico"
window.resizable(False, False)

pygame.mixer.init()
music_files = []  # Sarašas kuriame saugomos muzikos failai.
current_song_index = 0  # Kintamasis, kuriame saugomas dabartinis grojamas sąrašo indeksą
current_time = tk.IntVar(value=0)  # Kintamasis, kuriame saugomas dabartinis grojamas laikas
artist_label = 0  # Kintamasis, kuriame saugomas artisto vardas
title_label = 0  # Kintamasis, kuriame saugomas dainos pavadinimas


# 1 freimas, skirtas muzikos paieškai.
def search_media():
    global music_var, music_listbox

    search_frame = tk.Frame(window, width=300, height=600, bg="#474747")
    search_frame.pack(side="left")

    search_label = tk.Label(search_frame, text="Media Library", bg="#474747", fg="white", font="Myriad")
    search_label.place(x=100, y=6)

    button = ttk.Button(search_frame, text="Open library", command=select_file)
    button.place(x=100, y=500)

    # Sukuriamas kintamasis, kuriame bus saugomi muzikos failų sąrašąs
    music_var = tk.Variable(value=music_files)

    music_listbox = tk.Listbox(listvariable=music_var, bg="#5b5b5b", fg="white", width=40, height=23)
    music_listbox.place(x=8, y=50)


# Funkcija leidžia vartotojui pasirinktų ".mp3" failą per sistemos dialogo langą.
def select_file():
    filetypes = (('Supported audio files', '*.mp3'),)

    filenames = fd.askopenfilenames(title='Open a file',
                                    initialdir='/',
                                    filetypes=filetypes)

    if filenames:
        for filename in filenames:
            music_files.append(filename)

        open_music(music_files[0])
        music_var.set(music_files)


# 2 freimas, skirtas muzikos grotuvui.
def media_player():
    global tk_img, play_img, pause_img, next_img, previous_img, progress_slider, \
        current_time, elapsed_time, sound_img

    player_frame = tk.Frame(window, bg="#292929", width=360, height=600)
    player_frame.pack(side="left")

    search_label = tk.Label(player_frame, text="Player", bg="#292929", fg="white", font="Myriad")
    search_label.place(x=158, y=6)

    # Įkeliama nuotrauka "backgroud image" su PIL biblioteka ir konvertuojama į tkinterio objektą.
    img = Image.open('bg-image.png')
    img = img.resize((250, 250), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(player_frame, image=tk_img)
    label.place(x=55, y=50)

    # Įkeliama nuotrauka "sound" su PIL biblioteka ir konvertuojama į tkinterio objektą.
    vol_img = Image.open('sound.png')
    sound_img = ImageTk.PhotoImage(vol_img)
    sound_label = tk.Label(player_frame, image=sound_img)
    sound_label.place(x=210, y=410)

    # Sukuriamas mygtukas "play" ir įkeliama nuotrauką.
    play_img = ImageTk.PhotoImage(file="play-button.png")
    play_button = ttk.Button(player_frame, image=play_img, command=play)
    play_button.place(x=135, y=325)

    # Sukuriamas mygtukas "pause" ir įkeliama nuotrauką.
    pause_img = ImageTk.PhotoImage(file="pause.png")
    pause_button = ttk.Button(player_frame, image=pause_img, command=pause)
    pause_button.place(x=185, y=325)

    # Sukuriamas mygtukas "next song" ir įkeliama nuotrauką.
    next_img = ImageTk.PhotoImage(file="next-button.png")
    next_button = ttk.Button(player_frame, image=next_img, command=next_song)
    next_button.place(x=235, y=325)

    # Sukuriamas mygtukas "previous song" ir įkeliama nuotrauką.
    previous_img = ImageTk.PhotoImage(file="previous-button.png")
    previous_button = ttk.Button(player_frame, image=previous_img, command=previous_song)
    previous_button.place(x=85, y=325)

    # Sukuriama progreso juostą.
    progress_slider = ttk.Progressbar(player_frame, orient="horizontal", length=300,
                                      mode="determinate")
    progress_slider.place(x=12, y=380)

    # Sukuriama garsumo skalę.
    volume_var = tk.DoubleVar()  # Sukuriame kintamąjį saugoti garsumui
    volume_scale = ttk.Scale(player_frame, orient="horizontal", from_=0, to=1, variable=volume_var,
                             command=set_volume)
    volume_scale.place(x=253, y=415)

    # Užrašas kusris rodo praėjusį laiką.
    elapsed_time = ttk.Label(player_frame, text="00:00")
    elapsed_time.place(x=320, y=380)


# Funkcija įkelia muzikos failus, nustato default garsą, įjungia dainą ir nustato grojamą vietą.
def open_music(file_name):
    global current_song

    pygame.mixer.music.load(file_name)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    current_song = pygame.mixer.Sound(file_name)


# Funkcija perjungia sekančia dainą
def next_song():
    global current_song_index

    if current_song_index < len(music_files) - 1:
        current_song_index += 1
    else:
        current_song_index = 0
    file_name = music_files[current_song_index]
    open_music(file_name)


# Funkcija perjungia ankstesnę dainą
def previous_song():
    global current_song_index

    if current_song_index > 0:
        current_song_index -= 1
    else:
        current_song_index = len(music_files) - 1
    file_name = music_files[current_song_index]
    open_music(file_name)


def play():
    pygame.mixer.music.unpause()


def pause():
    pygame.mixer.music.pause()


# Funkcija nustato muzikos grojimo garsą.
def set_volume(val):
    volume = float(val)
    pygame.mixer.music.set_volume(volume)


# Funkcija atnaujina laiko eigą.
def update_elapsed_time():
    current_time.set(pygame.mixer.music.get_pos() // 1000)
    elapsed_time.config(text=format_time(current_time.get()))
    elapsed_time.after(1000, update_elapsed_time)


# Funkcija formatuoja laiką į str, formatų "mm:ss"
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"


# Funkcija atnaujina juostą(progress_slider), rodančią dabartinę muzikos grojimo vietą.
def update_progress():
    global current_song

    if pygame.mixer.music.get_busy() and current_song:
        current_time = pygame.mixer.music.get_pos() / 1000
        total_time = current_song.get_length()
        progress_percentage = (current_time / total_time) * 100
        progress_slider["value"] = progress_percentage
    window.after(100, update_progress)


# 3 freimas, skirtas dainos žodžių paiškai.
def find_lyrics():
    global artist_text, title_text, lyrics_frame, text_widget

    lyrics_frame = tk.Frame(window, width=300, height=600,
                            bg="#474747")
    lyrics_frame.pack(side="right")

    lyrics_label = tk.Label(lyrics_frame, text="Search for song lyrics",
                            bg="#474747", fg="white", font="Myriad")
    lyrics_label.place(x=75, y=6)

    artist_label = tk.Label(lyrics_frame, text="Enter the artist's name:",
                            bg="#474747", fg="white", font="Myriad")
    artist_label.place(x=5, y=35)

    artist_name_label = tk.Label(lyrics_frame, text="Artist name:",
                                 bg="#474747", fg="white", font="Myriad")
    artist_name_label.place(x=5, y=160)

    song_title_label = tk.Label(lyrics_frame, text="Song title:",
                                bg="#474747", fg="white", font="Myriad")
    song_title_label.place(x=5, y=190)

    # Įvesties laukas artisto vardui.
    artist_text = ttk.Entry(lyrics_frame)
    artist_text.bind("<Return>", lambda event: artist())
    artist_text.place(x=80, y=75, anchor="center")

    # Mygtukas įvestos dainos artisto išvesti.
    btn_artist = ttk.Button(lyrics_frame, text="Click", command=artist)
    btn_artist.place(x=170, y=62)

    # Užrašas "Enter song title:".
    title_label = tk.Label(lyrics_frame, text="Enter song title:",
                           bg="#474747", fg="white", font="Myriad")
    title_label.place(x=5, y=95)

    # Įvesties laukas dainos pavadinimui.
    title_text = ttk.Entry(lyrics_frame)
    title_text.bind("<Return>", lambda event: title())
    title_text.place(x=80, y=135, anchor="center")

    # Mygtukas dainos pavadimui išvesti.
    btn_title = ttk.Button(lyrics_frame, text="Click", command=title)
    btn_title.place(x=170, y=122)

    # Mygtukas dainos žodžių paieškai.
    btn_search = ttk.Button(lyrics_frame, text="Search", command=search_song)
    btn_search.place(x=60, y=225)

    # Teksto laukas, kuriame bus rodomas paieškos rezultatas.
    text_widget = tk.Text(lyrics_frame, wrap="word", bg="#5b5b5b", fg="white", width=35, height=15)
    text_widget.place(x=8, y=260)

    # Mygtukas teksto valymui.
    btn_clear = ttk.Button(lyrics_frame, text="Clear", command=clear)
    btn_clear.place(x=170, y=225)


# Funkcijoje gaunam vartotojo įvestą tekstą.
def artist():
    global artist_input, artist_label

    artist_input = artist_text.get().capitalize()
    if artist_label:
        artist_label.destroy()
    artist_label = tk.Label(lyrics_frame, text=artist_input, bg="#474747", fg="white", font="Myriad")
    artist_label.place(x=90, y=161)


# Funkcijoje gaunam vartotojo įvestą dainos pavadinimą.
def title():
    global title_input, title_label

    title_input = title_text.get().capitalize()
    if title_label:
        title_label.destroy()
    title_label = tk.Label(lyrics_frame, text=title_input, bg="#474747", fg="white", font="Myriad")
    title_label.place(x=90, y=190)


# Funkcija paleidžia music_lyrics_api(), išvalo tekstą iš lauko ir įterpia funkcijos music_lyrics_api() rezultatą.
def search_song():
    music_lyrics_api()
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, clear_lyrics)


# Funkcija išvalo title, artist ir rezultato teksto laukus.
def clear():
    artist_text.delete(0, tk.END)
    title_text.delete(0, tk.END)
    text_widget.delete("1.0", tk.END)


# Funkcija gauiti dainos žodžius, įvedus artisto ir dainos pavadinimą.
def music_lyrics_api():
    global clear_lyrics, artist_input, title_input

    r = requests.get(f"https://api.lyrics.ovh/v1/{artist_input}/{title_input}")

    sarasas = r.json()
    lyrics = sarasas.get('lyrics')
    if lyrics:
        split_lines = lyrics.splitlines()
        clear_lyrics = '\n'.join(split_lines[1:])
    else:
        clear_lyrics = "No lyrics found for this song."


search_media()
media_player()
find_lyrics()
update_progress()
update_elapsed_time()

window.iconbitmap(icon_path)
window.mainloop()
