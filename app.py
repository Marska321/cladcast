# app.py
import streamlit as st
from PIL import Image
import uuid
import io

from weather import get_weather_forecast
from llm_stylist import get_outfit_recommendation
from firebase_config import init_firebase

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_wardrobe_items(_db):
    items_ref = _db.collection("items").stream()
    return [item.to_dict() for item in items_ref]

st.set_page_config(page_title="CladCast", layout="wide")
load_css("style.css")
db, bucket = init_firebase()

st.title("CladCast 👕🌦️")
st.write("Your permanent, weather-aware stylist. Add items to your closet, and I'll help you dress for tomorrow.")

with st.sidebar:
    st.header("Add to Your Closet")
    uploaded_photo = st.camera_input("Take a photo of a clothing item")
    item_description = st.text_input("Item name or description", key="item_desc")
    
    if st.button("Add Item", use_container_width=True):
        if uploaded_photo and item_description:
            with st.spinner("Saving your item..."):
                image = Image.open(uploaded_photo)
                byte_arr = io.BytesIO()
                image.save(byte_arr, format='PNG')
                filename = f"images/{uuid.uuid4()}.png"
                blob = bucket.blob(filename)
                blob.upload_from_string(byte_arr.getvalue(), content_type='image/png')
                blob.make_public()
                
                db.collection("items").add({"description": item_description, "image_url": blob.public_url})
                st.success(f"Added '{item_description}'!")
                st.cache_data.clear()
        else:
            st.error("Please take a photo and add a description.")

st.header("Your Digital Closet")
wardrobe = get_wardrobe_items(db)

if not wardrobe:
    st.info("Your closet is empty. Add some items using the sidebar!")
else:
    cols = st.columns(5)
    for i, item in enumerate(wardrobe):
        with cols[i % 5]:
            st.image(item["image_url"], caption=item["description"], use_container_width=True)

st.divider()
st.header("Get Your Outfit Recommendation")
user_plan = st.text_input("What are your plans for tomorrow?", "A casual day out")

if st.button("What Should I Wear Tomorrow?", type="primary", use_container_width=True):
    if not wardrobe:
        st.error("You must add items to your closet first.")
    else:
        with st.spinner("Forecasting your perfect outfit..."):
            weather_data = get_weather_forecast()
            wardrobe_list = [item["description"] for item in wardrobe]
            recommendation = get_outfit_recommendation(weather_data, wardrobe_list, user_plan)
            
            st.subheader("Tomorrow's Weather in Cape Town")
            st.write(weather_data)

            st.markdown(recommendation)
