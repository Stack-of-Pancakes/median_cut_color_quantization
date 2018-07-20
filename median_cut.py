from statistics import mean
from PIL import Image


class ColorCube(object):
    def __init__(self, colors):
        self.colors = colors or []
        self.red = [r[0] for r in colors]
        self.green = [g[1] for g in colors]
        self.blue = [b[2] for b in colors]
        self.size = (max(self.red) - min(self.red),
                     max(self.green) - min(self.green),
                     max(self.blue) - min(self.blue))
        self.max_range = max(self.size)
        self.max_channel = self.size.index(self.max_range)

    def average(self):
        r = int(mean(self.red))
        g = int(mean(self.green))
        b = int(mean(self.blue))
        return r, g, b

    def split(self):
        middle = len(self.colors) // 2
        colors = sorted(self.colors, key=lambda c: c[self.max_channel])
        return ColorCube(colors[:middle]), ColorCube(colors[middle:])

    def __lt__(self, other):
        return self.max_range < other.max_range


def median_cut(img, num_colors, unique=False):
    # If unique is true then multiple instances of a single RGB value will only be counted once
    # and the rest discarded. This is MUCH faster and creates a more diverse pallete, but is not
    # a "true" median cut.
    # For example if an image had 99 blue pixels (0,0,255) and a single red pixel (255,0,0) the
    # respective median cuts would be
    # unique = False: [(0,0,255),(5,0,249)]
    # unique = True:  [(0,0,255),(255,0,0)]
    # False would produce 2 almost identical shades of blue, True would result in pure blue/red
    colors = []
    for color_count, color in img.getcolors(img.width * img.height):
        if unique:
            colors += [color]
        else:
            colors += [color] * color_count
    cubes = [ColorCube(colors)]

    while len(cubes) < num_colors:
        cubes.sort()
        cubes += cubes.pop().split()

    return [c.average() for c in cubes]


def show_median_cut(cuts):
    # Create background for the palette
    palette = Image.new('RGB', (100 * len(cuts), 100))

    # Create a square of each color and insert each, side-by-side, into the palette
    for i in range(len(cuts)):
        color = Image.new('RGB', (100, 100), cuts[i])
        palette.paste(color, (100 * i, 0))

    palette.show()


my_image = Image.open('input/cogs.jpg')

# Create two palettes.  One with true median cut and the other with unique colors.
median_non_unique = median_cut(my_image, 8)
median_unique = median_cut(my_image, 8, unique=True)

