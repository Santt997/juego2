import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Recolección")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Cargar imágenes
player_image = pygame.Surface((50, 50))
player_image.fill(GREEN)

item_image = pygame.Surface((30, 30))
item_image.fill(RED)

# Clase del jugador
class Player:
    def __init__(self):
        self.rect = player_image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limitar movimiento dentro de la pantalla
        self.rect.clamp_ip(screen.get_rect())

    def draw(self):
        screen.blit(player_image, self.rect)

# Clase del objeto a recoger
class Item:
    def __init__(self):
        self.rect = item_image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def draw(self):
        screen.blit(item_image, self.rect)

# Función principal del juego
def main():
    clock = pygame.time.Clock()
    player = Player()
    items = [Item() for _ in range(5)]
    score = 0
    start_ticks = pygame.time.get_ticks()  # Tiempo inicial

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mover al jugador
        player.move()

        # Comprobar colisiones con los objetos
        for item in items[:]:
            if player.rect.colliderect(item.rect):
                items.remove(item)
                score += 1
                print(f"Puntuación: {score}")
                items.append(Item())  # Añadir un nuevo ítem al recoger uno

        # Calcular el tiempo transcurrido
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Convertir a segundos

        # Si el tiempo se ha agotado
        if seconds >= 60:
            mostrar_mensaje("¡Tiempo agotado!", f"Puntuación final: {score}")
            if not preguntar_reinicio():
                break
            else:
                main()  # Reiniciar el juego

        # Dibujar todo en la pantalla
        screen.fill(WHITE)
        player.draw()
        
        for item in items:
            item.draw()

        # Mostrar el temporizador y la puntuación en la pantalla
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Tiempo: {60 - int(seconds)}", True, BLACK)
        score_text = font.render(f"Puntuación: {score}", True, BLACK)
        
        screen.blit(timer_text, (10, 10))
        screen.blit(score_text, (10, 50))

        # Actualizar la pantalla
        pygame.display.flip()
        
        # Controlar la velocidad del juego
        clock.tick(60)

def mostrar_mensaje(titulo, mensaje):
    font = pygame.font.Font(None, 54)
    title_surface = font.render(titulo, True, BLACK)
    message_surface = font.render(mensaje, True, BLACK)

    screen.fill(WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 + 30))
    
    pygame.display.flip()
    
    # Esperar un momento para que el jugador vea el mensaje
    pygame.time.delay(2000)

def preguntar_reinicio():
    font = pygame.font.Font(None, 36)
    pregunta_surface = font.render("¿Deseas volver a jugar? (s/n)", True, BLACK)

    screen.fill(WHITE)
    screen.blit(pregunta_surface, (WIDTH // 2 - pregunta_surface.get_width() // 2, HEIGHT // 2))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:   # Si presiona 's', reinicia el juego
                    return True
                elif event.key == pygame.K_n: # Si presiona 'n', sale del juego
                    return False

if __name__ == "__main__":
    main()
