"""
Main menu for pawnshop
"""
import pygame
import pygame_gui
import debug.debug as DB
import math

DB.DEBUG_LEVEL = 2

################################
# Functions to build menu items
################################

def mk_label(name):
    return (None, pygame_gui.elements.UILabel,
            [],
            dict(text=name))

def mk_button(name, action):
    return (None, pygame_gui.elements.UIButton,
            [(pygame_gui.UI_BUTTON_PRESSED,
              action)],
            dict(text=name))

def mk_drop_down(label, action, list, default):
    return (label, pygame_gui.elements.UIDropDownMenu,
            [(pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
              action)],
            {'options_list' : list,
             'starting_option' : default}
            )

class MenuHandler():
    """
    Object that will contain the menu manager and produce menus
    """
    def __init__(self, dimensions, window_surface):
        self.manager = pygame_gui.UIManager(dimensions)
        self.item_handlers   = {} # ^ Keep track of the menu items and
                                  # handler functions. This a
                                  # dictionary of dictionaries,
                                  # mapping, event types to elements,
                                  # to handlers.
        self.clock = clock = pygame.time.Clock()
        self.window_surface = window_surface
        self.enabled = True
        self.dimensions = dimensions
        self.item_width = 150 * 2 # includes label
        self.item_height = 40
        self.available_height = self.dimensions[1]-2*self.item_height
        self.available_width  = self.dimensions[0]-self.item_width
        
        
    def create_menu(self, menu_items, theme = None):
        """
        Every menu item must contain
        0. Label : Optional(string)
        1. The generating function (e.g. pygame_gui.elements.UIButton)
        2. list of Pairs of event type and Handler function
        3. The arguments (kwarg) as a dictionary
        """
        # First calculate how many columns we need:
        total_menu_height = self.item_height * len(menu_items)
        columns = math.ceil(total_menu_height / self.available_height)
        items_per_column = math.ceil(len(menu_items) /columns) # Round up
        x_offset = self.available_width // columns
        DB.debug(2, "total_menu_height", total_menu_height, " self.available_width ", self.available_width)
        DB.debug(2, "Menu needs", columns, " columns with ", items_per_column, "items per column")
        
        items = 0
        for (label, item_gen, handlers, kwargs) in menu_items:
            #Create coordinates
            (column, row) = (items // items_per_column, items % items_per_column)
            print("column", column, "/ x_offset", x_offset, "/ self.item_width", self.item_width)
            x = column * x_offset + (x_offset // 2) 
            y = (row + 1) * self.item_height + self.item_height // 2
            width = self.item_width
            # create rectangles
            if label:
                #If there is a label shift right by half the size
                lbl_x = x
                x     = x + self.item_width//2
                width = width //2
                
            # Create the rectangles
            rectangle = pygame.Rect((x, y), (width,
                                             self.item_height))
            my_item  = item_gen(manager = self.manager,
                               relative_rect=rectangle, **kwargs)
            if label:
                lbl_rectangle = pygame.Rect((lbl_x, y),
                                            (width,
                                             self.item_height))
                my_label = pygame_gui.elements.UILabel(text=label, manager
                                                       = self.manager,
                                                       relative_rect=lbl_rectangle)
            for (event_type, handler) in handlers:
                if not event_type in self.item_handlers:
                    self.item_handlers[event_type] = {}
                self.item_handlers[event_type][my_item] = handler
            items = items + 1

            
        DB.debug(2, "Created a menue with", items, "items")

    def event_check(self, event):
        """
        Checks events, updates time and draws menu 
        """

        # Check the value-less events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.type in self.item_handlers and event.ui_element in self.item_handlers[event.type]:
                handler = self.item_handlers[event.type][event.ui_element]
                handler()
        # Check the events that have text values
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.type in self.item_handlers and event.ui_element in self.item_handlers[event.type]:
                handler = self.item_handlers[event.type][event.ui_element]
                handler(event.text)
        # Check the events that have text values
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.type in self.item_handlers and event.ui_element in self.item_handlers[event.type]:
                handler = self.item_handlers[event.type][event.ui_element]
                handler(event.value)

        # Always update the manager.
        self.manager.process_events(event)
        
    def frame_step(self, time_delta, events = []):
        if self.enabled:
            for event in events:
                self.event_check(event)
        self.manager.update(time_delta)

    def draw_ui(self):
        if self.enabled:
            self.manager.draw_ui(self.window_surface)

    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False
