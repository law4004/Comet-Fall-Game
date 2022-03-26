import pygame
import math
from game import Game

pygame.init()

# generer la fenetre du jeu
pygame.display.set_caption("Comet Fall Game")
screen = pygame.display.set_mode((1080, 720))

# importer l'arriere plan du jeu
background = pygame.image.load('assets/bg.jpg')

# importer la banniere
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

# importer le bouton pour lancer la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

# charger le jeu
game = Game()

running = True

# boucle tant que running = True
while running is True:

    # appliquer l'arriere plan du jeu
    screen.blit(background, (0, -200))

    for projectile in game.player.all_projectiles:
        projectile.move()

    # verifier si le jeu a commence ou non
    if game.is_playing:
        # declencher les instructions de la partie
        game.update(screen)
    # verifier si le jeu n'a pas commence
    else:
        # ajouter l'ecran de bienvenue
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    # mettre a jour l'ecran
    pygame.display.flip()

    # si le joueur ferme cette fenetre
    for event in pygame.event.get():
        # verifier que l'event est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # detecter si un joueur appuie sur une touche du keyboard
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # detecter si la touche espace est enclenchee pour lancer le projectile
            if event.key == pygame.K_SPACE:
                game.start()
                # jouer le son
               # game.sound_manager.play('click')

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # mettre le jeu en mode "lance"
            game.player.launch_projectile()
