from statistics import mean


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


def median_cut(img, num_colors):
    colors = []
    for color_count, color in img.getcolors(img.width * img.height):
        colors += [color] * color_count
    cubes = [ColorCube(colors)]

    while len(cubes) < num_colors:
        cubes.sort()
        cubes += cubes.pop().split()

    return [c.average() for c in cubes]
