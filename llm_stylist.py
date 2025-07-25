# llm_stylist.py
from groq import Groq
import streamlit as st

def get_outfit_recommendation(weather_data, wardrobe_list, user_plan):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        wardrobe_text = ", ".join(wardrobe_list) or "nothing"
        system_prompt = "You are 'CladCast', a friendly, practical AI stylist. Recommend an outfit using only items from the user's wardrobe based on the weather and their plans."
        
        user_prompt = f"""
        ### CONTEXT
        - **Weather:** {weather_data}
        - **User's Plan:** "{user_plan}"
        - **Available Wardrobe:** {wardrobe_text}

        ### TASK
        Recommend one complete outfit using ONLY items from the available wardrobe. Briefly explain *why* it works, referencing the weather and plans. If a crucial item is missing, mention it. Format the output clearly using markdown, starting with a headline.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the AI model on Groq: {e}"