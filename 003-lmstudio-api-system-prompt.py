import lmstudio as lms

import util

# Wir interagieren über die LMStudio API, um LMStudio zu befehlen, ein Modell zu laden.
# Vorher lassen wir uns anzeigen, welche Modelle wir heruntergeladen zu haben, um die gültigen Modellnamen zu kennen.
util.print_available_models()

# Modell laden
print("Loading model...")
model = lms.llm(
    "olmo-2-0425-1b-instruct",
    # "olmo-3-7b-instruct",
    config={
        "seed": 42,
    },
)
util.print_loaded_models()

# Frage: wie können wir den System Prompt nutzen, um die Antworten des Modells zu steuern?
# Aufgabe:
# - System Prompt so verändern, dass das Modell nur 1 Wort als Antwort gibt.
# - System Prompt so verändern, dass das Modell auf Deutsch antwortet.
# Mehrere Anweisungen können anneinander gehängt werden
chat = lms.Chat(
    "You are a helpful assistant. Lorem Ipsum dolor sit amet. Der Himmel ist blau. ",
)

chat.add_user_message("What is the capital of Austria?")

# Antwort generiern aus der bisherigen Konversation (System Prompt + User Message)
response = model.respond(
    chat,
    config={
        "temperature": 0.0,
    },
)

chat.add_assistant_response(response)

print(response.content)

chat.add_user_message("What is the capital of Germany?")

response = model.respond(
    chat,
    config={
        "temperature": 0.0,
    },
)

print(response.content)
