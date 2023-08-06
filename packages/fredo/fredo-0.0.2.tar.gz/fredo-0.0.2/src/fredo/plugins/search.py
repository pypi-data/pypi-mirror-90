from fredo.plugins.base import Plugin


class GoogleSearch(Plugin):

    label = "Search with google"

    def get_options(self, query):
        return [self.make_item(title=query, command=query, subtitle=self.label)]

    def action(self, command):
        import webbrowser
        query = command.replace(" ", "+")
        url = f"https://google.com/search?q={query}"
        webbrowser.open(url)


class YoutubeSearch(Plugin):

    label = "Search with Youtube"

    def get_options(self, query):
        return [self.make_item(title=query, command=query, subtitle=self.label)]

    def action(self, command):
        import webbrowser
        query = command.replace(" ", "+")
        url = f"https://youtube.com/results?search_query={query}"
        webbrowser.open(url)
