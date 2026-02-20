import os

import lmstudio as lms
from lmstudio.json_api import AnyPrediction

import util

util.print_available_models()

print("Loading model...")
model = lms.llm(
    "olmo-2-0425-1b-instruct",
    # "olmo-3-7b-instruct",
    config={
        "seed": 42,
    },
)
util.print_loaded_models()


def process_document(text: str) -> AnyPrediction:
    chat = lms.Chat(
        f"You are a helpful assistant that extracts metadata from documents. "
        # Frage: Wie könnte man den System Prompt so gestalten,
        # dass das Modell die Ausgabe wie beschrieben in TASK.md generiert?
    )

    chat.add_user_message(f"Here is the text from the document:\n\n{text}")

    # Die Antwort des Modells wird gestreamt, d.h. wir erhalten sie in Fragmenten, während sie generiert wird.
    # Dadurch können wir die Ausgabe in Echtzeit anzeigen, wie üblich in bekannten Chat-Interfaces.
    intermediate_result = ""
    for fragment in model.respond_stream(
        chat,
        config={
            "temperature": 0.0,
        },
    ):
        print(fragment.content, end="", flush=True)
        intermediate_result += fragment.content

    print()

    # Modelle geben häufig strukturierte Antworten in Code-Blöcken zurück
    # Hier extrahieren wir den Inhalt eines JSON-Code-Blocks, falls vorhanden, da die Metadaten in diesem Format erwartet werden.
    modified_result = util.extract_json_from_response(intermediate_result)

    return modified_result


# Hauptprogrammteil:
# Hier listen wir die PDF-Dateien in einem Verzeichnis auf, lassen den Benutzer eine auswählen,
# extrahieren den Text Seite für Seite und verarbeiten ihn mit dem LLM, um die gewünschten Metadaten zu extrahieren.
if __name__ == "__main__":
    pdf_dir = "./pdfs"
    pdf_entries = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    print("\nAvailable PDF Documents:")
    for index, filename in enumerate(pdf_entries):
        count = util.get_pdf_page_count(os.path.join(pdf_dir, filename))
        print(f"[{index}] {filename} ({count} pages)")

    choice = util.user_choice(
        "Select the number of the PDF you want to process:", pdf_entries
    )
    selected_filename = pdf_entries[choice]
    pdf_file_path = os.path.join(pdf_dir, selected_filename)
    print(f"\nYou selected: {selected_filename}")

    print(f"Extracting text from {pdf_file_path}...")

    current_page = 0
    while True:
        page_text, is_last_page = util.extract_text_from_pdf(
            pdf_file_path, current_page
        )
        current_page += 1
        print(len(page_text), "characters extracted.")

        print("Processing page text with LLM...")
        metadata = process_document(page_text)

        print("\n--- Extracted Metadata ---")
        print(metadata)
        if is_last_page:
            print("\nReached the end of the document.")
            break
