from flask import Flask, request, send_file, jsonify
import io
import logging
import os
from unoserver_master.src.unoserver.client import UnoClient

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the unoserver host and port from environment variables
unoserver_host = os.getenv('UNOSERVER_HOST', 'localhost')
unoserver_port = os.getenv('UNOSERVER_PORT', '2003')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    convert_to = request.form.get('convert_to', 'pdf')  # Default to PDF if not specified
    try:
        client = UnoClient(server=unoserver_host, port=unoserver_port)
        result = client.convert(indata=file.read(), convert_to=convert_to)
        return send_file(
            io.BytesIO(result),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=f'converted.{convert_to}'
        )
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
