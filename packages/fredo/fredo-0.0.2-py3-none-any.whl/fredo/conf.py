from fredo.plugins.apps import Apps
from fredo.plugins.calculator import Calculator
from fredo.plugins.files import Files
from fredo.plugins.search import GoogleSearch, YoutubeSearch

DEFAULT_CALCULATOR = Calculator

DEFAULT_PLUGIN = Apps

PLUGINS = {
    'g': GoogleSearch,
    'y': YoutubeSearch,
    'f': Files,
}
