
import cv2
import pyzbar.pyzbar as pyzbar
import qrcode
import barcode
from barcode.writer import ImageWriter
import requests
from urllib.parse import urlparse
from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Scanning and Decoding
def scan_code(image_path):
    print(f"Scanning image at: {image_path}")
    if not os.path.exists(image_path):
        print(f"Error: Image file does not exist at {image_path}")
        return None, "Error: Image file does not exist."
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: Could not load image for scanning.")
        return None, "Error: Could not load image."
    max_dimension = 1500
    height, width = image.shape
    if max(height, width) > max_dimension:
        scale = max_dimension / max(height, width)
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
    elif max(height, width) < 500:  # Upscale if too small
        scale = 500 / min(height, width)
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_LINEAR)
    # Enhance contrast
    image = cv2.equalizeHist(image)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   
    decoded_objects = pyzbar.decode(image)
    if decoded_objects:
        data = decoded_objects[0].data.decode('utf-8')
        print(f"Decoded data: {data}")
        return data, None
    print("No code detected in image.")
    return None, "No code detected"

# Fake Detection
def detect_fake(data):
    print(f"Checking data for fake: {data}")
    try:
        if data.startswith(('http://', 'https://')):
            parsed_url = urlparse(data)
            domain = parsed_url.netloc
            if not domain or 'suspicious' in domain.lower():
                return "Warning: Potentially malicious URL!"
            response = requests.head(data, allow_redirects=True, timeout=5)
            if response.status_code != 200:
                return "Warning: URL may be invalid!"
            if 'phish' in data.lower():
                return "Warning: Possible phishing attempt!"
        else:
            if len(data) < 5:
                return "Warning: Data appears tampered!"
        return "Code appears safe."
    except Exception as e:
        return f"Error: {str(e)}"

# Generate QR Code
def generate_qr(data, filename='static/qrcode.png'):
    print(f"Generating QR code with data: {data}")
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR code saved to: {filename}")
        return filename
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return None

# Generate Barcode
def generate_barcode(data, filename='static/barcode'):
    print(f"Generating barcode with data: {data}")
    if len(data) > 80:
        print("Warning: Data too long for reliable barcode scanning.")
        return None
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        options = {'module_width': 0.6, 'module_height': 20.0, 'quiet_zone': 10.0}
        code128 = barcode.get('code128', data, writer=ImageWriter())
        saved_file = code128.save(filename)
        print(f"Barcode saved to: {saved_file}")
        return saved_file
    except Exception as e:
        print(f"Error generating barcode: {str(e)}")
        return None

# Web Interface
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    qr_file = None
    barcode_file = None
    error = None
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        print(f"Form data: {request.form}")
        print(f"Files: {request.files}")
        if 'image' in request.files and request.files['image'].filename:
            print("Processing uploaded image for scanning...")
            file = request.files['image']
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                print("Error: Uploaded file is not a supported image format.")
                error = "Error: Please upload a PNG, JPG, or JPEG image."
            else:
                file_path = 'static/uploaded.png'
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                print(f"Image saved to: {file_path}")
                data, scan_error = scan_code(file_path)
                if data:
                    result = detect_fake(data)
                    print(f"Fake detection result: {result}")
                else:
                    result = scan_error
                    print(f"Scan error: {result}")
        elif 'generate_qr' in request.form:
            data = request.form.get('qr_data', '')
            print(f"QR data received: {data}")
            if data:
                qr_file = generate_qr(data)
                if not qr_file:
                    error = "Failed to generate QR code"
            else:
                error = "No data provided for QR code"
        elif 'generate_barcode' in request.form:
            data = request.form.get('barcode_data', '')
            print(f"Barcode data received: {data}")
            if data:
                if len(data) > 80:
                    error = "Error: Barcode data too long (max 80 characters)."
                else:
                    barcode_file = generate_barcode(data)
                    if not barcode_file:
                        error = "Failed to generate barcode"
                    else:
                        barcode_file = barcode_file.rsplit('.png', 1)[0]
            else:
                error = "No data provided for barcode"
    return render_template('index.html', result=result, qr_file=qr_file, barcode_file=barcode_file, error=error)

@app.route('/download/<filename>')
def download(filename):
    print(f"Serving file: {filename}")
    if not os.path.exists(os.path.join('static', filename)):
        print(f"Error: File {filename} does not exist in static folder.")
        return "File not found", 404
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


