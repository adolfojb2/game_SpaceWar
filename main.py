from game_objects import *

def game_loop(game,screen):
    global game_over
    game_over = False
    while not game_over:
        #Eventos del juego
        game.state = game.process_events() 
        # run_logic
        game_over = game.run_logic()
        #dibujado del juego
        game.display_frame(screen)
        game.clock.tick(60)  #FPS
        if game.state == "menu":
            break

def main():
    # Crear objeto game
    game = Game()
    running = True
    # Bucle principal (menu)
    while running:
        if game.state == "menu":
            # Procesar eventos para el menú
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        game.selected_option = (game.selected_option + 1) % len(game.menu_options)
                    elif event.key == pygame.K_UP:
                        game.selected_option = (game.selected_option - 1) % len(game.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if game.selected_option == 0:  # Iniciar juego
                            game.state = "game"
                        elif game.selected_option == 1:  # Salir
                            running = False
            # Dibujar el menú
            game.draw_menu(game.screen)
            pygame.display.flip()
            game.clock.tick(60)
        elif game.state == "game":
            game_loop(game,game.screen)
        
    pygame.quit()
    sys.exit()
#Ejecutar la función principal (main)
if __name__=="__main__":
    main()





  
    