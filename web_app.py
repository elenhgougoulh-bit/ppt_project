import streamlit as st
import os
from app import build_presentation  # Εισάγουμε τη συνάρτηση που φτιάξαμε

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="AI PPTX Designer", page_icon="🪄")

st.title("🪄 AI PowerPoint Generator")
st.subheader("Δημιούργησε επαγγελματικές παρουσιάσεις σε δευτερόλεπτα")

# Sidebar για ρυθμίσεις
with st.sidebar:
    st.header("Ρυθμίσεις")
    num_slides = st.slider("Αριθμός Διαφανειών", min_value=3, max_value=15, value=5)
    use_images = st.checkbox("Προσθήκη Εικόνων από Unsplash", value=True)

# Κύριο Interface
topic = st.text_input(
    "Τι θέμα θέλεις να έχει η παρουσίασή σου;",
    placeholder="π.χ. Η ιστορία της Αστρονομίας",
)

if st.button("🚀 Δημιουργία Παρουσίασης"):
    if not topic:
        st.error("Παρακαλώ δώσε ένα θέμα!")
    else:
        with st.spinner("Το AI σκέφτεται και σχεδιάζει την παρουσίασή σου..."):
            try:
                # Καλούμε τη συνάρτηση παραγωγής
                # Σημείωση: Πρέπει η build_presentation να επιστρέφει το όνομα του αρχείου
                filename = build_presentation(topic)

                if filename and os.path.exists(filename):
                    st.success(f"Η παρουσίαση '{topic}' είναι έτοιμη!")

                    # Κουμπί Download
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="📥 Κατέβασε το PPTX",
                            data=file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        )
                else:
                    st.error("Κάτι πήγε στραβά κατά την αποθήκευση του αρχείου.")
            except Exception as e:
                st.error(f"Σφάλμα: {e}")

st.markdown("---")
st.caption("Powered by Gemini 2.5 & Unsplash API")
