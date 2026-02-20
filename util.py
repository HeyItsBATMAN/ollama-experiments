from typing import List, Tuple

from pypdf import PdfReader


def get_pdf_page_count(pdf_path: str) -> int:
    """Returns the number of pages in a given PDF file."""
    reader = PdfReader(pdf_path)
    return len(reader.pages)


def extract_text_from_pdf(pdf_path: str, page: int) -> Tuple[str, bool]:
    """Extracts all text from a given PDF file."""
    reader = PdfReader(pdf_path)
    is_last_page = page == len(reader.pages) - 1
    return (reader.pages[page].extract_text(), is_last_page)


def user_choice(prompt: str, options: List[str]) -> int:
    """Prompts the user to select an option from a list."""
    while True:
        try:
            choice = int(input(f"\n{prompt}\n"))
            if 0 <= choice < len(options):
                return choice
            else:
                print(f"Please enter a number between 0 and {len(options) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def print_available_models():
    """Prints the list of available models."""
    import lmstudio as lms

    print("\nAvailable models:")
    for downloaded_model in lms.list_downloaded_models():
        print(f"{downloaded_model.model_key}")


def print_loaded_models():
    """Prints the list of loaded models."""
    import lmstudio as lms

    print(
        f"\nLoaded models: {', '.join([x.identifier for x in lms.list_loaded_models()])}"
    )


def extract_json_from_response(response: str) -> str:
    """Extracts JSON content from a model response, if it is enclosed in a code block."""
    if "```json" in response:
        start_index = response.index("```json")
        if "```" in response[start_index + len("```json") :]:
            end_index = response.index("```", start_index + len("```json"))
            json_content = response[start_index + len("```json") : end_index].strip()
            return json_content

    return response
