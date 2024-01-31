import pygame
import random
from constants import config, ROJO

class Torre(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # Establece la superficie con canal alfa
        self.image.fill((255, 255, 255, 255))  # Establece el valor alfa inicial en 255 (totalmente opaco)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = config['salud_torre']

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            alpha = int(255 * (self.health / config['salud_torre']))  # Calcula el nuevo valor alfa basado en la salud
            self.image.fill((255, 255, 255, alpha))  # Actualiza el valor alfa de la imagen de la torre

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(center=(random.randint(*config['rango_spawn_enemigo']), 0))
        self.speed = random.uniform(*config['rango_velocidad_enemigo'])
        self.acaba_morir = False  # Bandera para indicar que el enemigo acaba de morir para ser usado para actualizar la salud del jugador

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600:
            self.rect.y = 0
            self.rect.x = random.randint(*config['rango_spawn_enemigo'])
            self.acaba_morir = True

    def justo_acaba_morir(self):
        acaba_morir = self.acaba_morir
        self.acaba_morir = False
        return acaba_morir

class Salud:
    def __init__(self):
        super().__init__()
        self.salud = config['salud_inicial']

    def decrease(self):
        self.salud -= 1
