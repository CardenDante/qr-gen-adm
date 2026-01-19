# QR Label Printer - Release Notes

## Version 1.0.0 - January 2026

### 🎉 Initial Release

A professional Windows application for generating and printing QR code labels on thermal printers.

---

### ✨ Features

#### Core Functionality
- **QR Code Generation**: Generate high-quality QR codes from admission numbers
- **Label Printing**: Direct printing to Xprinter 470B thermal printers
- **Multiple Label Sizes**: Support for 5 standard label sizes:
  - 60 x 40 mm
  - 50 x 30 mm
  - 40 x 30 mm
  - 50 x 25 mm
  - 70 x 40 mm

#### User Interface
- **Modern Design**: Clean, professional interface with light theme
- **Live Preview**: Real-time preview of generated QR codes before printing
- **Responsive Layout**: Dual-panel design with form controls and preview area
- **Keyboard Shortcuts**: Press Enter to quickly generate QR codes

#### Label Design
- **Professional Layout**: QR code on left, text identifier on right
- **Branded Format**: Labels include "WCN26F-" prefix with admission number
- **High Contrast**: Black and white design optimized for thermal printing
- **Border Frame**: Subtle border for professional appearance

#### Technical Features
- **Thermal Printer Optimization**: 203 DPI resolution support
- **Auto Printer Detection**: Automatically finds Xprinter 470B
- **Error Correction**: High-level error correction (ERROR_CORRECT_H) for reliable scanning
- **Standalone Executable**: Single .exe file with all dependencies included

---

### 🔧 Technical Specifications

**Platform**: Windows 10/11

**Supported Printers**:
- Xprinter 470B
- XP-470B
- Any printer with "XPRINTER" in name
- Falls back to default printer if Xprinter not found

**QR Code Specifications**:
- Format: Plain admission number (no prefix in QR data)
- Error Correction Level: High (30% recovery capability)
- Border: Minimal 2-unit border
- Version: Auto-fit (version 1+)

**Label Specifications**:
- Resolution: 203 DPI
- Color: Monochrome (1-bit)
- Format: Optimized for thermal printing
- QR Code Size: 90% of label height

---

### 📦 Distribution

**File**: `QRLabelPrinter.exe`

**Size**: ~50 MB (includes all dependencies)

**Requirements**:
- Windows 10 or later
- Thermal printer (recommended: Xprinter 470B)
- Printer drivers installed

**Installation**:
- No installation required
- Simply run the .exe file
- No Python or additional dependencies needed

---

### 🎨 Interface Highlights

- **Color Scheme**: Professional blue and green accents on white background
- **Typography**: Clear, readable fonts with proper hierarchy
- **Buttons**:
  - Green "Generate QR Code" button
  - Blue "Print Label" button (enabled after generation)
- **Footer**: "WCN26F © 2025" branding

---

### 🔄 Workflow

1. Enter admission number
2. Select label size from dropdown
3. Click "Generate QR Code" or press Enter
4. Preview the generated label
5. Click "Print Label" to send to printer
6. Form automatically clears after successful print

---

### 🐛 Known Limitations

- Windows only (uses win32 printing APIs)
- Requires thermal printer for optimal results
- Icon may not display on some systems (falls back to default)

---

### 🛠️ Build Information

**Built with**:
- Python 3.11
- CustomTkinter 5.2.2
- Pillow 10.4.0
- qrcode 7.4.2
- pywin32 306
- PyInstaller 6.18.0

**Icon**: Programmatically generated QR code icon

**Build Type**: Single-file executable (--onefile)

**Window Mode**: Windowed application (--windowed)

---

### 📝 Credits

**Developer**: WCN26F

**Copyright**: © 2025 WCN26F

**License**: All rights reserved

---

### 📞 Support

For issues or questions:
- Check printer connection and drivers
- Ensure printer is powered on
- Verify label size matches loaded labels
- Test with default printer if Xprinter not found

---

### 🚀 Future Enhancements (Potential)

- Custom QR code prefixes
- Batch printing support
- Label design customization
- Additional printer support
- Save/load admission number lists
- Print preview before printing
- Export QR codes as images
- Multi-language support

---

**Release Date**: January 20, 2026

**Status**: Stable Release
