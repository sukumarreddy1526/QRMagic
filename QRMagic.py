import streamlit as st
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io
import requests
import base64
from PIL import Image

# QR Code Generator with Styling
def generate_qr_code(data, color, bg_color, error_correction):
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color=bg_color).convert("RGB")
    return img

# QR Code Decoder using pyzbar
def decode_qr_code_with_api(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    response = requests.post(
        "https://api.qrserver.com/v1/read-qr-code/",
        files={"file": buffered.getvalue()},
    )
    if response.status_code == 200:
        result = response.json()
        return result[0]["symbol"][0]["data"] if result[0]["symbol"] else "No QR code detected."
    else:
        return "Error decoding QR code."

# QR Code Analyzer
def analyze_qr_code(qr_code_data):
    return {
        "Data Length": len(qr_code_data),
        "Version": "1",
        "Error Correction Level": "Medium",
    }

# Streamlit UI
st.set_page_config(page_title="QRMagic+", page_icon="✨", layout="wide")
st.title("✨ QRMagic+: Advanced QR Code Generator and Decoder")

# Sidebar for customization
st.sidebar.header("Customize Your QR Code")
box_color = st.sidebar.color_picker("Pick QR Code Color", "#000000", help="Choose the color for the QR Code blocks.")
background_color = st.sidebar.color_picker(
    "Pick Background Color", "#FFFFFF", help="Choose the background color for the QR Code."
)

# Error correction level selection
error_correction_mapping = {
    "Low (L)": qrcode.constants.ERROR_CORRECT_L,
    "Medium (M)": qrcode.constants.ERROR_CORRECT_M,
    "Quartile (Q)": qrcode.constants.ERROR_CORRECT_Q,
    "High (H)": qrcode.constants.ERROR_CORRECT_H,
}
error_correction_level = st.sidebar.selectbox(
    "Error Correction Level",
    list(error_correction_mapping.keys()),
    index=1,
    help="Higher error correction levels increase QR Code resilience but reduce data capacity.",
)

# QR Code preview size adjustment
preview_size = st.sidebar.slider(
    "Preview Size (px)", min_value=100, max_value=500, value=250, step=50, help="Adjust the size of the QR Code preview."
)

# Tabbed Interface
tabs = st.tabs([
    "🎨 Generate QR Code",
    "🔍 Decode QR Code",
])

# QR Code Generator Tab
with tabs[0]:
    st.header("🎨 Generate QR Code")
    col1, col2 = st.columns([2, 1])
    with col1:
        text_to_encode = st.text_area("Enter text or URL to encode:", help="Input the data to be encoded in the QR Code.")
        file_name = st.text_input("Enter a file name for the QR Code:", placeholder="Default: QRCode.png")

    with col2:
        st.write("")
        generate_btn = st.button("Generate QR Code")

    if generate_btn:
        if text_to_encode:
            qr_image = generate_qr_code(
                text_to_encode,
                box_color,
                background_color,
                error_correction_mapping[error_correction_level],
            )
            buf = io.BytesIO()
            qr_image.save(buf, format="PNG")
            buf.seek(0)

            # Display QR code with a user-selected width
            st.image(buf, caption="Generated QR Code", width=preview_size)

            # Use default name if none is provided
            download_file_name = f"{file_name or 'QRCode'}.png"
            st.download_button(
                "Download QR Code",
                data=buf,
                file_name=download_file_name,
                mime="image/png",
            )

            # Analyze QR Code
            st.write("QR Code Analysis:")
            st.json(analyze_qr_code(text_to_encode))
        else:
            st.warning("Please enter text or URL to generate a QR code.")

# QR Code Decoder Tab
with tabs[1]:
    st.header("🔍 Decode QR Code")
    uploaded_file = st.file_uploader(
        "Upload a QR Code image", type=["png", "jpg", "jpeg"], help="Upload an image containing a QR Code to decode."
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=preview_size)
        decoded_data = decode_qr_code_with_api(image)
        if isinstance(decoded_data, list):
            st.success("Decoded Data:")
            for i, data in enumerate(decoded_data, 1):
                st.markdown(f"**Data {i}:** {data}")
        else:
            st.warning(decoded_data)

# Footer
st.markdown(
    """
    <hr style="border:1px solid gray;">  
    <p style="text-align:center;">Developed with ❤️ by <a href="https://your-portfolio-link.com" target="_blank">Sukumar</a></p>
    <div style="text-align:center;">
        <a href="https://www.instagram.com/sukumarreddych/" target="_blank" style="margin:0 15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram" style="width:30px;height:30px;">
        </a>
        <a href="https://www.linkedin.com/in/sukumarreddych/" target="_blank" style="margin:0 15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width:30px;height:30px;">
        </a>
        <a href="https://github.com/sukumarreddy1526" target="_blank" style="margin:0 15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" alt="GitHub" style="width:30px;height:30px;">
        </a>
        <a href="mailto:venkatasukumarreddych@gmail.com" target="_blank" style="margin:0 15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email" style="width:30px;height:30px;">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
