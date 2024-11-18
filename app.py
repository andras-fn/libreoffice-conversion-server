import sys
import os
import io
import logging
import subprocess
import threading
import time
import uno
import unohelper
from flask import Flask, request, send_file, jsonify
from com.sun.star.beans import PropertyValue
from com.sun.star.io import XOutputStream

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OutputStream(unohelper.Base, XOutputStream):
    def __init__(self):
        self.buffer = io.BytesIO()

    def closeOutput(self):
        pass

    def writeBytes(self, seq):
        self.buffer.write(seq.value)

class LibreOfficeManager:
    def __init__(self, host="127.0.0.1", port="2002"):
        self.host = host
        self.port = port
        self.process = None

    def start(self):
        if self.is_running():
            logger.info("LibreOffice is already running.")
            return

        connection = f"socket,host={self.host},port={self.port};urp;StarOffice.ComponentContext"
        cmd = [
            "libreoffice",
            "--headless",
            "--invisible",
            "--nocrashreport",
            "--nodefault",
            "--nologo",
            "--nofirststartwizard",
            "--norestore",
            f"--accept={connection}"
        ]
        logger.info("Starting LibreOffice with command: " + " ".join(cmd))
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(20)  # Increase the wait time to ensure LibreOffice starts

    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(10)
            except subprocess.TimeoutExpired:
                logger.info("Killing LibreOffice process")
                self.process.kill()

    def is_running(self):
        return self.process and self.process.poll() is None

libreoffice_manager = LibreOfficeManager()

def check_libreoffice():
    try:
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context
        )
        context = resolver.resolve(
            f"uno:socket,host={libreoffice_manager.host},port={libreoffice_manager.port};urp;StarOffice.ComponentContext"
        )
        service = context.ServiceManager
        desktop = service.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context
        )
        return True
    except Exception as e:
        logger.error(f"LibreOffice headless service is not available: {e}")
        return False

def convert_document(input_data, convert_to):
    try:
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context
        )
        context = resolver.resolve(
            f"uno:socket,host={libreoffice_manager.host},port={libreoffice_manager.port};urp;StarOffice.ComponentContext"
        )
        service = context.ServiceManager
        desktop = service.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context
        )

        input_stream = service.createInstanceWithContext(
            "com.sun.star.io.SequenceInputStream", context
        )
        input_stream.initialize((uno.ByteSequence(input_data),))

        input_props = (
            PropertyValue(Name="InputStream", Value=input_stream),
            PropertyValue(Name="Hidden", Value=True),
        )

        document = desktop.loadComponentFromURL("private:stream", "_blank", 0, input_props)

        if document is None:
            raise RuntimeError("Could not load document")

        output_stream = OutputStream()
        output_props = (
            PropertyValue(Name="FilterName", Value=convert_to),
            PropertyValue(Name="OutputStream", Value=output_stream),
        )

        document.storeToURL("private:stream", output_props)
        document.close(True)

        return output_stream.buffer.getvalue()
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        raise

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    convert_to = request.form.get('convert_to', 'pdf')  # Default to PDF if not specified

    # Map convert_to to LibreOffice filter name
    filter_map = {
        'pdf': 'writer_pdf_Export',
        'docx': 'MS Word 2007 XML',
        'xlsx': 'Calc MS Excel 2007 XML',
        'pptx': 'Impress MS PowerPoint 2007 XML',
    }

    filter_name = filter_map.get(convert_to.lower())
    if not filter_name:
        return jsonify({"error": f"Unsupported conversion format: {convert_to}"}), 400

    # Check if LibreOffice headless service is available
    if not check_libreoffice():
        return jsonify({"error": "LibreOffice headless service is not available"}), 500

    try:
        result = convert_document(file.read(), filter_name)
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
    if not libreoffice_manager.is_running():
        libreoffice_manager.start()
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        libreoffice_manager.stop()
