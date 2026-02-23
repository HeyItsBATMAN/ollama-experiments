import csv
import os
import re
import unicodedata

import lmstudio as lms
from lmstudio.json_api import AnyPrediction

import util
from schema import MetadataSchema

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
        # Tipp: Wir können Modellen auch das gesamte Schema geben
        f"The metadata should be extracted according to the following schema:\n\n{MetadataSchema.model_json_schema()}."
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
    # Hier speichern wir die extrahierten Metadaten in einer Liste,
    # die später in eine CSV-Datei geschrieben wird.
    csv_results = [
        [
            "issue_date",
            "classification",
            "language",
            "places",
            "signature",
            "summary",
        ]
    ]
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

        # Validierung der Metadaten gegen das erwartete Schema (siehe schema.py)
        try:
            metadata_object = MetadataSchema.model_validate_json(str(metadata))
            # Wenn wir die Metadaten erfolgreich extrahieren konnten,
            # können wir sie in die CSV-Ergebnisliste aufnehmen.
            print("Metadata validation successful.")
            csv_results.append(
                [
                    metadata_object.issue_date,
                    metadata_object.classification,
                    metadata_object.language,
                    ", ".join(metadata_object.places),
                    metadata_object.signature,
                    metadata_object.summary,
                ]
            )

        except Exception as e:
            print("\nMetadata validation failed:", str(e))

        if is_last_page:
            print("\nReached the end of the document.")
            break

    name_without_ext = os.path.splitext(selected_filename)[0]
    normalized = unicodedata.normalize("NFKD", name_without_ext)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^\w\s-]", "", ascii_name).strip().lower()
    slug = re.sub(r"[-\s]+", "-", slug)
    csv_filename = f"{slug}.csv"

    if os.path.exists(csv_filename):
        os.remove(csv_filename)

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerows(csv_results)
