import pygame
import pygame_gui
import menu
import module.all_modules as modules
import virtual_board as VB

pygame.init()
dimensions = (800, 600)

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(dimensions)

background = pygame.Surface(dimensions)
background.fill(pygame.Color('#000000'))

menu_active = True
THE_MODULE = modules.default_module

# Global instances
main_menu_handler = menu.MenuHandler(dimensions, window_surface)
config_menu_handler = menu.MenuHandler(dimensions, window_surface)
chess_board = VB.VBoard()
    

# Play button
def play_button_function(module_instance):
    global main_menu_handler
    global config_menu_handler
    global chess_board
    global is_running
    
    print ("We'll PLAY!")
    print("We are playing wiht:", module_instance.get_name())
    config_menu_handler.disable()
    chess_board.enable()
    
    
def mk_play_button_item(module_instance):
    play_button_item = (pygame_gui.elements.UIButton,
                        [(pygame_gui.UI_BUTTON_PRESSED,
                          lambda: play_button_function(module_instance))],
                        dict(text='Play') )
    return play_button_item

# Next button
def next_button_function():
    global main_menu_handler
    global config_menu_handler
    global chess_board
    global THE_MODULE
    
    print ("Let's next a game! Module:" , THE_MODULE)
    main_menu_handler.disable()
    
    # Create the configuration menue
    module_instance = modules.available_modules[THE_MODULE]()
    config_menu_items = module_instance.config_menu
    chess_board.module = module_instance
    play_button_item = mk_play_button_item(module_instance)
    
    config_menu_items = config_menu_items + [play_button_item, back_button_item]
    config_menu_handler.create_menu(config_menu_items)
    config_menu_handler.enable()
    
    
next_button_item = (pygame_gui.elements.UIButton,
                     [(pygame_gui.UI_BUTTON_PRESSED,
                       next_button_function)],
                     dict(text='Next') )

# Goodbye button
def exit_button_function():
    global main_menu_handler
    global is_running
    
    print ("We'll exit!")
    main_menu_handler.disable()
    is_running = False
    
exit_button_item = (pygame_gui.elements.UIButton,
                   [(pygame_gui.UI_BUTTON_PRESSED,
                    exit_button_function)],
                   dict(text='Exit') )


# Back button
def back_button_function():
    global main_menu_handler
    global config_menu_handler
    global is_running
    
    print ("We'r going back!")
    main_menu_handler.enable()
    config_menu_handler.disable()
    
back_button_item = (pygame_gui.elements.UIButton,
                   [(pygame_gui.UI_BUTTON_PRESSED,
                    back_button_function)],
                   dict(text='Back') )

# Modules
def choose_module_function(event_text):
    global THE_MODULE
    
    print ("Expanded!")
    print("New Choice ", event_text)
    THE_MODULE = event_text

choose_modules = (pygame_gui.elements.UIDropDownMenu,
              [(pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
                choose_module_function)],
              {'options_list' : modules.available_modules_names,
               'starting_option' : modules.default_module}
              )

main_menu_items = [choose_modules, next_button_item, exit_button_item]
main_menu_handler.create_menu(main_menu_items)

clock = pygame.time.Clock()
is_running = True
def done ():
    pygame.display.quit()
    pygame.quit()

i = 0
while is_running:
    time_delta = clock.tick(60)/1000.0
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            is_running = False
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

done()
