import streamlit as st
import numpy as np


st.title("Playground applications")

st.subheader("Most common color")
img_file = st.file_uploader("Choose a file")
if img_file is not None:
    print(img_file.id, img_file.name, img_file.type, img_file.size)
    print(uploaded_file.getvalue().shape)
st.write("success!")
    
