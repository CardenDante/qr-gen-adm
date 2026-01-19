"""
Script to create QR icon and build executable
"""
import qrcode
from PIL import Image

print("Creating QR code icon...")
# Generate QR code icon
qr = qrcode.QRCode(version=1, box_size=10, border=1)
qr.add_data("QR")
qr.make(fit=True)
icon_img = qr.make_image(fill_color="black", back_color="white")
icon_img = icon_img.resize((256, 256), Image.Resampling.LANCZOS)

# Save as ico file
icon_img.save("qr_icon.ico", format='ICO')
print("Icon created: qr_icon.ico")

print("\nNow run: pyinstaller --onefile --windowed --icon=qr_icon.ico --name=QRLabelPrinter main.py")
