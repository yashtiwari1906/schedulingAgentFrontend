import streamlit as st
import asyncio
import websockets

# Function to handle WebSocket connection and message handling
async def websocket_handler(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                st.session_state.messages.append(message)
                st.experimental_rerun()
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

# Function to send messages through WebSocket
async def send_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)

# Streamlit app layout
st.title("WebSocket Chat App")

# Initialize session state for messages if not already done
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display messages received from the server
for msg in st.session_state.messages:
    st.write(msg)

# Input box for user to type a message
user_input = st.text_input("Type your message:")

# Button to send the message
if st.button("Send"):
    if user_input:
        # Send the user's message through WebSocket
        asyncio.run(send_message("ws://localhost:6000/ws/chat/?userId=teslaEmp4", user_input))
        user_input = ""  # Clear input after sending

# Start the WebSocket handler in a separate thread if not already started
if 'ws_started' not in st.session_state:
    asyncio.run(websocket_handler("ws://localhost:6000/ws/chat/?userId=teslaEmp4"))
    st.session_state.ws_started = True
