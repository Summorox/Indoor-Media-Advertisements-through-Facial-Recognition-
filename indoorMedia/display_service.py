import os

from flask import Flask, request, send_from_directory, redirect, url_for
from threading import Thread
import cv2

app = Flask(__name__)

@app.route('/display', methods=['POST'])
def display_ad():
    global ad_path
    ad_path = request.get_json().get('ad_path')
    if ad_path is not None:
        print(f"Displaying ad: {ad_path}")
        return redirect(url_for('serve_ad'))
    else:
        print(f"Error: No ad_path provided.")
    return 'Error: No ad_path provided.', 400

@app.route('/ad', methods=['GET'])
def serve_ad():
    global ad_path
    if ad_path is None:
        return 'No ad to display', 404
    dir = os.path.dirname(ad_path)  # directory of ad
    filename = os.path.basename(ad_path)  # filename of ad
    return send_from_directory(dir, filename)

if __name__ == '__main__':
    app.run(port=50000)