import streamlit.components.v1 as components
import streamlit as st

from constants import REACT_FRONTEND_AGENT_SERVER_URL

# # Load the React component
# my_component = components.declare_component("chat", path="frontend/build")

# def render_react_component():
#     return my_component()




def chatPage():
    import streamlit as st

    # st.set_page_config(page_title="Chat App", layout="wide")

    st.title("Donna's Cabin")
    st.write("Hi there please let me know what do you want and I can provide you that right away. cause I'm Donna")

    # Embed the React app
    st.components.v1.iframe(REACT_FRONTEND_AGENT_SERVER_URL, height=600, scrolling=True)
