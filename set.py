# importing required library
import pygame
import os 
import random

# activate the pygame library .
pygame.init()

# maak een scherm aan (4 bij 3 kaarten)
screen = pygame.display.set_mode((403, 602))

# laad alle kaarten
def load_images(path_to_directory):
    image_dict = {}
    key = 0
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.gif'):
            path = os.path.join(path_to_directory, filename)
            image_dict[key] = pygame.image.load(path).convert()
            key += 1
    return image_dict

image_dict = load_images(r"kaarten")

# kies 12 random start kaarten
start_kaarten = random.sample(list(image_dict),12)

def get_kaart(pos):
    x, y = pos
    col = x // 101
    row = y // 201
    if 0 <= col < 4 and 0 <= row < 3:
        return row * 4 + col
    return None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(get_kaart(pos))

    i = 0
    for x in range(4):
        for y in range(3):
            kaart = image_dict[start_kaarten[i]]
            screen.blit(kaart, (x * 101, y * 201))
            y += 1
            i += 1
        x += 1
    pygame.display.flip()

# Clean up
pygame.quit()