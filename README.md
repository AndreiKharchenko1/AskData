# AskDataPython

Working template for UI can be found here:
https://andreikharchenko1.github.io/AskData/

This adds the Python/GenAI part of AskData to the Application.

I created a python script that takes a user input, adds a prompt
and sends it to Google's Gemini API (AskData.py).
This is very simple, works in the console and is separate from the web interface.

I then expanded created AskDataDisplay.py to use it with Flask
and add it to the chat web interface that Andrei already created.

to try it, **run AskDataDisplay.py** and it should start on your localhost.

_You may need to create your own API key, I added mine as an .env file, but I don't know if that will still work._

_Also, depending on your python set up, you might need to install
Flask, dotenv, and google-generativeai._

For now, I have only used Gemini, but I build the code 
so that we can easily change the model and try different ones.

We should try to keep the python logic and the webpage
as separated as possible and only have the js of the webpage return the user input and 
display the model's answer.
But the logic itself should be all separate in the python files.

