from flask import Flask, request, jsonify
import subprocess
import logging
import time
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Home route (fixes the 404 Not Found issue)
@app.route('/', methods=['GET'])
def home():
    return "✅ Webhook running! Send POST requests to /alert", 200


# 🚨 Alert route — called by Alertmanager
@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    logging.info("Received alert payload")

    # Extract alert name and severity
    alert_name = data['alerts'][0]['labels'].get('alertname', 'unknown')
    severity = data['alerts'][0]['labels'].get('severity', 'unknown')

    logging.info(f"Alert: {alert_name} severity={severity}")

    # Define playbook command
    timestamp = int(time.time())
    log_file = f"/webhook/ansible_run_{timestamp}.log"
    cmd = [
        "ansible-playbook",
        "-i", "/ansible/inventory.ini",
        "/ansible/restart-nginx.yml"
    ]

    # Run ansible playbook
    with open(log_file, "w") as f:
        subprocess.Popen(cmd, stdout=f, stderr=f)

    logging.info(f"Starting ansible playbook: {' '.join(cmd)}, logging to {log_file}")

    return jsonify({"status": "ansible_started", "log": log_file})


if __name__ == "__main__":
    # Flask will listen on all network interfaces (Docker-friendly)
    app.run(host="0.0.0.0", port=5001)

