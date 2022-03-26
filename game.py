import pygame

from comet_event import CometFallEvent
from monster import Mummy
from player import Player
from sounds import SoundManager

# creation d'une seconde classe qui va representer le jeu
class Game:

    def __init__(self):
        # definir si le jeu a commence ou non
        self.is_playing = False
        # generer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # generer l'evenement
        self.comet_event = CometFallEvent(self)
        # groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        # gerer le son
        # self.sound_manager = SoundManager()
        # mettre le score a 0
        self.font = pygame.font.Font("assets/PottaOne-Regular.ttf", 25)
        self.score = 0
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()

    def add_score(self, points):
        self.score += points

    def game_over(self):
        print("Votre score est de " + str(self.score) + " points !")
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        # jouer le son
        # self.sound_manager.play('game_over')

    def update(self, screen):
        # afficher le score sur l'ecran
        score_text = self.font.render(f"Score : {self.score}", 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        # appliquer l'image du joueur
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        # actualiser la barre d'event du jeu
        self.comet_event.update_bar(screen)

        # actualiser l'aniamtion du joueur
        self.player.update_animation()

        # recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # recuperer les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        # recuperer les cometes du jeu
        for comet in self.comet_event.all_comets:
            comet.fall()

        # appliquer l'ensemble des images du groupe de projectiles
        self.player.all_projectiles.draw(screen)

        # appliquer l'ensemble des images du groupe de monstres
        self.all_monsters.draw(screen)

        # appliquer l'ensemble des images du grp de cometes
        self.comet_event.all_comets.draw(screen)

        # verifier si le joueur souhaite aller a gauche ou a droite
        if self.pressed.get(pygame.K_d) and str(self.player.rect.x) + str(self.player.rect.width) < str(screen.get_width):
            self.player.move_right()
        elif self.pressed.get(pygame.K_q) and self.player.rect.x > 0:
            self.player.move_left()

    @staticmethod
    def check_collision(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster = Mummy(self)
        self.all_monsters.add(monster)
