class PlotConfig(object):
    """ Class for defining traffic stops code configuration details """

    def __init__(self):
        # Define colorscheme
        self.COLORSCHEME = {
            'black': '#1b9e77',
            'white': '#a9a9a9',
            'hispaniclatino': '#d95f02',
            'hispanic/latino': '#d95f02',
            'asian': '#7570b3',
            'nativeamerican': 'y',
            'native american': 'y',
            'pacific': 'c',
            'male': '#222222',
            'female': '#222222',
        }

        self.LINESTYLE = {
            'male': '-.',
            'female': ':',
        }

    def get_color(self, name):
        if isinstance(name, list) or isinstance(name, tuple):
            for n in name:
                if n.lower() in self.COLORSCHEME:
                    return self.COLORSCHEME[n.lower()]
        try:
            return self.COLORSCHEME.get(name.lower(), '#000000')
        except:
            return self.COLORSCHEME.get(name, '#000000')


    def get_linestyle(self, name):
        if isinstance(name, list) or isinstance(name, tuple):
            return self.LINESTYLE.get(name[-1].lower(), '-')
        return self.LINESTYLE.get(name.lower(), '-')
