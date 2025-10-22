import { GoogleGenAI, Type } from 'https://cdn.jsdelivr.net/npm/@google/genai@1.25.0/+esm'

var response = "wow empty"

var create_event_args = {
    "name": "event_create",
    "description": "Creates a single-day calendar event with name and description and saves it to localstorage.",
    "parameters": {
        "type": Type.OBJECT,
        "properties": {
            "name": {
                "type": Type.STRING,
                "description": "Name of the event being created."
            },
            "date": {
                "type": Type.STRING,
                "description": "Date of event. Format: 'dDD-MM-YYYY', e.g. 'd05-09-2023'",
            },
            "description": {
                "type": Type.STRING,
                "description": "Description of the event being created. "
            }
        },
        "required": ["name", "date", "description"]
    }
}

export const bot = new GoogleGenAI({
    apiKey: 'AIzaSyCNUX7mhETUC1lQgoK14J_OQSB10oXvnsI'
    });

export async function generate(prompt) {
    response = await bot.models.generateContent({
        model: "gemini-2.5-flash",
        contents: prompt,
        config: {
            tools: [{
                functionDeclarations: [create_event_args]
            }]
        },
    })
}

export function get_response() {
    return response
}
//I have literally no clue how to write JS. This thing is written with lots of help from the web. Its only purpose is to be imported by calendar-setup.py to provide access to the Gemini API via Pyodide.
//Horrible programming, I know. However, pydantic is allergic to running google-genai in python, and trying to install pydantic just blows everything up.