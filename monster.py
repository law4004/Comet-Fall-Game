import pygame
import random
import animation


# creer une classe qui va gerer la notion de monstre sur le jeu
class Monster(animation.AnimateSprite):

    def __init__(self, game, name):
        super().__init__(name)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.2
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540
        self.loot_amount = 10
        self.velocity = 1
        self.start_animation()

    def damage(self, amount):
        # infliger les degats
        self.health -= amount

        # verifier si son new nombre de hp est < ou = a 0
        if self.health <= 0:
            # reapparaitre comme un new monstre
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, 2)
            self.health = self.max_health
            # ajouter le nb de points
            self.game.add_score(self.loot_amount)

            # si la barre d'event est chargee au max
            if self.game.comet_event.is_full_loaded():
                # retirer du jeu
                self.game.all_monsters.remove(self)

                # appel de la methode pour essayer de declencher la pluie de cometes
                self.game.comet_event.attempt_fall()

    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):
        # dessiner la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 20, self.health, 5])

    def forward(self):
        # le deplacement ne se fait que si il n'y a pas de collision avec un groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        # si le monstre est en collision avec le joueur
        else:
            # infliger des degats (au joueur)
            self.game.player.damage(self.attack)

# definir une classe pour la momie
class Mummy(Monster):

    def __init__(self, game):
        super().__init__(game, "mummy")
