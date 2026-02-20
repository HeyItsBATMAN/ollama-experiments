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

# Chat-Interface
chat = lms.Chat("You are a helpful assistant.")

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
