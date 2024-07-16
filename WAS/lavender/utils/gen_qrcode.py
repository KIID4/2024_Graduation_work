import base64
from io import BytesIO
import qrcode


def generate_qrcode(data):
    buffered = BytesIO()
    myQR = qrcode.make(";".join(data))
    myQR.save(buffered)
    qrcode_image = base64.b64encode(buffered.getvalue()).decode()
    return qrcode_image
