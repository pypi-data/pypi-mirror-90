from multiprocessing import Queue
import threading
from typing import List, Tuple, Type, Union

from fredo.conf import PLUGINS, DEFAULT_CALCULATOR, DEFAULT_PLUGIN
from fredo.fredo_types.item import Item
from fredo.plugins.base import Plugin


class Fredo:

    def __init__(self, g):
        self.gui = g
        self.plugins = PLUGINS
        self.calculator = DEFAULT_CALCULATOR
        self.default_plugin = DEFAULT_PLUGIN
        self.current_plugin = None
        self.command = ''
        self.q = Queue()
        self.t = threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        v = None
        while True:
            value = self.q.get()
            if v is not value:
                self.callback(value)
                v = value

    def get_options(self, query: str) -> List[Item]:
        """From a given query, return a list of options"""
        pass

    def parse_query(self, query: str) -> Tuple[Union[Type[Plugin], None], str]:
        """From a given query, return a tuple with the plugin
        and the actual query"""
        if not isinstance(query, str):
            raise TypeError(f"Only strings are allowed. Got {query}")
        query = query.lstrip()
        # If query is a math expression, send It to the calc plugin
        try:
            eval(query)
            return self.calculator, query
        except (SyntaxError, NameError):
            if ' ' in query:
                prefix = query.split(' ', 1)[0]
                suffix = query.split(' ', 1)[1]
                if prefix in self.plugins:
                    return self._get_plugin(prefix), suffix
        return self.default_plugin, query

    def parse_input(self, query):
        # If query is a math expression, send It to the calc plugin
        plugin, query = self.parse_query(query)
        self.setup_plugin(plugin, query)

    def setup_plugin(self, plugin, query):
        if self.current_plugin:
            self.current_plugin.kill()
        self.current_plugin = plugin(fredo=self, query=query, q=self.q)
        self.command = query
        self.set_mode_label(self.current_plugin.label)

    def callback(self, options):
        self.refresh_options(options)

    def _get_plugin(self, prefix):
        """Returns the plugin associated with a prefix"""
        return self.plugins.get(prefix, None)

    def refresh_options(self, options):
        self.gui.refresh_options(options)

    def action(self, command):
        self.current_plugin.action(command)

    def set_mode_label(self, new_label):
        self.gui.set_mode_label(new_label)
