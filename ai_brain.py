import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Φορτώνουμε τα κλειδιά από το .env
load_dotenv()

# Αρχικοποιούμε τον ΝΕΟ client της Google
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_presentation_json(topic, num_slides=5):
    print(f"Σκέφτομαι το περιεχόμενο για: '{topic}'...")

    # Το prompt μας
    prompt = f"""
    Είσαι ένας expert δημιουργός επαγγελματικών παρουσιάσεων.
    Ο χρήστης σου ζητάει να δημιουργήσεις μια παρουσίαση με θέμα: "{topic}" και μέγεθος {num_slides} διαφάνειες.
    
    Οι διαθέσιμοι τύποι layout (layout_num) που πρέπει να χρησιμοποιήσεις είναι:
    - 0: Title Slide (Απαιτεί 'title' και 'subtitle')
    - 2: Title and Content (Απαιτεί 'title' και 'content')
    - 7: Section Header (Απαιτεί 'title' και 'content')
    - 40: Quote (Απαιτεί 'title' ως όνομα συγγραφέα και 'content' ως το απόφθεγμα)
    
    Το JSON πρέπει να περιέχει ένα array που λέγεται "slides".
    Κάθε αντικείμενο στο array πρέπει να έχει το "layout" (αριθμό) και τα αντίστοιχα πεδία κειμένου.
    Το content (όπου υπάρχει) να έχει bullets (•) αν είναι λίστα.
    """

    try:
        # Χρησιμοποιούμε το νέο SDK και ζητάμε εγγυημένο JSON (application/json)
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Χρησιμοποιούμε το πιο σύγχρονο μοντέλο
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", temperature=0.7
            ),
        )

        # Εφόσον ζητήσαμε JSON, το response.text είναι ήδη έγκυρο JSON
        presentation_data = json.loads(response.text)

        return presentation_data.get("slides", [])

    except Exception as e:
        print(f"Υπήρξε σφάλμα με το νέο AI API: {e}")
        return None


# Δοκιμάζουμε αν δουλεύει αυτόνομα
if __name__ == "__main__":
    test_topic = "Το Μέλλον της Τηλεργασίας"
    slides_json = generate_presentation_json(test_topic)

    if slides_json:
        print("\nΕπιτυχία! Το AI απάντησε με το εξής JSON:\n")
        print(json.dumps(slides_json, indent=2, ensure_ascii=False))
