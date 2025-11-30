
<img width="2560" height="1440" alt="Palendar (2)" src="https://github.com/user-attachments/assets/76086aff-10bd-4083-877d-90c79fa091f0" />

# Palendar
An AI-powered calendar, designed to be accessible, easy to understand and use, and simple to integrate into your daily life. Our goal is to help those who may struggle to plan events or remember things and get them back on the right track without making it hard, technologically demanding, or expensive. Originally a submission for the 2025 Congressional App Challenge, we plan to keep working on our project for the foreseeable future.

### <a src="https://www.youtube.com/watch?v=hclkkxjP2ZM">Congressional App Challenge Video (be wary of voicecracks)</a>

# WARNING!!

**While the AI functionality requires an API key, it is currently replaced with a placeholder for security concerns. We should have a working backend by the beginning of next year, although that's not guaranteed.**

## Features

* Event creation and editing
* AI planning assistant
* Notepad 
* *in testing, theoretically works* Daily event reminders

## Future planned features

* A functioning backend to handle the AI responses instead of running everything in the frontend
* Proper testing for daily reminders
* State management for the AI that *actually works*
* More customization features, such as event colors and themes

## Release Timeline (take with a grain of salt, it's an estimate)

### Beta Version

* V 0.1 (Current Version)
* V 0.2 (Backend implementation)
* V 0.6 (JS migration(Currently In Pyscript)) ✅ (I already did this for fun - Haoyan)
* V 1.0 (Redesign ??? and Stable Release)

### Stable Version Coming Soon!

The version of Palendar we made for the Congressional App Challenge was originally just a local build. We tried hosting it online via Github Pages, but not having a good understanding of backend programming and hosting led to us having to take it down (because we accidentally leaked our api key...shhhhhh). At the moment, you can still access it <a src="haohaohaoyan.github.io/Palendar">here</a> but it is lacking the AI-based functionalities.

### What about keeping it open-sourced?

We plan to eventually separate the actual live build and its open-sourced code, keeping a copy of the files that is cleaned of any secrets and ready for locally hosting on this repo, and using the original that contains stuff we don't want to get leaked to host a usable build. This should be happening within the near future, maybe one to three months from now. We want to keep Palendar accessible and free for users, and open-source for others who may have ran into the same problems we did.

## Open-source modules and libraries used

* Python modules
    * calendar
    * datetime
    * json
    * random
    * ast
* Pyscript
* Bootstrap
* Google Gemini SDK

## Roadblocks in development

* Time constraint (we only found out about the Challenge a month before it was due)
* Limited knowledge and not knowing much about Javascript, requiring using Pyscript to use Python in the browser
* Incompatibility issues with the Gemini SDK
* Nonexistent memory for the AI (State management is kinda finicky!)
* API security in the browser (Currently being fixed and should be done by the end of December 2025)

## Team

* Khush Patel: Project cofounder
* Haoyan Li: Project cofounder & Lead Developer
* Manan Nepal: Video, graphics producer
* Pratham Kurmachalam: Tester

## Feedback 

Please do not hesitate in sending us feedback on user experience, bugs, visuals, or anything in between. It's most convenient with the issues tab on Github.
