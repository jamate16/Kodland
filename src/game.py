import sys
import random

import pygame

from sprites import Torre, Enemigo, Salud
from constants import BLANCO, config, estados_juego

class Game:
    def __init__(self):
        # Inicializar ventana de Pygame y reloj
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Torres de defensa')
        self.clock = pygame.time.Clock()

        # Se generan los grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.torres = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()

        # Inicialización de estado del juego y variables temporales
        self.salud = Salud()
        self.available_towers = config['torres_iniciales']
        self.tower_placement_timer = pygame.time.get_ticks()
        self.current_game_state = estados_juego['MENU']
        self.tiempo_inicio = pygame.time.get_ticks()

        # Crear una torre al inicio
        self.create_tower(400, 500)

    def create_tower(self, x, y):
        new_torre = Torre(x, y)
        self.all_sprites.add(new_torre)
        self.torres.add(new_torre)

    def generate_enemy(self):
        """
        Genera un nuevo enemigo con una probabilidad determinada y lo agrega al grupo de sprites.
        """
        if random.randint(0, 100) < config['probabilidad_spawn_enemigo']:
            enemigo = Enemigo()
            self.all_sprites.add(enemigo)
            self.enemigos.add(enemigo)

    def handle_collisions(self):
        colisiones = pygame.sprite.groupcollide(self.enemigos, self.torres, True, False)
        for colision in colisiones:
            torre = colisiones[colision][0]
            torre.hit()

    def draw_menu(self, titulo: str):
        """
        Dibuja el menú principal en la pantalla.

        Args:
            titulo (str): El título del menú.
        """
        font = pygame.font.Font(None, 48)
        menu_text = font.render(titulo, True, BLANCO)
        self.screen.blit(menu_text, (400 - menu_text.get_width() // 2, 100))
        font = pygame.font.Font(None, 36)
        start_text = font.render("Click para empezar", True, BLANCO)
        self.screen.blit(start_text, (400 - start_text.get_width() // 2, 200))
        info_text = font.render("Posiciona torres para defenderte. Si la salud llega a cero pierdes", True, BLANCO)
        self.screen.blit(info_text, (400 - info_text.get_width() // 2, 300))

    def draw_game(self):
        """
        Dibuja la interfaz del juego en la pantalla.
        """

        # Establece la fuente para la información del juego
        fuente = pygame.font.Font(None, 36)
        
        # Calcula el tiempo restante
        tiempo_restante = max(0, config['duracion_juego'] - (pygame.time.get_ticks() - self.tiempo_inicio) // 1000)
        
        # Renderiza y muestra el texto del tiempo
        texto_tiempo = fuente.render(f"Tiempo restante: {tiempo_restante} s", True, BLANCO)
        self.screen.blit(texto_tiempo, (10, 10))
        
        # Renderiza y muestra el texto de la salud
        texto_salud = fuente.render(f"Salud: {self.salud.salud}/{config['salud_inicial']}", True, BLANCO)
        self.screen.blit(texto_salud, (10, 50))
        
        # Renderiza y muestra el texto de las torres disponibles
        texto_torres = fuente.render(f"Torres: {self.available_towers}", True, BLANCO)
        self.screen.blit(texto_torres, (10, 90))

    def update_screen(self):
        """
        Actualiza la pantalla del juego.
        """

        # Limpia la pantalla con color negro
        self.screen.fill((0, 0, 0))

        # Dibuja los sprites en la pantalla
        self.all_sprites.draw(self.screen)

        # Muestra la interfaz correspondiente al estado del juego
        if self.current_game_state == estados_juego['MENU']:
            self.draw_menu("Torres de defensa")
        elif self.current_game_state == estados_juego['GAME_OVER']:
            self.draw_menu("Game Over")
        elif self.current_game_state == estados_juego['WON']:
            self.draw_menu("Ganaste")
        elif self.current_game_state == estados_juego['GAME']:
            self.draw_game()

        # Actualiza la pantalla
        pygame.display.flip()

    def run(self):
        """
        Bucle principal del juego.
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_game_state == estados_juego['MENU']:
                        if evento.button == 1:
                            self.tiempo_inicio = pygame.time.get_ticks()
                            self.current_game_state = estados_juego['GAME']
                    elif self.current_game_state == estados_juego['GAME']:
                        if evento.button == 1 and self.available_towers > 0:
                            pos_mouse = pygame.mouse.get_pos()
                            self.create_tower(pos_mouse[0], pos_mouse[1])
                            self.available_towers -= 1
                    elif (
                        self.current_game_state == estados_juego['GAME_OVER']
                        or self.current_game_state == estados_juego['WON']
                    ):
                        if evento.button == 1:
                            self.current_game_state = estados_juego['MENU']
                            self.salud.salud = config['salud_inicial']
                            self.available_towers = config['torres_iniciales']
                            self.tower_placement_timer = pygame.time.get_ticks()
                            self.all_sprites.empty()
                            self.torres.empty()
                            self.enemigos.empty()
                            torre = Torre(400, 500)
                            self.all_sprites.add(torre)
                            self.torres.add(torre)

            # Lógica del juego
            tiempo_actual = pygame.time.get_ticks()
            if self.current_game_state == estados_juego['GAME']:
                self.all_sprites.update()
                for enemigo in self.enemigos:
                    if enemigo.justo_acaba_morir():
                        self.salud.decrease()

                self.generate_enemy()
                self.handle_collisions()
                if self.salud.salud <= 0:
                    self.current_game_state = estados_juego['GAME_OVER']
                elif tiempo_actual - self.tiempo_inicio >= config['duracion_juego'] * 1000:
                    self.current_game_state = estados_juego['WON']

            self.update_screen()

            # Incrementa available_towers cada 5 segundos
            tiempo_actual = pygame.time.get_ticks()
            if (
                self.current_game_state == estados_juego['GAME']
                and tiempo_actual - self.tower_placement_timer >= config['intervalo_nueva_torre']
            ):
                self.available_towers += 1
                self.tower_placement_timer = tiempo_actual

            # Configura la velocidad de fotogramas
            self.clock.tick(60)