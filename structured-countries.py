from enum import Enum
from typing import List

import ollama
from pydantic import BaseModel, RootModel


class FormOfGovernment(str, Enum):
    ANARCHY = "Anarchy"
    ARISTOCRACY = "Aristocracy"
    AUTHORITARIANISM = "Authoritarianism"
    BUREAUCRACY = "Bureaucracy"
    CAPITALISM = "Capitalism"
    CONFEDERATION = "Confederation"
    CONFESSIONAL_STATE = "Confessional state"
    COLONIALISM = "Colonialism"
    COMMUNISM = "Communism"
    CORPORATOCRACY = "Corporatocracy"
    DEMOCRACY = "Democracy"
    ECCLESIOCRACY = "Ecclesiocracy"
    ELECTOCRACY = "Electocracy"
    ERGATOCRACY = "Ergatocracy"
    FASCISM = "Fascism"
    FEDERALISM = "Federalism"
    FEUDALISM = "Feudalism"
    GENIOCRACY = "Geniocracy"
    GERONTOCRACY = "Gerontocracy"
    IMPERIALISM = "Imperialism"
    KAKISTOCRACY = "Kakistocracy"
    KLEPTOCRACY = "Kleptocracy"
    LOGOCRACY = "Logocracy"
    MERITOCRACY = "Meritocracy"
    MILITARY_DICTATORSHIP = "Military Dictatorship"
    MONARCHY = "Monarchy"
    OLIGARCHY = "Oligarchy"
    PLUTOCRACY = "Plutocracy"
    REPUBLICANISM = "Republicanism"
    SOCIALISM = "Socialism"
    STATISM = "Statism"
    TECHNOCRACY = "Technocracy"
    THEOCRACY = "Theocracy"
    TOTALITARIANISM = "Totalitarianism"
    TRIBALISM = "Tribalism"


class Country(BaseModel):
    country: str
    capital: str
    population: int
    formOfGovernment: FormOfGovernment


class CountryList(RootModel):
    root: List[Country]


countries = ["Japan", "Brazil", "Germany", "Australia", "Canada"]

stream = ollama.chat(
    model="granite4:350m",
    format=CountryList.model_json_schema(),
    stream=True,
    options={
        "temperature": 0.2,
        "seed": 0,
    },
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful assistant that provides information about countries. Respond according to the following JSON schema: {CountryList.model_json_schema()}",
        },
        {
            "role": "user",
            "content": f"Give me information about the following countries in JSON format: {', '.join(countries)}.",
        },
    ],
)

message = ""

for chunk in stream:
    if hasattr(chunk["message"], "thinking") and chunk["message"].get("thinking"):
        print(chunk["message"]["thinking"], end="", flush=True)
    message += chunk["message"]["content"]
    print(chunk["message"]["content"], end="", flush=True)

print()  # Final newline
with open("structured-countries-output.json", "w") as f:
    f.write(message)
