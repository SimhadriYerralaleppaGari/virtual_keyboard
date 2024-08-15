import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
from virtual_keyboard import start_virtual_keyboard, stop_virtual_keyboard

app = Flask(__name__)
keyboard_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enable', methods=['POST'])
def enable_keyboard():
    global keyboard_thread
    if not keyboard_thread or not keyboard_thread.is_alive():
        keyboard_thread = threading.Thread(target=start_virtual_keyboard)
        keyboard_thread.start()
    return jsonify({"success": True})

@app.route('/disable', methods=['POST'])
def disable_keyboard():
    stop_virtual_keyboard()
    return jsonify({"success": True})

@app.route('/status')
def keyboard_status():
    global keyboard_thread
    enabled = keyboard_thread is not None and keyboard_thread.is_alive()
    return jsonify({"enabled": enabled})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)