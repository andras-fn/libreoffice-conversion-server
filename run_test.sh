#!/bin/sh

# Start LibreOffice in the background
libreoffice --headless --invisible --nocrashreport --nodefault --nologo --nofirststartwizard --nolockcheck --norestore --accept="socket,host=127.0.0.1,port=2002;urp;StarOffice.ServiceManager" &

# Wait for LibreOffice to start
sleep 10

# Check if LibreOffice service is available
for i in $(seq 1 10); do
    echo "Checking if LibreOffice is available (attempt $i)..."
    if netstat -an | grep -q 2002; then
        echo "LibreOffice is available."
        break
    fi
    sleep 5
done

# Run the test script
python test_libreoffice.py
