import { GoogleGenAI, Type } from 'https://cdn.jsdelivr.net/npm/@google/genai@1.25.0/+esm'

var response = ""
const current_date = new Date()

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
                "description": "The date of event. Format: 'dDD-MM-YYYY', e.g. 'd05-09-2023'",
            },
            "description": {
                "type": Type.STRING,
                "description": "Description of the event being created, preferably with details and notes. If not provided by user, include some tips or trivia related to the event."
            }
        },
        "required": ["name", "date", "description"]
    }
}

var chat_history = []

export const bot = new GoogleGenAI({
    apiKey: "Put your API key here"
});

function get_events() {
    let event_list = JSON.parse(localStorage.getItem("event_keys").replaceAll("'", '"'))
    var event_return = []
    for (let index = 0; index < event_list.length; index++) {
        const element = event_list[index];
        event_return.push(localStorage.getItem(element))
    };
    return event_return
}

export async function generate(prompt) {
    response = await bot.models.generateContent({
        model: "gemini-2.5-flash",
        contents: prompt,
        config: {
            tools: [{
                functionDeclarations: [create_event_args]
            }],
            systemInstruction: `Current date is d${current_date.toDateString()}. Current events are ${get_events()}. Dates are formatted as "dDD-MM-YYYY", and please reformat appropriately. Do not use markdown text.`
        },
    })
    return
}

export function get_response() {
    return response
}

//literally most horrible notification planning EVER
export const notification = Notification
export async function notification_create() {
    let notif_text = await bot.models.generateContent({
        model: "gemini-2.5-flash",
        contents: "Summarize upcoming events, please",
        config: {
            systemInstruction: `Current date is ${current_date.toDateString()} Current events are ${get_events()}. Avoid using markdown text. If there are events in the next day, include them.`
        }
    })
    var notif = new Notification("Events today (hover to read in full):", {body: notif_text.text})
    return
}

export async function notification_send() {
    //why why why
    var current_date = new Date()
    var nextnotif = new Date(localStorage.getItem("next_notif"))
    if (Notification.permission == "granted" && localStorage.getItem("notification_toggle") == "true") {
        //System: sets expected next time of sending, when it passes, sends notification and ascends by a day
        //gonna do this laterojiojfiojfiojeioj;fioej;feijow;feijow;
        if (current_date.valueOf() >= nextnotif.valueOf()) {
            notification_create()
            nextnotif.setDate(current_date.getDate()+1)
            localStorage.setItem("next_notif", nextnotif)
            }
        }
        setTimeout(notification_send, 1800000)
        //every half hour
    }
//I have literally no clue how to write JS. This thing is written with lots of help from the web. Its only purpose is to be imported by calendar-setup.py to provide access to the Gemini API via Pyodide.
//Horrible programming, I know. However, pydantic is allergic to running google-genai in python, and trying to install pydantic-ai just blows everything up.

notification_send()