import os


CLOUD_RUN_URL = "https://bmls-master-364846809818.us-central1.run.app"
LOCAL_WEBSOCKET_URL = "ws://localhost:6000"
LOCAL_URL = "http://0.0.0.0:6000"
GCP_AGENT_URL = "http://34.100.164.25:6000"


REACT_FRONTEND_AGENT_SERVER_LOCAL_URL = "http://localhost:3001"
REACT_FRONTEND_GCP_URL = "http://34.100.164.25:3001"

GCP_IP = os.environ.get("GCP_IP")
REACT_FRONTEND_AGENT_SERVER_URL = f"http://{GCP_IP}:3001"
AGENT_SERVER_URL = LOCAL_URL #f"http://{GCP_IP}:6000"
