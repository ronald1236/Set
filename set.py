import pygame
import os 
import random

# activeer de pygame library
pygame.init()
pygame.font.init()

# aantal secondes voordat de computer reageert
difficulty = 30

# zet start score
player_score = 0
computer_score = 0

# zet start values
last_clicked = 12
clicked = []
clicks = 0

# maak een scherm aan (4 bij 3 kaarten)
screen = pygame.display.set_mode((416, 662))

# begin timer
start_time = pygame.time.get_ticks()

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
def draw_score(player_score, computer_score):
    player_text = score_font.render(f"Player: {player_score}", True, (255, 255, 255))
    computer_text = score_font.render(f"Computer: {computer_score}", True, (255, 255, 255))
    screen.blit(player_text, (10, 615))
    screen.blit(computer_text, (215, 615))

# kies 12 random start kaarten
start_kaarten = random.sample(list(image_dict),12)

# krijg de positie van een kaart in start_kaarten lijst
def get_kaart_pos(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    if 0 <= col < 4 and 0 <= row < 3:
        return row * 4 + col
    return None

# maak rand om de geklickte kaart groen
def show_clicked(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    screen.fill('green', rect = (col * 104, row * 204, 104, 204))

# zet een de naam van een kaart om naar een tuple (#,#,#,#)
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

# maakt een blauwe rand om een set
def show_set(set):
    for kaart in set:
        row = kaart // 4
        col = kaart % 4
        screen.fill('blue', rect = (col * 104, row * 204, 104, 204))
        kaart_key = start_kaarten[kaart]
        kaart_image = image_dict[kaart_key]
        screen.blit(kaart_image, (2 + col * 104, 2 + row * 204))

# message if no set is found
def show_no_set_message():
    font = pygame.font.SysFont("Arial", 36)
    text = font.render("Geen SET gevonden!", True, (255, 0, 0))
    screen.blit(text, (80, 300))  # center-ish
    pygame.display.flip()

# zoek naar een set
def find_set():
    global computer_score, clicked, clicks, last_clicked
    for i in range (12):
        for j in range (i + 1, 12):
            for k in range (j + 1,12):
                if is_set([i, j, k]):
                    show_set([i, j, k])
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    screen.fill('black')
                    new_kaarten([i, j, k])
                    computer_score += 1
                    clicked = []
                    clicks = 0
                    last_clicked = 12
                    return
    show_no_set_message()
    pygame.time.wait(1500)
    screen.fill('black')
    change_cards()

# verandert de eerste drie kaarten
def change_cards():
    new_kaarten([0, 1, 2])

# check of 3 kaarten een set zijn
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

# checkt of 3 eigenschappen alle drie gelijk of alle drie anders zijn
def check(list):
    length = len(set(list))
    if length == 1 or length == 3:
        return True
    return False

# vervangt kaarten
def new_kaarten(clicked):
    for pos in clicked:
        start_kaarten[pos] = new_kaart()

# kiest random een nieuwe kaart die nog niet op het bord ligt
def new_kaart():
    new = random.choice([i for i in list(image_dict.keys()) if i not in start_kaarten])
    return new

# Main loop
running = True
while running:
    if pygame.time.get_ticks() - start_time >= difficulty * 1000:
        find_set()
        start_time = pygame.time.get_ticks() # reset timer
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
                            player_score += 1
                            new_kaarten(clicked)
                            start_time = pygame.time.get_ticks()
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
    screen.fill('black', rect=(0, 612, 416, 50))
    draw_score(player_score, computer_score)
    pygame.display.flip()

# Clean up
pygame.quit()