from flask import Flask, request, jsonify
from flask_cors import CORS
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    website_link = data.get('link')
    fill_color = data.get('fill_color', 'black')  # Default color if not provided
    back_color = data.get('back_color', 'white')  # Default color if not provided
    error_correction = data.get('error_correction', 'M')  # Default error correction level

    if not website_link:
        return jsonify({'error': 'No link provided'}), 400

    error_correction_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }

    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
        box_size=10,
        border=5
    )
    qr.add_data(website_link)
    qr.make()

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    img_url = f'data:image/png;base64,{img_str}'

    return jsonify({'qr_code_url': img_url})

if __name__ == '__main__':
    app.run(debug=True)
