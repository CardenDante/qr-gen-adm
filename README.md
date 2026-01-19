# QR Code Label Printer

<div align="center">
  <img src="Profile.png" alt="QR Label Printer" width="200"/>

  **Professional QR Code Label Generator for Thermal Printers**

  [![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
  [![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

---

## 📋 Overview

A modern, professional desktop application for generating and printing QR code labels directly to thermal printers. Specifically optimized for the **Xprinter 470B** thermal label printer.

## ✨ Features

- 🎨 **Modern Professional UI** - Clean, intuitive interface built with CustomTkinter
- 📱 **Live QR Preview** - See your QR code before printing
- 🖨️ **Direct Thermal Printing** - One-click printing to Xprinter 470B
- 📏 **Multiple Label Sizes** - Support for 5 common label dimensions
- 🎯 **Automatic Formatting** - Labels include "WCN26F-" prefix with admission number
- ⚡ **Fast & Efficient** - Instant QR generation and printing
- 🔒 **Monochrome Optimization** - Perfect black & white output for thermal printers

## 📦 Download

**[Download Latest Release](https://github.com/yourusername/qr-label-printer/releases/latest)**

Download `QR_Label_Printer.exe` and run - no installation required!

## 🎯 Supported Label Sizes

- 60 x 40 mm *(default)*
- 50 x 30 mm
- 40 x 30 mm
- 50 x 25 mm
- 70 x 40 mm

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)

1. Download `QR_Label_Printer.exe` from the releases page
2. Double-click to run
3. Enter admission number (e.g., `4433`)
4. Click "Generate QR Code"
5. Review the preview
6. Click "Print Label"

### Option 2: Run from Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qr-label-printer.git
   cd qr-label-printer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Building from Source

To create your own executable:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   build.bat
   ```

3. Find the executable in `dist/QR_Label_Printer.exe`

## 🖨️ Printer Setup

### Supported Printers
- **Primary**: Xprinter 470B (203 DPI)
- **Compatible**: Most thermal label printers with Windows drivers

### Setup Instructions

1. Install Xprinter 470B drivers from manufacturer
2. Set printer as default (optional - app will auto-detect)
3. Load appropriate label size (60x40mm recommended)
4. Run the application

## 📱 How It Works

### QR Code Data
- **You type**: `4433`
- **QR encodes**: `4433` (pure data)
- **Label displays**:
  - QR Code with `4433`
  - Text: `WCN26F-` (small) + `4433` (large)

### Label Layout
```
┌────────────────────────┐
│┌────────┐              │
││        │  WCN26F-     │
││   QR   │              │
││  CODE  │   4433       │
││        │              │
│└────────┘              │
└────────────────────────┘
```

## 🛠️ Technical Specifications

- **Platform**: Windows 10/11
- **Python Version**: 3.8+
- **Printer DPI**: 203 (optimized for thermal printers)
- **QR Error Correction**: High (Level H)
- **Image Format**: Monochrome (1-bit) for optimal thermal printing

## 📚 Dependencies

```
customtkinter==5.2.2
qrcode[pil]==7.4.2
Pillow==10.4.0
pywin32==306
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**WCN26F**
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- QR Code generation by [python-qrcode](https://github.com/lincolnloop/python-qrcode)
- Printer integration using [pywin32](https://github.com/mhammond/pywin32)

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/yourusername/qr-label-printer/issues)
- Check [Documentation](https://github.com/yourusername/qr-label-printer/wiki)

---

<div align="center">
  Made with ❤️ by WCN26F © 2025

  **[⬆ back to top](#qr-code-label-printer)**
</div>
