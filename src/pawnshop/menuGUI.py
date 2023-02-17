import pygame
import pygame_gui
import menu
import module.all_modules as modules
import virtual_board as VB
import sys

pygame.init()
pygame.display.set_caption('PawnShop')

menu_active = True
THE_MODULE = modules.default_module

# Global instances
chess_board = VB.VBoard()
dimensions = chess_board.dimensions
window_surface = pygame.display.set_mode(dimensions)

main_menu_handler = menu.MenuHandler(dimensions, window_surface)
config_menu_handler = menu.MenuHandler(dimensions, window_surface)



background = pygame.Surface(dimensions)
background.fill(pygame.Color('#000000'))


# Play button
def play_button_function(module_instance):
    global main_menu_handler
    global config_menu_handler
    global chess_board
    global is_running
    
    print("We are playing with:", module_instance.get_name())
    config_menu_handler.disable()
    module_instance.update_config()
    chess_board.enable()
    
    
def mk_play_button_item(module_instance):
    play_button_item = menu.mk_button('Play', lambda: play_button_function(module_instance))
    return play_button_item
    
# Next button
def next_button_function():
    global main_menu_handler
    global config_menu_handler
    global chess_board
    global THE_MODULE
    
    print ("We shall play:" , THE_MODULE)
    main_menu_handler.disable()
    
    # Create the configuration menue
    module_instance = modules.available_modules[THE_MODULE]()
    config_menu_items = module_instance.get_config_menu()
    chess_board.module = module_instance
    play_button_item = mk_play_button_item(module_instance)
    
    config_menu_items = config_menu_items + [play_button_item, back_button_item]
    config_menu_handler.create_menu(config_menu_items)
    config_menu_handler.enable()
    
    
next_button_item = menu.mk_button('Next', next_button_function)

# Goodbye button
def exit_button_function():
    global main_menu_handler
    global is_running
    
    print ("We'll exit!")
    main_menu_handler.disable()
    is_running = False
    
exit_button_item = menu.mk_button('Exit', exit_button_function) 


# Back button
def back_button_function():
    global main_menu_handler
    global config_menu_handler
    global is_running
    
    print ("We'r going back!")
    main_menu_handler.enable()
    config_menu_handler.disable()
    
back_button_item = menu.mk_button('Back', back_button_function)

# Modules
def choose_module_function(event_text):
    global THE_MODULE
    
    print("New Choice ", event_text)
    THE_MODULE = event_text

choose_modules = menu.mk_drop_down('Choose module', choose_module_function,
                              modules.available_modules_names, modules.default_module)

main_menu_items = [choose_modules, next_button_item, exit_button_item]
main_menu_handler.create_menu(main_menu_items)

clock = pygame.time.Clock()
is_running = True
def done ():
    chess_board.on_board_exit()
    pygame.display.quit()
    pygame.quit()
    exit()

i = 0
try:
    while is_running:
        time_delta = clock.tick(60)/1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                is_running = False
                done()
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu_handler.enable()
        
        # Step in the menus (they only act if enabled)
        main_menu_handler.frame_step(time_delta, events=events)
        config_menu_handler.frame_step(time_delta, events=events)
        chess_board.frame_step(events)
        
        
        window_surface.blit(background, (0, 0))
        main_menu_handler.draw_ui()
        config_menu_handler.draw_ui()
        chess_board.draw_board()
        chess_board.rest()
            
        
        if not (main_menu_handler.enabled or config_menu_handler.enabled or chess_board.enabled):
            background.fill(pygame.Color('#000000'))
    
        pygame.display.update()
except Exception as e:
    print("Exception:", e)
    
        
done()
