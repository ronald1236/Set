import pygame
import os 
import random

# activate the pygame lybrary
pygame.init()
pygame.font.init()

# Create the display screen (3 by 4 cards)
screen = pygame.display.set_mode((416, 662))
pygame.display.set_caption("SET Game")

# load all cards into two dictionaries, one storing the images and one storing the filenames
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

image_dict, filename_dict = load_images(r"cards")

# Starting screen where you can select the difficulty
def show_start_screen():
    font_title = pygame.font.Font(None, 72)
    font_button = pygame.font.Font(None, 36)
    font_subtitle = pygame.font.Font(None, 24)
    
    selected = False
    difficulty = 30 

    buttons = [
        {"rect": pygame.Rect(108, 200, 200, 60), "label": "Easy (45s)", "value": 45, "color": (0, 200, 0)},
        {"rect": pygame.Rect(108, 300, 200, 60), "label": "Normal (30s)", "value": 30, "color": (255, 255, 0)},
        {"rect": pygame.Rect(108, 400, 200, 60), "label": "Hard (15s)", "value": 15, "color": (200, 0, 0)},
    ]

    while not selected:
        screen.fill((40, 40, 40))
        
        title_text = font_title.render("SET GAME", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(208, 80))
        screen.blit(title_text, title_rect)
        
        subtitle_text = font_subtitle.render("Select difficulty level:", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(208, 150))
        screen.blit(subtitle_text, subtitle_rect)
        
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            pygame.draw.rect(screen, (0, 0, 0), button["rect"], 3)
            text = font_button.render(button["label"], True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)

        instruction_text = font_subtitle.render("Computer will find a set after the time limit", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(208, 550))
        screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()

        # Check for click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button["rect"].collidepoint(pos):
                        difficulty = button["value"]
                        selected = True
                        break
    
    return difficulty

# Get the difficulty
difficulty = show_start_screen()

# Set starting variables
player_score = 0
computer_score = 0
last_clicked = 12
clicked = []
clicks = 0

# Start timer
start_time = pygame.time.get_ticks()

# Shows the scoreboard
score_font = pygame.font.SysFont("Arial", 30)
def draw_score(player_score, computer_score):
    player_text = score_font.render(f"Player: {player_score}", True, (255, 255, 255))
    computer_text = score_font.render(f"Computer: {computer_score}", True, (255, 255, 255))
    screen.blit(player_text, (10, 615))
    screen.blit(computer_text, (215, 615))

# Choose 12 random starting cards
playing_cards = random.sample(list(image_dict),12)

# Helper functions

