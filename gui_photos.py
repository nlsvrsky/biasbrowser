import pandas as pd
import streamlit as st
from scipy.stats import norm
import os

if "image_set" not in st.session_state:
    image_set = "Photos"
else:
    image_set = st.session_state["image_set"]

if image_set == "Photos":
    img_dir = "CP_images"
    img_props = "Image_Properties_CP.csv"
else:
    img_dir = "LD_images"
    img_props = "Image_Properties_LD.csv"

z_transformed = True

img_df = pd.read_csv(img_props)
props = list(img_df.columns)
props = [prop for prop in props if prop not in ("hits", "misses", "false_alarms", "correct_rejections", "subject", "block", "Unnamed: 0", "Unnamed: 48", "Image size (pixels)", "Aspect ratio")]
props.reverse()

if z_transformed:
    img_df["HR"] = norm.cdf(img_df["HR"])
    img_df["FAR"] = norm.cdf(img_df["FAR"])

prop = st.selectbox("Sort by:", props)
asc_desc = st.radio("Direction:", ["Ascending", "Descending"])
image_set = st.radio("Image set:", ["Photos", "Line drawings"], key="image_set")

img_df = img_df.sort_values(prop, ascending=asc_desc == "Ascending")

for i, img in enumerate(img_df["stim"]):
    st.image(os.path.join(img_dir, img))
    st.caption("**Image:** " + img + "  \n**" + prop + ":** " + str(img_df[prop].iloc[i]) + "  \n(HR:" + str(img_df["HR"].iloc[i].round(2)) + ", FAR: " + str(img_df["FAR"].iloc[i].round(2)) + ")")
    st.divider()
