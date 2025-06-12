# importing required library
import pygame
import os 
import random

# activate the pygame library .
pygame.init()
pygame.font.init()

# maak een scherm aan (4 bij 3 kaarten)
screen = pygame.display.set_mode((416, 662))

# laad alle kaarten
def load_images(path_to_directory):
    image_dict = {}
    filename_dict = {}
    key = 0
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.gif'):
            path = os.path.join(path_to_directory, filename)
            image_dict[key] = pygame.image.load(path).convert()
            filename_dict[key] = filename
            key += 1
    return image_dict, filename_dict

image_dict, filename_dict = load_images(r"kaarten")

#scorebord laten zien
score_font = pygame.font.SysFont("Arial", 30)
def draw_score(score):
    text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 620)) 

# kies 12 random start kaarten
start_kaarten = random.sample(list(image_dict),12)

def get_kaart(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    if 0 <= col < 4 and 0 <= row < 3:
        return start_kaarten[row * 4 + col]
    return None

def get_kaart_pos(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    if 0 <= col < 4 and 0 <= row < 3:
        return row * 4 + col
    return None

def show_clicked(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    screen.fill('green', rect = (col * 104, row * 204, 104, 204))

def kaart_naar_tuple(kaart_pos):
    kaart_key = start_kaarten[kaart_pos]
    filename = filename_dict[kaart_key]
    name = filename.replace('.gif', '')

    if name.startswith('green'):
        kleur = 0
        name = name[5:]
    elif name.startswith('purple'):
        kleur = 1
        name = name[6:]
    elif name.startswith('red'):
        kleur = 2
        name = name[3:]

    if name.startswith('diamond'):
        vorm = 0
        name = name[7:]
    elif name.startswith('oval'):
        vorm = 1
        name = name[4:]
    elif name.startswith('squiggle'):
        vorm = 2
        name = name[8:]

    if name.startswith('empty'):
        vulling = 0
        name = name[5:]
    elif name.startswith('filled'):
        vulling = 1
        name = name[6:]
    elif name.startswith('shaded'):
        vulling = 2
        name = name[6:]

    if name == '1':
        aantal = 0
    elif name == '2':
        aantal = 1
    elif name == '3':
        aantal = 2

    return (kleur, vorm, vulling, aantal)
        

def is_set(clicked):
    kaart_tuples = []
    for kaart_pos in clicked:
        kaart_tuples.append(kaart_naar_tuple(kaart_pos))
    kleuren = []
    vormen = []
    vulling = []
    aantallen = []
    for kaart in kaart_tuples:
        kleuren.append(kaart[0])
        vormen.append(kaart[1])
        vulling.append(kaart[2])
        aantallen.append(kaart[3])
    if check(kleuren):
        if check(vormen):
            if check(vulling):
                if check(aantallen):
                    return True
    return False

def check(list):
    length = len(set(list))
    if length == 1 or length == 3:
        return True
    return False

def new_kaarten(clicked):
    for pos in clicked:
        start_kaarten[pos] = new_kaart()

def new_kaart():
    new = random.choice([i for i in list(image_dict.keys()) if i not in start_kaarten])
    return new

score = 0
score_increment = 1

# Main loop
running = True
last_clicked = 12
clicked = []
clicks = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            kaart_positie = get_kaart_pos(pos)
            if last_clicked != kaart_positie:
                if clicks < 3:
                    show_clicked(pos)
                    clicked.append(kaart_positie)
                    clicks += 1
                    last_clicked = kaart_positie
                    if clicks == 3:
                        if is_set(clicked):
                            score += score_increment
                            new_kaarten(clicked)
                        clicked = []
                        clicks = 0
                        screen.fill('black')
                        last_clicked = 13


    i = 0
    for y in range(3):
        for x in range(4):
            kaart_key = start_kaarten[i]
            kaart = image_dict[kaart_key]
            screen.blit(kaart, (2 + x * 104, 2 + y * 204))
            i += 1
    screen.fill('black', rect=(0, 662, 416, 40))
    draw_score(score)
    pygame.display.flip()

# Clean up
pygame.quit()