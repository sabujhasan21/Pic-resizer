import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="Image Tool", layout="centered")

st.title("🖼️ Image Tool (Resize + Compress + Pixel Info)")

# ==============================
# 🔹 Upload multiple images
# ==============================
uploaded_files = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

# ==============================
# 🔹 Resize Settings
# ==============================
st.subheader("📏 Resize Settings")
col1, col2 = st.columns(2)

with col1:
    width = st.number_input("Width", min_value=1, value=800)

with col2:
    height = st.number_input("Height", min_value=1, value=600)

# ==============================
# 🔹 Compression Settings
# ==============================
st.subheader("🗜️ Compression Settings")
quality = st.slider("Image Quality (Lower = More Compression)", 10, 100, 80)

# ==============================
# 🔹 Process Images
# ==============================
if uploaded_files:
    st.write(f"✅ {len(uploaded_files)} images uploaded")

    if st.button("🚀 Process Images"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a") as zip_file:
            for file in uploaded_files:
                try:
                    img = Image.open(file)

                    # Resize image
                    resized_img = img.resize((width, height))

                    img_bytes = io.BytesIO()

                    # Compression logic
                    if file.type == "image/png":
                        resized_img.save(img_bytes, format="PNG", optimize=True)
                    else:
                        resized_img = resized_img.convert("RGB")
                        resized_img.save(
                            img_bytes,
                            format="JPEG",
                            quality=quality,
                            optimize=True
                        )

                    zip_file.writestr(file.name, img_bytes.getvalue())

                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {e}")

        zip_buffer.seek(0)

        st.success("✅ All images processed successfully!")

        st.download_button(
            label="📥 Download All Images (ZIP)",
            data=zip_buffer,
            file_name="processed_images.zip",
            mime="application/zip"
        )

# ==============================
# 🔥 Pixel Size Checker
# ==============================
st.divider()
st.subheader("🔍 Check Image Pixel Size")

single_file = st.file_uploader(
    "Upload a single image",
    type=["jpg", "jpeg", "png", "webp"],
    key="single_image"
)

if single_file:
    try:
        img = Image.open(single_file)
        w, h = img.size

        st.image(img, caption="Uploaded Image", use_column_width=True)
        st.success(f"📐 Image Size: {w} × {h} pixels")

    except Exception as e:
        st.error(f"❌ Error: {e}")
