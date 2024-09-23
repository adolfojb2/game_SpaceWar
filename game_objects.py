import pygame , sys, random

# Constantes
BLACK = (0,0,0)
GRAY = (100, 100, 100)
WHITE = (255,255,255)
YELLOW = (255, 255, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("meteor.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #sirve para posicionar el sprite
    
    def update(self):
        self.rect.y += 5  # velocidad de los meteoros
        if self.rect.y > 600:
            self.rect.y = -10
            self.rect.x = random.randrange(800)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #sirve para posicionar el sprite
        self.speed_x = 0
        self.speed_y = 0
    def changespeed(self,x):
        self.speed_x += x

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y = 510

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #sirve para posicionar el sprite
    def update(self):
        self.rect.y -= 5

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #sirve para posicionar el sprite
    
    def update(self):
        self.rect.y += 5  # velocidad de los aliens
        if self.rect.y > 600:
            self.rect.y = -10
            self.rect.x = random.randrange(800)

class Game(object):
    def __init__(self):
        # Iniciar pygame
        pygame.init()
        # Crear el objeto screen
        size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Space War')
        #configurar reloj
        self.clock = pygame.time.Clock()
        self.game_over = False
        # Creación de variables y listas
        self.score = 0
        self.cant_meteor = 30
        self.cant_alien = 7
        # Estados del juego
        self.state = "menu"  # Comenzamos en el menú
        self.game_over = False
        # Opciones del menú
        self.menu_options = ["Iniciar Juego", "Salir"]
        self.selected_option = 0
        # Configura la fuente del menu
        self.font = pygame.font.Font(None, 76)
        #listas
        self.meteor_list = pygame.sprite.Group()
        self.alien_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        self.background = pygame.image.load("space.jpg").convert() 
        self.sound = pygame.mixer.Sound("laser5.ogg")
        self.start_ticks = pygame.time.get_ticks() #tiempo de inicio del cronometro
        # Ocultar puntero del mouse
        pygame.mouse.set_visible(0)
        # Generar las coordenadas de los meteoros y guardarlas en listas
        for i in range(self.cant_meteor):
            self.meteor = Meteor()
            self.meteor.rect.x = random.randrange(750)
            self.meteor.rect.y = random.randrange(550)

            self.meteor_list.add(self.meteor)
            self.all_sprites_list.add(self.meteor)
        # Generar las coordenadas de los aliens y guardarlas en listas
        for i in range(self.cant_alien):
            self.alien = Alien()
            self.alien.rect.x = random.randrange(750)
            self.alien.rect.y = random.randrange(550)

            self.alien_list.add(self.alien)
            self.all_sprites_list.add(self.alien)
        # Se crea el objeto Jugador y agragarlo a la lista de sprites
        self.player = Player()
        self.all_sprites_list.add(self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(-3)
                if event.key == pygame.K_RIGHT:
                    self.player.changespeed(3)
                if event.key == pygame.K_SPACE:
                    self.laser = Laser()
                    self.laser.rect.x = self.player.rect.x + 45
                    self.laser.rect.y = self.player.rect.y - 20
                    self.all_sprites_list.add(self.laser)
                    self.laser_list.add(self.laser)
                    self.sound.play()
                if event.key == pygame.K_r:
                    if self.game_over:
                        self.__init__() #reinicia el juego
                        self.state = "game"
                if event.key == pygame.K_m:
                    if self.game_over:
                        self.state = "menu"
                        self.__init__() #reinicia el juego
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(3)
                if event.key == pygame.K_RIGHT:
                    self.player.changespeed(-3)
        return self.state
    
    def run_logic(self):
        if not self.game_over:
            self.all_sprites_list.update()
            #colisiones player_alien
            player_hit_list = pygame.sprite.spritecollide(self.player,self.alien_list, True)
            if len(player_hit_list) > 0:
                self.game_over = True
                self.start_ticks = pygame.time.get_ticks() # tiempo hasta el game over
            for laser in self.laser_list:
                #colisiones laser_meteoro
                meteor_hit_list = pygame.sprite.spritecollide(laser,self.meteor_list, True)
                #colisiones laser_alien
                alien_hit_list = pygame.sprite.spritecollide(laser,self.alien_list, True)
                for meteor in meteor_hit_list: # eliminar laser cuando colisiona con meteoro
                    self.all_sprites_list.remove(laser)
                    self.laser_list.remove(laser)
                    self.score += 1 #puntaje por eliminar meteoro
                for alien in alien_hit_list: # eliminar laser cuando colisiona con alien
                    self.all_sprites_list.remove(laser)
                    self.laser_list.remove(laser)
                    self.score += 3 #puntaje por eliminar alien
                if laser.rect.y < -10: # condición para eliminar laser que sale de la pantalla
                    self.all_sprites_list.remove(laser)
                    self.laser_list.remove(laser)
            if len(self.meteor_list)== 0: #Condición para pasar a Game over
                self.game_over = True
                self.start_ticks = pygame.time.get_ticks() # tiempo hasta el game over
        return self.game_over

    def display_frame(self,screen):
        #imagen de fondo 
        screen.blit(self.background, [0,0])
        if self.game_over:
            font = pygame.font.SysFont("serif", 35) # Fuente
            text = font.render("Game Over, press R to restart o M to menu",True, WHITE) #Texto
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2) # Posición texto
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2) # Posición texto
            screen.blit(text,[center_x,center_y]) # Ponerlo en pantalla
            # Mostrar Score
            text = font.render(f"Score: {self.score}",True, WHITE) #Texto
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2) # Posición texto
            center_y = (SCREEN_HEIGHT // 2) + (text.get_height()) # Posición texto
            screen.blit(text,[center_x,center_y]) # Ponerlo en pantalla
            # Mostrar tiempo
            text = font.render(f"Time: {self.timer_text}",True, WHITE) #Texto
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2) # Posición texto
            center_y = (SCREEN_HEIGHT // 2) + (text.get_height()*2) # Posición texto
            screen.blit(text,[center_x,center_y]) # Ponerlo en pantalla

        if not self.game_over:
            self.all_sprites_list.draw(screen)
            # Score
            font = pygame.font.SysFont("serif", 20) # Fuente
            text = font.render(f"Score: {self.score}",True, WHITE) #Texto
            center_x = 150 # Posición texto
            center_y = 10 # Posición texto
            screen.blit(text,[center_x,center_y]) # Ponerlo en pantalla
            
            # Calcula el tiempo transcurrido
            total_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000  # Convierte a segundos
            minutes = total_seconds // 60  # Calcula los minutos
            seconds = total_seconds % 60   # Calcula los segundos restantes

            # Formatea el tiempo en MM:SS
            self.timer_text = f"{minutes:02}:{seconds:02}"
            text = font.render(f"Time: {self.timer_text}",True, WHITE) #Texto
            center_x = 20 # Posición texto
            center_y = 10 # Posición texto
            screen.blit(text,[center_x,center_y]) #Ponerlo en pantalla

        pygame.display.flip()
    
    def draw_menu(self,screen):
        #screen.fill(BLACK)
        self.bg_menu = pygame.image.load("bg_menu.jpg").convert() 
        screen.blit(self.bg_menu, [0,0])
        for index, option in enumerate(self.menu_options):
            if index == self.selected_option:
                text_surface = self.font.render(option, True, YELLOW)  # Opción seleccionada
            else:
                text_surface = self.font.render(option, True, (150, 150, 150))  # Opción no seleccionada
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 200 + index * 100))