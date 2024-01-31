# Tuplas de colores
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

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

# Estados del juego
estados_juego = {
    'MENU': 0,
    'GAME': 1,
    'GAME_OVER': 2,
    'WON': 3
}
