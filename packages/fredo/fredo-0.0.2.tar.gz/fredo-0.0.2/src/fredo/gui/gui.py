from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from fredo.core import Fredo

Window.size = (800, 350)


class SingleOption(TwoLineListItem):
    def __init__(self, command='nocommand', **kwargs):
        super(SingleOption, self).__init__(**kwargs)
        self.command = command
        self.selected = False
        self.bind(on_press=self.get_command)

    def select(self):
        self.selected = True
        self.bg_color = (.5, .5, .5, 0.1)

    def deselect(self):
        self.selected = False
        self.bg_color = []

    def get_command(self, instance):
        return self.command


class RootLayout(GridLayout):
    def __init__(self, fredo, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2

        self.fredo = fredo

        # Text Input
        self.textinput = TextInput(
            text='', multiline=False, size_hint_y=None,
            height=60,
            padding=[12, 12, 12, 12],
            font_size=25
        )
        self.textinput.write_tab = False
        self.textinput.bind(text=self.on_text)
        self.add_widget(self.textinput)

        # Options
        self.options_box = OptionsBox()
        self.add_widget(self.options_box)

    def on_text(self, instance, value):
        self.fredo.parse_input(value)


class OptionsBox(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.list = MDList()
        self.add_widget(self.list)

    @property
    def selected_option(self):
        for option in self.list.children:
            if option.selected:
                return option
        else:
            return None

    @property
    def selected_option_index(self):
        for i, option in enumerate(self.list.children):
            if option.selected:
                return i
        else:
            return None

    def select_next(self):
        try:
            self.select_option(self.selected_option_index - 1)
        except Exception:
            self.select_option(0)

    def select_previous(self):
        try:
            self.select_option(self.selected_option_index + 1)
        except Exception:
            self.select_option(0)

    def select_option(self, index):
        if len(self.list.children) + 1 < index:
            return
        [option.deselect() for option in self.list.children if option.selected]
        self.list.children[index].select()

    def refresh_options(self, items):
        self.remove_items()
        self.add_items(items)
        if len(items):
            self.select_option(len(items)-1)

    def add_items(self, items):
        for idx, item in enumerate(items):
            i = SingleOption(
                    text=item['title'],
                    secondary_text=item.get('subtitle', ''),
                    command=item.get('command', None)
                )
            self.list.add_widget(i)

    def remove_items(self):
        self.list.clear_widgets()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.fredo = Fredo(self)
        self.screen = RootLayout(self.fredo)
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)
        Clock.schedule_once(self.show_keyboard)
        Clock.schedule_once(self.show_window)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode in (43, 81):
            # TAB OR DOWN
            self.screen.options_box.select_next()
        elif keycode == 82:
            # UP
            self.screen.options_box.select_previous()
        elif keycode == 40:
            # ENTER
            self.action()

    def _on_keyboard_up(self, instance, keyboard, keycode):
        if keyboard == 27:
            # ESC
            self.stop()

    def refresh_options(self, options):
        self.screen.options_box.refresh_options(options)

    def action(self):
        command = self.screen.options_box.selected_option.command
        self.fredo.action(command)
        self.stop()

    def set_mode_label(self, new_label):
        pass

    def show_keyboard(self, event):
        self.screen.textinput.focus = True

    def show_window(self, _):
        self.root_window.show()

    def build(self):
        self.title = 'Hello world'
        return self.screen

    def get_application_name(self):
        """Setting name of window so that I can force floating in any Window Manager"""
        return '__fredo__'
