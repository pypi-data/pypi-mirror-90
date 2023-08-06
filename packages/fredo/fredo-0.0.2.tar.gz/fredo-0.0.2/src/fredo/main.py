import os
import sys

from fredo.core import Fredo

def main():
    # TODO add option to run with logs
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

    from fredo.gui.gui import MainApp

    MainApp().run()


if __name__ == "__main__":
    sys.exit(main())
