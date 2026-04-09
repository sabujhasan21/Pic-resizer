import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

st.set_page_config(page_title="Image Tool", layout="centered")

st.title("🖼️ Image Tool (Resize + Crop + Compress + Pixel Info)")

# ==============================
# 🔹 Upload multiple images
# ==============================
uploaded_files = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

# ==============================
# 🔹 Mode Selection
# ==============================
st.subheader("⚙️ Select Mode")
mode = st.radio("Choose Processing Type:", ["Resize", "Crop"])

# ==============================
# 🔹 Size Input
# ==============================
st.subheader("📏 Size Settings")
col1, col2 = st.columns(2)

with col1:
    width = st.number_input("Width", min_value=1, value=800)

with col2:
    height = st.number_input("Height", min_value=1, value=600)

# ==============================
# 🔹 Compression
# ==============================
st.subheader("🗜️ Compression Settings")
quality = st.slider("Image Quality", 10, 100, 80)

# ==============================
# 🔹 Preview (Crop Only)
# ==============================
if uploaded_files and mode == "Crop":
    st.subheader("👀 Crop Preview (First Image)")

    try:
        preview_img = Image.open(uploaded_files[0])
        cropped_preview = ImageOps.fit(preview_img, (width, height))

        col1, col2 = st.columns(2)
        with col1:
            st.image(preview_img, caption="Original")
        with col2:
            st.image(cropped_preview, caption="Cropped Preview")

    except Exception as e:
        st.error(f"Preview error: {e}")

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

                    # 👉 Resize or Crop
                    if mode == "Resize":
                        processed_img = img.resize((width, height))
                    else:
                        processed_img = ImageOps.fit(img, (width, height))

                    img_bytes = io.BytesIO()

                    # 👉 Compression
                    if file.type == "image/png":
                        processed_img.save(img_bytes, format="PNG", optimize=True)
                    else:
                        processed_img = processed_img.convert("RGB")
                        processed_img.save(
                            img_bytes,
                            format="JPEG",
                            quality=quality,
                            optimize=True
                        )

                    zip_file.writestr(file.name, img_bytes.getvalue())

                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {e}")

        zip_buffer.seek(0)

        st.success("✅ Done!")

        st.download_button(
            label="📥 Download ZIP",
            data=zip_buffer,
            file_name="processed_images.zip",
            mime="application/zip"
        )

# ==============================
# 🔍 Pixel Size Checker
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
