import pygame

pygame.init()


window_size = (600, 600)
window_width, window_height = window_size
window_name = "Chess V3"

window = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_name)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

