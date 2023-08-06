import os
from pathlib import Path

from fredo.plugins.base import Plugin
from fredo.plugins.utils import run_app


class Apps(Plugin):

    user_dpath = str(Path.home().joinpath('.local/share/applications'))
    dpath = "/usr/share/applications/"
    label = "Launch"

    def get_options(self, query):
        apps = self.get_app_list(self.dpath, self.user_dpath)
        apps.sort()
        options = []
        for app in apps:
            if len(options) == 5:
                break
            if query.lower() in app.lower():
                app_item = self.parse_desktop_file(app)
                if app_item:
                    app_item['subtitle'] = f'{self.label}'
                    options.append(app_item)
        return options

    def action(self, command):
        run_app(command)

    def get_app_list(self, *args):
        apps = []
        for path in args:
            for file in os.listdir(path):
                apps.append(os.path.join(path, file))
        return apps

    def parse_desktop_file(self, app):
        app_item = {}
        with open(app) as f:
            for line in f.readlines():
                if line[0:5] == 'Name=' and 'title' not in app_item.keys():
                    app_item['title'] = line.split("=")[1].strip("\r\n")
                if line[0:5] == "Exec=":
                    app_item['command'] = self.parse_line(line.split("=")[1].strip("\r\n"))
                    if len(app_item) > 1:
                        return app_item
        return None

    @staticmethod
    def parse_line(line):
        # Line can be something like /usr/bin/app --something %U
        # or just 'app', so we check. If it's the former case,
        # we only want to end up with 'app --something'
        le = line.split(" ")
        if len(le) > 1:
            del le[-1]
        exe = ' '.join(le)
        return exe
