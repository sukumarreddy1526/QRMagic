# QRMagic+ ✨

**QRMagic+** is an advanced QR Code generator and decoder application built with Streamlit. It allows users to create customizable QR codes with various styling options and decode QR codes to extract information.

## Features

### 🎨 QR Code Generator
- Input text or URLs to encode.
- Customize QR code:
  - **Color** and **background color**.
  - **Error correction level** (Low, Medium, Quartile, High).
- Download the generated QR code as an image file.
- Analyze QR code properties, such as data length and version.

### 🔍 QR Code Decoder
- Upload QR code images in `png`, `jpg`, or `jpeg` formats.
- Decodes data using the [QRServer API](https://goqr.me/).
- Displays decoded data and provides warnings for invalid QR codes.

### User-Friendly Interface
- Built using **Streamlit** with an intuitive UI.
- Interactive customization via a sidebar.
- Adjustable QR code preview size.

### Modern Design
- Includes social links and footer for enhanced presentation.

---

## Installation and Usage

### Prerequisites
- Python 3.8+
- Required Python libraries: `streamlit`, `qrcode`, `Pillow`, `requests`.

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/sukumarreddy1526/QRMagic.git
   cd QRMagic
