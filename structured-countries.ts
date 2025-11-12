import ollama from "ollama";
import { z } from "zod";

enum FormOfGovernment {
  Anarchy = "Anarchy",
  Aristocracy = "Aristocracy",
  Authoritarianism = "Authoritarianism",
  Bureaucracy = "Bureaucracy",
  Capitalism = "Capitalism",
  Confederation = "Confederation",
  ConfessionalState = "Confessional state",
  Colonialism = "Colonialism",
  Communism = "Communism",
  Corporatocracy = "Corporatocracy",
  Democracy = "Democracy",
  Ecclesiocracy = "Ecclesiocracy",
  Electocracy = "Electocracy",
  Ergatocracy = "Ergatocracy",
  Fascism = "Fascism",
  Federalism = "Federalism",
  Feudalism = "Feudalism",
  Geniocracy = "Geniocracy",
  Gerontocracy = "Gerontocracy",
  Imperialism = "Imperialism",
  Kakistocracy = "Kakistocracy",
  Kleptocracy = "Kleptocracy",
  Logocracy = "Logocracy",
  Meritocracy = "Meritocracy",
  MilitaryDictatorship = "Military Dictatorship",
  Monarchy = "Monarchy",
  Oligarchy = "Oligarchy",
  Plutocracy = "Plutocracy",
  Republicanism = "Republicanism",
  Socialism = "Socialism",
  Statism = "Statism",
  Technocracy = "Technocracy",
  Theocracy = "Theocracy",
  Totalitarianism = "Totalitarianism",
  Tribalism = "Tribalism",
}

const Country = z.object({
  country: z.string(),
  capital: z.string(),
  population: z.number(),
  formOfGovernment: z.enum(FormOfGovernment),
});

const CountryList = z.array(Country);

const countries = ["Japan", "Brazil", "Germany", "Australia", "Canada"];

const stream = await ollama.chat({
  model: "granite4:3b-h",
  format: z.toJSONSchema(CountryList),
  stream: true,
  options: {
    temperature: 0.2,
    seed: 0,
  },
  messages: [
    {
      role: "system",
      content: `You are a helpful assistant that provides information about countries. Respond according to the following JSON schema: ${z.toJSONSchema(CountryList)}`,
    },
    {
      role: "user",
      content: `Give me information about the following countries in JSON format: ${countries.join(", ")}.`,
    },
  ],
});

for await (const chunk of stream) {
  if (chunk.message.thinking) {
    process.stdout.write(chunk.message.thinking);
  }
  process.stdout.write(chunk.message.content);
}

process.stdout.write("\n");
