import fnmatch
from pathlib import Path

from fredo.plugins.base import Plugin


class Files(Plugin):

    path = str(Path.home())
    label = "Launch"

    def get_options(self, query):
        if not query:
            return [self.make_item(title='search files')]
        options = []
        for root, dirnames, filenames in os.walk(self.path):
            for filename in fnmatch.filter(filenames, f'*{query}*'):
                if len(options) == 5:
                    break
                options.append(
                    self.make_item(title=filename, command=os.path.join(root, filename), subtitle=self.label)
                )
        return options

    def action(self, command):
        import subprocess
        subprocess.Popen(["xdg-open", command])
