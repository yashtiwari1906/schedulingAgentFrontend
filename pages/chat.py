import streamlit.components.v1 as components
import streamlit as st

# # Load the React component
# my_component = components.declare_component("chat", path="frontend/build")

# def render_react_component():
#     return my_component()




def chatPage():
    import streamlit as st

    # st.set_page_config(page_title="Chat App", layout="wide")

    st.title("Embedded React Chat App")

    # Embed the React app
    st.components.v1.iframe("http://localhost:3001", height=600, scrolling=True)
