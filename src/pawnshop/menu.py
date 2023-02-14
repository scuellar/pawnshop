"""
Main menu for pawnshop
"""
import pygame
import pygame_gui
import debug.debug as DB
import math

DB.DEBUG_LEVEL = 2

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
        self.item_width = 150
        self.item_height = 50
        self.available_height = self.dimensions[1]-2*self.item_height
        self.available_width  = self.dimensions[0]-2*self.item_width
        
        
    def create_menu(self, menu_items, theme = None):
        """
        Every menu item must contain
        1. The generating function (e.g. pygame_gui.elements.UIButton)
        2. list of Pairs of event type and Handler function
        3. The arguments (kwarg) as a dictionary
        """
        # First calculate how many columns we need:
        total_menu_height = self.item_height * len(menu_items)
        print("total_menu_height", total_menu_height)
        print("self.available_height", self.available_height)
        columns = math.ceil(total_menu_height / self.available_height)
        items_per_column = math.ceil(len(menu_items) /columns) # Round up
        DB.debug(2, "Menu needs", columns, " columns with ", items_per_column, "items per column")
        
        items = 0
        for (item_gen, handlers, kwargs) in menu_items:
            #Create coordinates
            (column, row) = (items // items_per_column, items % items_per_column)
            x_offset = self.available_width // columns
            x = column * x_offset + (x_offset // 2) + self.item_width // 2
            y = (row + 1) * self.item_height + self.item_height // 2
            # Create the rectangle
            rectangle = pygame.Rect((x, y), (self.item_width,
                                             self.item_height))
            
            my_item = item_gen(manager = self.manager,
                               relative_rect=rectangle, **kwargs)
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
