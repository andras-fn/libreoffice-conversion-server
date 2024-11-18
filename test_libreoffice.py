import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.io import XOutputStream
import unohelper
import io

class OutputStream(unohelper.Base, XOutputStream):
    def __init__(self):
        self.buffer = io.BytesIO()

    def closeOutput(self):
        pass

    def writeBytes(self, seq):
        self.buffer.write(seq.value)

def convert_document(input_data, convert_to):
    try:
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context
        )
        context = resolver.resolve(
            "uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext"
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
        print(f"Conversion error: {e}")
        raise

if __name__ == "__main__":
    with open("test.docx", "rb") as f:
        input_data = f.read()
    result = convert_document(input_data, "writer_pdf_Export")
    with open("output.pdf", "wb") as f:
        f.write(result)
