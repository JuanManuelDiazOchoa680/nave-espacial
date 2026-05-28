import os
import sys
import pygame

pygame.init()
try:
    pygame.mixer.init()
    mixer_ok = True
except Exception:
    mixer_ok = False

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave atari")

azul_espacio = (2, 6, 23)  # Azul muy oscuro, parecido al espacio (R,G,B)

# Intentamos cargar `boton_play.png` desde la misma carpeta que este archivo.
script_dir = os.path.dirname(__file__)
play_image_path = os.path.join(script_dir, "assets/images/boton_play.png")
button_img = None
if os.path.exists(play_image_path):
    try:
        button_img = pygame.image.load(play_image_path).convert_alpha()
    except Exception as e:
        print("No se pudo cargar play.png:", e)

# Rect del botón (si no hay imagen, dibujamos un rectángulo)
if button_img:
    button_rect = button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
else:
    BUTTON_SIZE = (100, 100)
    button_rect = pygame.Rect((WIDTH // 2 - BUTTON_SIZE[0] // 2, HEIGHT // 2 - BUTTON_SIZE[1] // 2), BUTTON_SIZE)

# Intentamos cargar un efecto de sonido opcional
sound = None
if mixer_ok:
    for fname in ("assets/sounds/sonido_boton_play.wav"):
        path = os.path.join(script_dir, fname)
        if os.path.exists(path):
            try:
                sound = pygame.mixer.Sound(path)
                break
            except Exception as e:
                print("Error cargando sonido:", e)

# Animación: al hacer click el botón se moverá hacia `target_y` a `speed` px/frame
moving = False
# Mover el botón fuera de la pantalla (por debajo): se calcula en base
# a la altura del botón para asegurar que quede totalmente fuera.
target_y = HEIGHT + (button_rect.height if hasattr(button_rect, 'height') else 120) + 20
speed = 10  # ajuste: píxeles por frame (ajústalo a tu gusto)

clock = pygame.time.Clock()

running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if button_rect.collidepoint(evento.pos) and not moving:
                moving = True
                if sound:
                    sound.play()

    if moving:
        if button_rect.y < target_y:
            button_rect.y += speed
            if button_rect.y > target_y:
                button_rect.y = target_y
        else:
            moving = False

    screen.fill(azul_espacio)

    if button_img:
        screen.blit(button_img, button_rect)
    else:
        pygame.draw.rect(screen, (200, 200, 200), button_rect, border_radius=12)
        # Dibujar un triángulo "play" encima
        tri_center = button_rect.center
        tri_size = min(button_rect.width, button_rect.height) * 0.5
        tri = [
            (tri_center[0] - tri_size / 4, tri_center[1] - tri_size / 2),
            (tri_center[0] - tri_size / 4, tri_center[1] + tri_size / 2),
            (tri_center[0] + tri_size / 2, tri_center[1]),
        ]
        pygame.draw.polygon(screen, (20, 20, 20), tri)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()