from collections import Counter
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import os, sys
from multiprocessing import Pool, Process, connection, current_process, Queue
import numpy as np
from PIL import Image, ImageColor
import tqdm
from typing import List


# patch missing asscaler func for colormath dependency
# TODO add reference github link here
def patch_asscaler(a):
    return a.item()

setattr(np, "asscalar", patch_asscaler)

class ColorDist(object):
    """
    A class used to represent the color distribution of an image.

    ...

    Attributes
    ----------
    img : PIL.Image
    color_cnt : Dict (r, g, b) -> Int
    n_colors : Int

    Methods
    -------
    most_common_colors(n=3)
        Returns a list of the n-most common colors as sRGBColor objects

    uniq_colors(colors: List)
        Uses delta_e function to calculate the diff between colors in the list
        and return list of unique colors. Uniqueness defined by delta_e threshold.

    most_common_uniq(n=3)
        Parallelized process to get the n-most common, unique colors in the image.

    get_color_mask(color)
        Get an array mask of bools where pixel value equals color in the image.

    get_color(coordinates)
        Returns the RGB of the pixel at coordinates
    """

    def __init__(self, bytes_arr: List):
        self.img = Image.open(bytes_arr)
        self.color_cnt = Counter([pixel for pixel in self.img.getdata()])
        self.n_colors = len(self.color_cnt.keys())

    def most_common_colors(self, n=3):
        return [sRGBColor(*rgb, is_upscaled=True) for rgb, _ in self.color_cnt.most_common(n)]

    def uniq_colors(self, colors):
        uniq_colors = list()
        for c in colors:
             color_diffs = []
             color = sRGBColor(*c, is_upscaled=True)
             for uniq_color in uniq_colors:
                 color1 = convert_color(color, LabColor)
                 color2 = convert_color(uniq_color, LabColor)
                 color_diff = delta_e_cie2000(color1, color2)
                 color_diffs.append(color_diff)
             if len(uniq_colors) == 0 or np.min(np.array(color_diffs)) >= 50:
                 # https://zschuessler.github.io/DeltaE/learn/
                 uniq_colors.append(color)
        return uniq_colors

    def most_common_uniq(self, n=3):
        colors = self.most_common_colors(self.n_colors)
        NUM_WORKERS = 4
        chunk_size = self.n_colors // NUM_WORKERS
        slice = ColorDist.chunks(colors, chunk_size)
        with Pool(processes=NUM_WORKERS) as pool:
            results = list(tqdm.tqdm(pool.imap(self.uniq_colors, slice), total=len(slice))) 
            color_set = { x for l in results for x in l} 
            return tuple(color_set)[:n]
    
    def get_color_mask(self, color):
        return np.where( np.all(np.array(self.img) == np.array(color.get_upscaled_value_tuple()), axis=-1))
    
    def get_color(self, coordinates):
        x = coordinates["x"]
        y = coordinates["y"]
        return self.img.getpixel((x, y))

    @staticmethod
    def chunks(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]

