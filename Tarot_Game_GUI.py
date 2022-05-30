import pygame

def init_game_ui():

    # Margins
    MARGIN_LEFT = 230
    MARGIN_TOP = 150

    # WINDOW SIZE
    WIDTH = 800
    HEIGHT = 600

    # COLORS
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (110, 110, 110)
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (0, 120, 0)
    RED = (255, 0, 0)
    LIGHT_RED = (120, 0, 0)

    # Initializing PyGame
    pygame.init()

    # Setting up the screen and background
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRAY)

    # Setting up caption
    pygame.display.set_caption("Tarot Africain")

    # Loading image for the icon
    # icon = pygame.image.load('icon.jpeg')

    # Setting the game icon
    # pygame.display.set_icon(icon)

    # Types of fonts to be used
    small_font = pygame.font.Font(None, 32)
    large_font = pygame.font.Font(None, 50)

# Load the card image
# prev_card = pygame.image.load(r'./ui/cartes/Dos.png')

# Scaling the loaded image
# prev_card = pygame.transform.scale(prev_card, (100, 160))

# The GAME LOOP
# while True:
#
#     # Tracking the mouse movements
#     mouse = pygame.mouse.get_pos()
#
#     # Loop events occuring inside the game window
#     for event in pygame.event.get():
#
#         # Quitting event
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#
#         # Left-mouse clicked event
#         if not over and event.type == pygame.MOUSEBUTTONDOWN:
#
#             # Clicked on the High Button
#             if 220 <= mouse[0] <= 220 + 125 and 370 <= mouse[1] <= 370 + 60:
#                 choice = 1
#
#             # Clicked on the Low Button
#             if 460 <= mouse[0] <= 460 + 120 and 370 <= mouse[1] <= 370 + 60:
#                 choice = 0
#
#
#         # Displaying scoreboard
#     pygame.draw.rect(screen, WHITE, [270, 40, 255, 90])
#     score_text = small_font.render("Score = " + str(score), True, BLACK)
#     score_text_rect = score_text.get_rect()
#     score_text_rect.center = (WIDTH // 2, 70)
#
#     chances_text = small_font.render("Chances = " + str(chances), True, BLACK)
#     chances_text_rect = chances_text.get_rect()
#     chances_text_rect.center = (WIDTH // 2, 100)
#
#
#     # If the game is finished, display the final score
#     if over:
#         pygame.draw.rect(screen, WHITE, [270, 40, 255, 90])
#         score_text = small_font.render("Final Score = " + str(score), True, BLACK)
#         score_text_rect = score_text.get_rect()
#         score_text_rect.center = (WIDTH // 2, 85)
#         screen.blit(score_text, score_text_rect)
#
#     # Update the display after each game loop
#     pygame.display.update()
