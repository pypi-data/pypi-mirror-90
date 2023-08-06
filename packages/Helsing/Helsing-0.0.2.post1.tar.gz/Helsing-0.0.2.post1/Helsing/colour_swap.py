"""
Use RegEx to find hex values and swap them around.
"""

import re
import qdarkstyle
from PyQt5.QtWidgets import QApplication

def activate_swap(string: str, values: list) -> str:
    """
    Takes a string value, and a list of placement for the colour values:
    e.g. [1, 3, 2] will keep the R value in place, while moving the G to the B spot, and the B to the G.
    e.g. [3, 1, 2] will move the R value the the 3rd (B) spot, the G to the 1st (R) spot, and the B to the 2nd (G).
    :param string: the string containing hex values
    :param values: the order, presented in a list, that we wish to create.
    :return: the string with hex values re-ordered.
    """
    if len(values) != 3:
        print("Require 3 values for re-ordering.")
        return "Try again"

    regex = re.compile('#([0123456789abcdef]{2})([0123456789abcdef]{2})([0123456789abcdef]{2})', re.IGNORECASE)

    return regex.sub(f'#\\{values[0]}\\{values[1]}\\{values[2]}', string)


def main():
    app = QApplication([])
    dark = qdarkstyle.load_stylesheet()
    with open('stylesheets/dark_blue.css', 'w') as f:
        f.write(activate_swap(dark, [1, 2, 3]))
    with open('stylesheets/dark_teal.css', 'w') as f:
        f.write(activate_swap(dark, [1, 3, 2]))
    with open('stylesheets/dark_magenta.css', 'w') as f:
        f.write(activate_swap(dark, [3, 1, 2]))
    with open('stylesheets/dark_purple.css', 'w') as f:
        f.write(activate_swap(dark, [2, 1, 3]))
    with open('stylesheets/dark_yellowGreen.css', 'w') as f:
        f.write(activate_swap(dark, [2, 3, 1]))
    with open('stylesheets/dark_orange.css', 'w') as f:
        f.write(activate_swap(dark, [3, 2, 1]))
    with open('stylesheets/dark_darkBlue.css', 'w') as f:
        f.write(activate_swap(dark, [1, 1, 2]))
    with open('stylesheets/dark_strongBlue.css', 'w') as f:
        f.write(activate_swap(dark, [1, 1, 3]))
    with open('stylesheets/dark_lilac.css', 'w') as f:
        f.write(activate_swap(dark, [2, 2, 3]))
    with open('stylesheets/dark_goldenrod.css', 'w') as f:
        f.write(activate_swap(dark, [2, 2, 1]))
    with open('stylesheets/dark_yellow.css', 'w') as f:
        f.write(activate_swap(dark, [3, 3, 1]))
    with open('stylesheets/dark_cornsilk.css', 'w') as f:
        f.write(activate_swap(dark, [3, 3, 2]))
    with open('stylesheets/dark_darkRed.css', 'w') as f:
        f.write(activate_swap(dark, [2, 1, 1]))
    with open('stylesheets/dark_red.css', 'w') as f:
        f.write(activate_swap(dark, [3, 1, 1]))
    with open('stylesheets/dark_pink.css', 'w') as f:
        f.write(activate_swap(dark, [3, 2, 2]))
    with open('stylesheets/dark_turquoise.css', 'w') as f:
        f.write(activate_swap(dark, [1, 2, 2]))
    with open('stylesheets/dark_cyan.css', 'w') as f:
        f.write(activate_swap(dark, [1, 3, 3]))
    with open('stylesheets/dark_powderBlue.css', 'w') as f:
        f.write(activate_swap(dark, [2, 3, 3]))
    with open('stylesheets/dark_green.css', 'w') as f:
        f.write(activate_swap(dark, [1, 2, 1]))
    with open('stylesheets/dark_limeGreen.css', 'w') as f:
        f.write(activate_swap(dark, [1, 3, 1]))
    with open('stylesheets/dark_paleGreen.css', 'w') as f:
        f.write(activate_swap(dark, [2, 3, 2]))
    with open('stylesheets/dark_darkViolet.css', 'w') as f:
        f.write(activate_swap(dark, [2, 1, 2]))
    with open('stylesheets/dark_fuchsia.css', 'w') as f:
        f.write(activate_swap(dark, [3, 1, 3]))
    with open('stylesheets/dark_plum.css', 'w') as f:
        f.write(activate_swap(dark, [3, 2, 3]))


if __name__ == '__main__':
    main()
