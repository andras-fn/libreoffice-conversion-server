import subprocess
import threading
import time
import socket
import logging
import sys

logger = logging.getLogger("libreoffice_manager")
logging.basicConfig(level=logging.INFO)

class LibreOfficeManager:
    def __init__(self, uno_interface="127.0.0.1", uno_port=2002):
        self.uno_interface = uno_interface
        self.uno_port = uno_port
        self.libreoffice_process = None

    def start_libreoffice(self):
        connection = f"socket,host={self.uno_interface},port={self.uno_port};urp;StarOffice.ComponentContext"

        cmd = [
            "libreoffice",
            "--headless",
            "--invisible",
            "--nocrashreport",
            "--nodefault",
            "--nologo",
            "--nofirststartwizard",
            "--nolockcheck",
            "--norestore",
            f"--accept={connection}",
        ]

        logger.info("Starting LibreOffice with command: " + " ".join(cmd))
        self.libreoffice_process = subprocess.Popen(cmd)

        # Wait for LibreOffice to be ready
        time.sleep(10)

        if not self.is_libreoffice_running():
            logger.error("LibreOffice failed to start.")
            sys.exit(1)

        logger.info("LibreOffice started successfully.")

    def is_libreoffice_running(self):
        try:
            with socket.create_connection((self.uno_interface, self.uno_port), timeout=5):
                return True
        except (ConnectionRefusedError, socket.timeout):
            return False

    def stop_libreoffice(self):
        if self.libreoffice_process:
            self.libreoffice_process.terminate()
            self.libreoffice_process.wait()
            logger.info("LibreOffice stopped.")

def main():
    manager = LibreOfficeManager()
    manager.start_libreoffice()

    # Run the test script
    try:
        subprocess.run(["python", "test_libreoffice.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Test script failed: {e}")
    finally:
        manager.stop_libreoffice()

if __name__ == "__main__":
    main()
