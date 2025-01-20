import json
import fitz  # PyMuPDF
import streamlit as st
from PIL import Image
import io

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file using PyMuPDF."""
    try:
        pdf_bytes = pdf_file.read()  # Read file as bytes
        with fitz.open(io.BytesIO(pdf_bytes)) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Failed to read the PDF file: {e}")
        return None

def extract_images_from_pdf(pdf_file):
    """Extracts images from a PDF file and returns them as PIL images."""
    images = []
    try:
        pdf_bytes = pdf_file.read()  # Read file as bytes
        with fitz.open(io.BytesIO(pdf_bytes)) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append(image)
        return images
    except Exception as e:
        st.error(f"Failed to extract images from the PDF: {e}")
        return None

def main():
    st.title("PDF Image and Text Extractor")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            # Display the extracted text
            st.subheader("Extracted Text")
            st.text(pdf_text)

        # Reset the file pointer to the beginning before passing it for image extraction
        uploaded_file.seek(0)

        # Extract images from the uploaded PDF
        images = extract_images_from_pdf(uploaded_file)

        if images:
            st.subheader("Extracted Images")
            for i, image in enumerate(images):
                st.image(image, caption=f"Image {i + 1}", use_column_width=True)

            # Option to download extracted images
            for i, image in enumerate(images):
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='PNG')
                image_bytes.seek(0)
                st.download_button(
                    label=f"Download Image {i + 1} as PNG",
                    data=image_bytes,
                    file_name=f"image_{i + 1}.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()
