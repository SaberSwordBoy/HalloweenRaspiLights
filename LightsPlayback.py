import pygame
import os
import itertools
import json

pygame.init()

# Variables
BOX_SIZE = 110
WINDOW_SIZE = (1280,720)
SONGS_FOLDER = "./songs/"
VOLUME = 0.5

# window stuff / pygame setup
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Raspi Lights")
clock = pygame.time.Clock()

# indicator boxes
indicators = [
    {"key": ["a", pygame.K_a],
     "colors": ["white", "red"],
     "x": 100,
     "y": 100},
    
    {"key": ["b", pygame.K_b],
     "colors": ["lightblue", "blue"],
     "x": 100,
     "y": 225},
    
    {"key": ["c", pygame.K_c],
     "colors": ["darkgray", "yellow"],
     "x": 100,
     "y": 350},

    {"key": ["d", pygame.K_d],
     "colors": ["darkgray", "green"],
     "x": 225,
     "y": 350},

    {"key": ["e", pygame.K_e],
     "colors": ["white", "orange"],
     "x": 1079,
     "y": 100},

    {"key": ["f", pygame.K_f],
     "colors": ["white", "purple"],
     "x": 1079,
     "y": 225},

    {"key": ["g", pygame.K_g],
     "colors": ["white", "brown"],
     "x": 954,
     "y": 350},

    {"key": ["h", pygame.K_h],
     "colors": ["white", "cyan"],
     "x": 1079,
     "y": 350}
]

# fonts and text
status_font = pygame.font.SysFont("arial", 25)
pos_text = status_font.render("hi", True, (233, 244, 244))
fps_text = status_font.render("hi", True, (233, 244, 244))

title_font = pygame.font.SysFont("Arial", 35)
title_text = title_font.render("Raspi Light Show Programmer", True, (255, 255, 40))
main_timer_text = title_font.render("0.0.0", True, (50, 245, 45))
current_song_text = title_font.render("PRESS CYCLE TO LOAD SONG", True, (50, 245, 45))

# timer setup
timer_running = False
timer = 0

#music playback
songs = []
song_cycle = itertools.cycle(songs)
for root, dirs, files in os.walk(SONGS_FOLDER):
    for file in files:
        if ".mp3" in file and "lightshow" not in file:
            songs.append(file)

current_song = next(song_cycle)
pygame.mixer.music.load(SONGS_FOLDER + current_song)
pygame.mixer.music.set_volume(VOLUME)

# getting inputs
try:
    with open(SONGS_FOLDER + current_song + ".lightshow", "r") as input_file:
        recorded_input = json.load(input_file)
except FileNotFoundError:
    title_text = title_font.render("Switch To Song with recorded data", True, (255, 255, 40))
    recorded_input = {'0': None}


# FUNCTIONS
def save_data_file():
    with open(SONGS_FOLDER + current_song + ".lightshow", "w") as raw_file:
        raw_file.write(json.dumps(recorded_data))

def cycle_songs():
    global current_song
    global recorded_data
    global recorded_input
    current_song = next(song_cycle)
    pygame.mixer.music.load(SONGS_FOLDER + current_song)
    with open(SONGS_FOLDER + current_song + ".lightshow", "r") as input_file:
        recorded_input = json.load(input_file)

def play():
    pygame.mixer.music.play(start=timer/60)

def pause():
    pygame.mixer.music.pause()


def update(events, keys):
    global timer_running
    global timer
    global pos_text
    global main_timer_text
    global current_song_text
    global fps_text
    global running

    pos_text = status_font.render(str(pygame.mouse.get_pos()) + " timer: " + str(timer), True, (233, 244, 244))
    fps_text = status_font.render(str(round(clock.get_fps())), False, (233, 244, 244))
    main_timer_text = status_font.render("{}".format(round(timer / 60, 2)), False, (143, 244, 156))
    current_song_text = title_font.render(current_song, True, (50, 245, 45))
    
    window.fill((44, 44, 46))
    window.blit(pos_text, (10, 10))
    window.blit(fps_text, (10, 35))
    window.blit(title_text, (WINDOW_SIZE[0] // 2 - (title_text.get_width() //2 ), 50))
    window.blit(main_timer_text, (WINDOW_SIZE[0] // 2 - (main_timer_text.get_width() // 2), 100))
    window.blit(current_song_text, (WINDOW_SIZE[0] // 2 - (current_song_text.get_width() // 2), 150))

    current_indicators = recorded_input[str(timer)]
    for box in indicators:
        for key, _ in current_indicators:
            if key == box['key'][1]:
                pygame.draw.rect(window,
                                 pygame.Color(box["colors"][0]),
                                 (box['x'], box['y'], BOX_SIZE, BOX_SIZE))
            else:
                pygame.draw.rect(window,
                                 pygame.Color(box["colors"][1]),
                                 (box['x'], box['y'], BOX_SIZE, BOX_SIZE))

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                timer_running = True
                play()

            elif event.key == pygame.K_2:
                timer_running = False
                pause()

            elif event.key == pygame.K_3:
                timer = 0

            elif event.key == pygame.K_4:
                cycle_songs()

    if timer_running:
        timer += 1

running = True
while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    update(events, keys)
    pygame.display.flip()
    clock.tick(60)