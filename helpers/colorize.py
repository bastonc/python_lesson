class Colorize:
    color_to_ANSI_sequences = {'gray': '90',
                  'red': '91',
                  'green': '92',
                  'yellow': '93',
                  'blue': '94',
                  'pink': '95',
                  'turquoise': '96'}

    def __init__(self, color):
        self.color = self.color_to_ANSI_sequences[color]

    def __enter__(self):
        print(f'\033[{self.color}m', end='')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'\033[0m', end='')
