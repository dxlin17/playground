from colormath.color_objects import LabColor, sRGBColor
from color_clf.color_dist import ColorDist
from io import BytesIO
import numpy as np
from PIL import Image 
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as sic


st.title("Playground applications")

with open("docs/color_clf_desc.md") as contents:
    st.markdown(contents.read())

def render_color_square(sRGB, size=32):
    return np.full((size, size, 3), sRGB.get_upscaled_value_tuple(), dtype=np.int32)


img_file = st.file_uploader("Choose a file")
if img_file is not None:
    img_data = BytesIO(img_file.getvalue())
    dist = ColorDist(img_data)

    value = sic(dist.img, key="pil", width=dist.img.width, height=dist.img.height)
    if value is None:
        value = {"x": 0, "y": 0}
    c1, c2 = st.columns([1, 1])
    color_at_cursor = sRGBColor(*dist.get_color(value), is_upscaled=True)
    c1.image(render_color_square(color_at_cursor))
    color = color_at_cursor
    st.write(color.get_rgb_hex())

    mask = dist.get_color_mask(color)
    color_mask = np.full((dist.img.width, dist.img.height, 3), (0, 0, 0))
    color_mask[mask] = (255, 255, 255)
    st.image(color_mask)
