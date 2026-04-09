import streamlit as st
from PIL import Image
import io
import zipfile

st.title("🖼️ Image Resizer + Compressor")

# 👉 Upload multiple images
uploaded_files = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

# 👉 Resize inputs
st.subheader("📏 Resize Settings")
col1, col2 = st.columns(2)
with col1:
    width = st.number_input("Width", min_value=1, value=800)
with col2:
    height = st.number_input("Height", min_value=1, value=600)

# 👉 Compression slider
st.subheader("🗜️ Compression Settings")
quality = st.slider("Image Quality (Lower = More Compression)", 10, 100, 80)

if uploaded_files:
    st.write(f"✅ {len(uploaded_files)} images uploaded")

    if st.button("Process Images"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a") as zip_file:
            for file in uploaded_files:
                try:
                    img = Image.open(file)

                    # 👉 Resize
                    resized_img = img.resize((width, height))

                    img_bytes = io.BytesIO()

                    # 👉 Handle format
                    if file.type == "image/png":
                        resized_img.save(img_bytes, format="PNG", optimize=True)
                    else:
                        resized_img = resized_img.convert("RGB")  # JPG safe
                        resized_img.save(
                            img_bytes,
                            format="JPEG",
                            quality=quality,
                            optimize=True
                        )

                    zip_file.writestr(file.name, img_bytes.getvalue())

                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")

        zip_buffer.seek(0)

        st.success("✅ Done! Download below 👇")

        st.download_button(
            label="📥 Download ZIP",
            data=zip_buffer,
            file_name="processed_images.zip",
            mime="application/zip"
        )
