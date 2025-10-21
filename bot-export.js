import { GoogleGenAI, Type } from 'https://cdn.jsdelivr.net/npm/@google/genai@1.25.0/+esm'
export const bot = new GoogleGenAI({
    apiKey: 'AIzaSyCNUX7mhETUC1lQgoK14J_OQSB10oXvnsI'
    });

export const types = Type;
//I have literally no clue how to write JS. This is mostly copied off of the Gemini SDK docs. Its only purpose is to be imported by calendar-setup.py to provide access to the Gemini API via Pyodide.
//Horrible programming, I know. However, pydantic is allergic to running google-genai in python, and trying to install pydantic just blows everything up.