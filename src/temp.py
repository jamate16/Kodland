import pygame
import sys
import random

# Inicializa Pygame
pygame.init()

# Configura la ventana del juego
screen = pygame.display.set_mode((800, 600))

# Configura el título de la ventana
pygame.display.set_caption('Torres de defensa')

# Configura el reloj del juego
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Configuración del juego
config = {
    'salud_inicial': 20,
    'salud_torre': 5,
    'rango_spawn_enemigo': (50, 750),
    'rango_velocidad_enemigo': (1, 1.5),
    'intervalo_nueva_torre': 3000,
    'probabilidad_spawn_enemigo': 3,
    'duracion_juego': 30, # [s]: en segundos 
    'torres_iniciales': 5
}

# Clase para las torres
class Torre(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA) # Establece la superficie con canal alfa
        self.image.fill((255, 255, 255, 255)) # Establece el valor alfa inicial en 255 (totalmente opaco)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = config['salud_torre']

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            alpha = int(255 * (self.health / config['salud_torre'])) # Calcula el nuevo valor alfa basado en la salud
            self.image.fill((255, 255, 255, alpha)) # Actualiza el valor alfa de la imagen de la torre

# Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(center=(random.randint(*config['rango_spawn_enemigo']), 0))
        self.speed = random.uniform(*config['rango_velocidad_enemigo'])
        self.acaba_morir = False # Bandera para indicar que el enemigo acaba de morir para ser usado para actualizar la salud del jugador

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

def handle_collisions():
    colisiones = pygame.sprite.groupcollide(enemigos, torres, True, False)
    for colision in colisiones:
        torre = colisiones[colision][0]
        torre.hit()

# Clase para la salud del jugador
class Salud():
    def __init__(self):
        super().__init__()
        self.salud = config['salud_inicial']

    def decrease(self):
        self.salud -= 1

# Grupos de sprites
all_sprites = pygame.sprite.Group()
torres = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

def create_tower(x, y):
    """
    Crea una nueva torre en la posición (x, y) y la agrega a los grupos de sprites.

    Args:
        x (int): La coordenada x de la posición de la torre.
        y (int): La coordenada y de la posición de la torre.
    """
    new_torre = Torre(x, y)
    all_sprites.add(new_torre)
    torres.add(new_torre)

def generate_enemy():
    """
    Genera un nuevo enemigo con una probabilidad determinada y lo agrega al grupo de sprites.
    """
    if random.randint(0, 100) < config['probabilidad_spawn_enemigo']:
        enemigo = Enemigo()
        all_sprites.add(enemigo)
        enemigos.add(enemigo)

def draw_menu(titulo: str):
    """
    Dibuja el menú principal en la pantalla.

    Args:
        titulo (str): El título del menú.
    """
    font = pygame.font.Font(None, 48)
    menu_text = font.render(titulo, True, BLANCO)
    screen.blit(menu_text, (400 - menu_text.get_width() // 2, 100))
    font = pygame.font.Font(None, 36)
    start_text = font.render("Click para empezar", True, BLANCO)
    screen.blit(start_text, (400 - start_text.get_width() // 2, 200))
    info_text = font.render("Posiciona torres para defenderte. Si la salud llega a cero pierdes", True, BLANCO)
    screen.blit(info_text, (400 - info_text.get_width() // 2, 300))

def draw_game():
    """
    Dibuja la interfaz del juego en la pantalla.
    """
    font = pygame.font.Font(None, 36)
    remaining_time = max(0, config['duracion_juego'] - (current_time - tiempo_inicio) // 1000)
    time_text = font.render(f"Tiempo restante: {remaining_time} s", True, BLANCO)
    screen.blit(time_text, (10, 10))
    health_text = font.render(f"Salud: {salud.salud}/{config['salud_inicial']}", True, BLANCO)
    screen.blit(health_text, (10, 50))
    towers_text = font.render(f"Torres: {available_towers}", True, BLANCO)
    screen.blit(towers_text, (10, 90))

def update_screen():
    """
    Actualiza la pantalla del juego.
    """
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    if current_game_state == game_states['MENU']:
        draw_menu("Torres de defensa")
    elif current_game_state == game_states['GAME_OVER']:
        draw_menu("Game Over")
    elif current_game_state == game_states['WON']:
        draw_menu("Ganaste")
    elif current_game_state == game_states['GAME']:
        draw_game()

    pygame.display.flip()

# Crear una torre al inicio
torre = Torre(400, 500)
all_sprites.add(torre)
torres.add(torre)

# Variables para el control de las torres
available_towers = config['torres_iniciales']
tower_placement_timer = pygame.time.get_ticks()

# Variable para la salud del jugador
salud = Salud()

# Variable para el estado del juego
game_states = {
    'MENU': 0,
    'GAME': 1,
    'GAME_OVER': 2,
    'WON': 3
}
current_game_state = game_states['MENU']
tiempo_inicio = pygame.time.get_ticks()

# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_game_state == game_states['MENU']:
                if event.button == 1:
                    tiempo_inicio = pygame.time.get_ticks()
                    current_game_state = game_states['GAME']
            elif current_game_state == game_states['GAME']:
                if event.button == 1 and available_towers > 0:
                    mouse_pos = pygame.mouse.get_pos()
                    create_tower(mouse_pos[0], mouse_pos[1])
                    available_towers -= 1
            elif current_game_state == game_states['GAME_OVER'] or current_game_state == game_states['WON']:
                if event.button == 1:
                    current_game_state = game_states['MENU']
                    salud.salud = config['salud_inicial']
                    available_towers = config['torres_iniciales']
                    tower_placement_timer = pygame.time.get_ticks()
                    all_sprites.empty()
                    torres.empty()
                    enemigos.empty()
                    torre = Torre(400, 500)
                    all_sprites.add(torre)
                    torres.add(torre)

    # Lógica del juego
    current_time = pygame.time.get_ticks()
    if current_game_state == game_states['GAME']:
        all_sprites.update()
        for enemy in enemigos:
            if enemy.justo_acaba_morir():
                salud.decrease()

        generate_enemy()
        handle_collisions()
        if salud.salud <= 0:
            current_game_state = game_states['GAME_OVER']
        elif current_time - tiempo_inicio >= config['duracion_juego'] * 1000:
            current_game_state = game_states['WON']

    update_screen()

    # Incrementa available_towers cada 5 segundos
    current_time = pygame.time.get_ticks()
    if current_game_state == game_states['GAME'] and current_time - tower_placement_timer >= config['intervalo_nueva_torre']:
        available_towers += 1
        tower_placement_timer = current_time

    # Configura la velocidad de fotogramas
    clock.tick(60)