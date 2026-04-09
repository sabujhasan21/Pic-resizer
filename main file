import streamlit as st
from PIL import Image
import io
import zipfile

st.title("🖼️ Batch Image Resizer")

# 👉 Upload multiple images
uploaded_files = st.file_uploader(
    "Upload Images", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True
)

# 👉 Size input
col1, col2 = st.columns(2)
with col1:
    width = st.number_input("Width", min_value=1, value=800)
with col2:
    height = st.number_input("Height", min_value=1, value=600)

if uploaded_files:
    st.write(f"✅ {len(uploaded_files)} images uploaded")

    if st.button("Resize Images"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a") as zip_file:
            for file in uploaded_files:
                try:
                    img = Image.open(file)
                    resized_img = img.resize((width, height))

                    img_bytes = io.BytesIO()
                    resized_img.save(img_bytes, format="PNG")
                    
                    zip_file.writestr(file.name, img_bytes.getvalue())

                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")

        zip_buffer.seek(0)

        st.download_button(
            label="📥 Download All Resized Images (ZIP)",
            data=zip_buffer,
            file_name="resized_images.zip",
            mime="application/zip"
        )
