# Display-Image-Analysis
Proof of concept application for display image analysis using OpenAI APIs. Completed as an intern project for Audiencelogy LLC. Languages used are Python and HTML. The application takes an ad image and uses OpenAI API services via request to analyze the image. main.py (local application) file uses hardcoded image URL and prompts to send chained requests to the LLM. The output from the first request is combined with the prompt from the second request. Similarly, the output from the second request is combined with the third prompt for the third request. app.py (web application) also uses chained requests to the LLM in a similar manner, except the prompts are input from the web application while it is running. The setup to run each file independently can be found below. 

# OpenAI services setup
1. Create an account with OpenAI
2. Keep track of your API key (you will need it later when setting up the files)
3. Familiarize yourself with the developer quickstart guide (optional)
  - https://platform.openai.com/docs/quickstart
    
# main.py setup
1. Install Python if it's not already installed
2. Run the following commands in command prompt to set up a virtual environment (windows commands). If you have Unix or MacOS follow this guide: https://platform.openai.com/docs/quickstart 
  - python -m venv openai-env
  - openai-env\Scripts\activate
  - pip install --upgrade openai
  - setx OPENAI_API_KEY "your-api-key-here"
3. Run the file in your IDE of choice

# app.py setup
1. Install Python if it's not already installed
2. Run the following commands in command prompt to set up a virtual environment (windows commands). If you have Unix or MacOS follow this guide: https://platform.openai.com/docs/quickstart 
  - python -m venv openai-env
  - openai-env\Scripts\activate
  - pip install --upgrade openai
  - setx OPENAI_API_KEY "your-api-key-here"
3. Install Flask using the following command
  - pip install Flask
4. Install the rules package for Python with the following command
  - pip install rules
5. Run the web application using the below command
  - python app.py
