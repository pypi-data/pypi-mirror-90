from fredo.plugins.base import Plugin
from fredo.plugins.utils import copy_to_clipboard


class Calculator(Plugin):

    label = "Calculate"

    def get_options(self, query):
        option = {'subtitle': 'Copy to clipboard'}
        try:
            option['command'] = eval(query)
            option['title'] = f"{query} = {option['command']}"
        except (SyntaxError, NameError):
            option['command'] = query
            option['title'] = query
        return [option]

    def action(self, command):
        copy_to_clipboard(command)
