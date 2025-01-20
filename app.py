import json
import re
from PyPDF2 import PdfReader, errors
import streamlit as st

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file with error handling."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except errors.PdfReadError:
        st.error("Failed to read the PDF file. It may be corrupted or unsupported.")
        return None

def extract_recommendations(pdf_text):
    """Extracts recommendations, COR, and LOE from the PDF text."""
    recommendations = []
    
    # Regex patterns for COR and LOE
    cor_pattern = r"(?i)Class of Recommendation\s*:\s*(COR\s*[A-C1-3]*)"
    loe_pattern = r"(?i)Level of Evidence\s*:\s*(LOE\s*[A-C1-3]*)"
    recommendation_pattern = r"(?i)Recommendation\s*:\s*(.*?)\n"

    cor_matches = re.findall(cor_pattern, pdf_text)
    loe_matches = re.findall(loe_pattern, pdf_text)
    recommendation_matches = re.findall(recommendation_pattern, pdf_text)

    for cor, loe, rec in zip(cor_matches, loe_matches, recommendation_matches):
        recommendations.append({
            "title": "Distal Radius Fracture Rehabilitation",
            "subCategory": [],
            "recommendation_content": rec.strip(),
            "guide_title": "Distal Radius Fracture Rehabilitation",
            "rating": loe.strip(),
            "stage": [
                "Rehabilitation",
                cor.strip()
            ],
            "disease": [
                "Fracture"
            ],
            "rationales": [],
            "references": [],
            "specialty": [
                "orthopedics"
            ]
        })

    return recommendations

def main():
    st.title("PDF Recommendation Extractor")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            # Extract recommendations
            recommendations = extract_recommendations(pdf_text)

            # Display recommendations
            st.subheader("Extracted Recommendations")
            st.json(recommendations)

            # Option to download JSON
            recommendations_json = json.dumps(recommendations, indent=4)
            st.download_button(
                label="Download Recommendations as JSON",
                data=recommendations_json,
                file_name="recommendations.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