# Gets the position of the card in playing_cards based on coordinates on the screen
def get_card_pos(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    if 0 <= col < 4 and 0 <= row < 3:
        return row * 4 + col
    return None

# Creates a green outline
def show_clicked(pos):
    x, y = pos
    col = x // 104
    row = y // 204
    screen.fill('green', rect = (col * 104, row * 204, 104, 204))

# Changes the name of a card to tuple with 4 values, one for each attribute (#,#,#,#)
def card_to_tuple(card_pos):
    card_key = playing_cards[card_pos]
    filename = filename_dict[card_key]
    name = filename.replace('.gif', '')

    if name.startswith('green'):
        color = 0
        name = name[5:]
    elif name.startswith('purple'):
        color = 1
        name = name[6:]
    elif name.startswith('red'):
        color = 2
        name = name[3:]

    if name.startswith('diamond'):
        shape = 0
        name = name[7:]
    elif name.startswith('oval'):
        shape = 1
        name = name[4:]
    elif name.startswith('squiggle'):
        shape = 2
        name = name[8:]

    if name.startswith('empty'):
        shading = 0
        name = name[5:]
    elif name.startswith('filled'):
        shading = 1
        name = name[6:]
    elif name.startswith('shaded'):
        shading = 2
        name = name[6:]

    if name == '1':
        number = 0
    elif name == '2':
        number = 1
    elif name == '3':
        number = 2

    return (color, shape, shading, number)

# Shows a blue outline around a set of cards
def show_set(set):
    for card in set:
        row = card // 4
        col = card % 4
        screen.fill('blue', rect = (col * 104, row * 204, 104, 204))
        card_key = playing_cards[card]
        card_image = image_dict[card_key]
        screen.blit(card_image, (2 + col * 104, 2 + row * 204))

# Shows a message when no set is found
def show_no_set_message():
    font = pygame.font.SysFont("Arial", 36)
    text = font.render("No SET Found!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(208, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()

# Swaps the first 3 cards on the board
def change_cards():
    new_cards([0, 1, 2])

# replaces 3 cards, if there are still cards in the deck
def new_cards(clicked):
    global difficulty
    if len(image_dict) > 12:
        for pos in clicked:
            card_key = playing_cards[pos]
            del image_dict[card_key]
            playing_cards[pos] = new_card()
    elif find_all_sets():
        for pos in clicked:
            card_key = playing_cards[pos]
            del image_dict[card_key]
            playing_cards[pos] = None
    else:
        end_game()

# Chooses a new random card from the deck that is not on the baord
def new_card():
    new = random.choice([i for i in list(image_dict.keys()) if i not in playing_cards])
    return new


# Shows ending screen and closes the game
def end_game():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("Arial", 48)
    
    if player_score > computer_score:
        text = font.render("YOU WON!", True, (0, 255, 0))
    elif computer_score > player_score:
        text = font.render("COMPUTER WON!", True, (255, 0, 0))
    else:
        text = font.render("DRAW!", True, (0, 0, 255))
    
    text_rect = text.get_rect(center=(208, 331))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    exit()

# Functions for the main algorithm

# Finds all possible sets on the board
def find_all_sets():
    sets = []
    for i in range (12):
        for j in range (i + 1, 12):
            for k in range (j + 1,12):
                if is_set([i, j, k]):
                    sets.append([i, j, k])
    return sets
                    
# Finds the first possible set
def find_set():
    global computer_score, clicked, clicks, last_clicked
    for i in range (12):
        for j in range (i + 1, 12):
            for k in range (j + 1,12):
                if is_set([i, j, k]):
                    show_set([i, j, k])
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    screen.fill('black')
                    new_cards([i, j, k])
                    computer_score += 1
                    clicked = []
                    clicks = 0
                    last_clicked = 12
                    return
    show_no_set_message()
    pygame.time.wait(1500)
    screen.fill('black')
    change_cards()

# Checks if 3 card make a set
def is_set(clicked):
    card_tuples = []
    for card_pos in clicked:
        if playing_cards[card_pos] == None:
            return False
        card_tuples.append(card_to_tuple(card_pos))
    colors = []
    shapes = []
    shadings = []
    numbers = []
    for card in card_tuples:
        colors.append(card[0])
        shapes.append(card[1])
        shadings.append(card[2])
        numbers.append(card[3])
    if check(colors):
        if check(shapes):
            if check(shadings):
                if check(numbers):
                    return True
    return False

# Checks if 3 attributes are all the same, or all different
def check(list):
    length = len(set(list))
    if length == 1 or length == 3:
        return True
    return False

# Clear the screen before starting the game
screen.fill('black')

# Main game loop
running = True
while running:
    if pygame.time.get_ticks() - start_time >= difficulty * 1000: # If timelimit has passed computer makes a move
        find_set()
        start_time = pygame.time.get_ticks() # reset timer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pos[1] < 612:
                card_position = get_card_pos(pos)
                if last_clicked != card_position and playing_cards[card_position] != None:
                    if clicks < 3:
                        show_clicked(pos)
                        clicked.append(card_position)
                        clicks += 1
                        last_clicked = card_position
                        if clicks == 3: # If 3 cards are clicked, start checking if they are a set
                            if is_set(clicked):
                                player_score += 1
                                new_cards(clicked)
                                start_time = pygame.time.get_ticks()
                            clicked = []
                            clicks = 0
                            screen.fill('black')
                            last_clicked = 13
    # draws the board
    i = 0
    for y in range(3):
        for x in range(4):
            if playing_cards[i] != None:
                card_key = playing_cards[i]
                card = image_dict[card_key]
                screen.blit(card, (2 + x * 104, 2 + y * 204))
            i += 1
    screen.fill('black', rect=(0, 612, 416, 50))
    draw_score(player_score, computer_score)
    pygame.display.flip()

# Clean up
pygame.quit()