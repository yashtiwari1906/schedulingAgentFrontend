# import streamlit as st
# import random
# import time
# import streamlit as st
# import asyncio
# import websockets
# import threading

# st.title("Simple chat")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "user_id" not in st.session_state:
#     st.session_state.user_id = None

# if "user_email" not in st.session_state:
#     st.session_state.user_email = None

# st.header("Connection Information")
# st.write(
#     "Enter your email below to establish a connection. "
#     "Your user ID is generated as the part before '@' in your email."
# )

# with st.container():
#     with st.form("connection_form"):
#         email_input = st.text_input("Email", key="email_input_form")
#         connect_button = st.form_submit_button("Connect")

#     if connect_button:
#         if email_input and "@" in email_input:
#             st.session_state["user_email"] = email_input
#             st.session_state["user_id"] = email_input.split("@")[0]
#             st.success(f"Connected as **{st.session_state['user_id']}**")
#             st.rerun()  # Forces UI to update
#         else:
#             st.error("Please enter a valid email address.")

# # --------------------------------------
# # Prevent Access to Chat if No Email
# # --------------------------------------
# if not st.session_state["user_email"]:
#     st.info("Connect using your email above to start chatting.")
#     st.stop()

# # --------------------------------------
# # WebSocket Connection Setup
# # --------------------------------------
# user_id = st.session_state["user_id"]
# ws_url = f"ws://localhost:6000/ws/chat/?userId={user_id}"
# st.write(f"**WebSocket URL:** {ws_url}")


# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})


# # Streamed response emulator
# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

# def websocket_handler(message):

#     try:
#         with websockets.connect(ws_url) as websocket:
#             websocket.send(message)
#             response = websocket.recv()
#             return response
#     except Exception as e:
#         return f"❌ Error: {str(e)}"

# def send_message(message):
#     # Create a new event loop for this thread.
#     # loop = asyncio.new_event_loop()
#     # asyncio.set_event_loop(loop)
#     # response = loop.run_until_complete(websocket_handler(message))
#     response = websocket_handler(message)
#     return response

# # Display assistant response in chat message container
# with st.chat_message("assistant"):
#     response = send_message(prompt)
# # Add assistant response to chat history
# st.session_state.messages.append({"role": "assistant", "content": response})


import queue
from constants import LOCAL_URL, LOCAL_WEBSOCKET_URL
import streamlit as st
import asyncio
import websockets
import websockets.sync.client
import threading
from streamlit_autorefresh import st_autorefresh


def chatPage():
    st.title("💬 Chat Application")

    # --------------------------------------
    # ✅ Properly Initialize Session State
    # --------------------------------------
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""

    if "user_id" not in st.session_state:
        st.session_state["user_id"] = ""

    if "messages" not in st.session_state:
        st.session_state["messages"] = []  # Ensuring 'messages' exists

    # --------------------------------------
    # Top Section: Email Input & Connection Info
    # --------------------------------------
    st.header("Connection Information")
    st.write(
        "Enter your email below to establish a connection. "
        "Your user ID is generated as the part before '@' in your email."
    )

    state_lock = threading.Lock()

    with st.container():
        with st.form("connection_form"):
            email_input = st.text_input("Email", key="email_input_form")
            connect_button = st.form_submit_button("Connect")

        if connect_button:
            if email_input and "@" in email_input:
                st.session_state["user_email"] = email_input
                st.session_state["user_id"] = email_input.split("@")[0]
                st.success(f"Connected as **{st.session_state['user_id']}**")
                st.rerun()  # Forces UI to update
            else:
                st.error("Please enter a valid email address.")

    # --------------------------------------
    # Prevent Access to Chat if No Email
    # --------------------------------------
    if not st.session_state["user_email"]:
        st.info("Connect using your email above to start chatting.")
        return
    message_queue = queue.Queue()

    def websocket_listener(session_state):
        try:
            with websockets.sync.client.connect(ws_url) as websocket:
                response = websocket.recv()
                print(response)
                message_queue.put({"role": "assistant", "content": response})
                with state_lock:
                    session_state.append({"role": "assistant", "content": response})
                print(session_state)
                with st.chat_message("assistant"):
                    st.markdown(response)
                return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # --------------------------------------
    # WebSocket Connection Setup
    # --------------------------------------
    user_id = st.session_state["user_id"]
    ws_url = f"{LOCAL_WEBSOCKET_URL}/ws/chat/?userId={user_id}"
    st.write(f"**WebSocket URL:** {ws_url}")

    thread = threading.Thread(target=websocket_listener, args=[st.session_state])
    thread.start()
    st.subheader("Chat History")
    # Display chat messages from history on app rerun
    while not message_queue.empty():
        print(message_queue)
        msg = message_queue.get()
        st.session_state.messages.append(msg)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --------------------------------------
    # WebSocket Communication Logic
    # --------------------------------------

    def websocket_handler(message):
        try:
            with websockets.sync.client.connect(ws_url) as websocket:
                websocket.send(message)
                response = websocket.recv()
                return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # def send_message(message):
    #     # Create a new event loop for this thread.
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     response = loop.run_until_complete(websocket_handler(message))

    #     # Ensure messages is always updated
    #     if "messages" not in st.session_state:
    #         st.session_state["messages"] = []

    #     st.session_state["messages"].append(f"🟢 You: {message}")
    #     st.session_state["messages"].append(f"🔵 Server: {response}")
    #     st.rerun()  # Updates UI

    # --------------------------------------
    # Chat Section
    # --------------------------------------
    st.header("Chat")
    user_message = st.text_input("Enter your message:", key="message_input")
    if st.button("Send"):
        if user_message:
            # Run send_message in a separate thread to keep UI responsive
            response = websocket_handler(user_message)
            st.session_state.messages.append({"role": "user", "content": user_message})
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Please enter a message before sending.")

    # --------------------------------------
    # Chat History Display
    # --------------------------------------


# if __name__ == "__main__":
#     chatPage()
