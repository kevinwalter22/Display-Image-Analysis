from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional

app = Flask(__name__)
client = OpenAI()

OpenAI.api_key = 'your API key here'

class PromptData(BaseModel):
    image_url: str
    num_prompts: int
    prompt1_text: Optional[str] = Field(None, description="Text for Prompt 1")
    prompt2_text: Optional[str] = Field(None, description="Text for Prompt 2")
    prompt3_text: Optional[str] = Field(None, description="Text for Prompt 3")

@app.route('/')
def home():
    form_html = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Analyze Ad</title>
    </head>
    <body>
        <h1>Analyze Ad</h1>
        <form action="/analyze_ad" method="post">
            <label for="image_url">Image URL:</label>
            <input type="text" id="image_url" name="image_url" required><br><br>

            <label for="num_prompts">Number of Prompts:</label>
            <select id="num_prompts" name="num_prompts" required onchange="showPrompts(this.value)">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select><br><br>

            <div id="prompt1_section">
                <label for="prompt1_text">Prompt 1:</label>
                <select id="prompt1_select" name="prompt1_select" onchange="updatePromptDisplay(this, 'default_prompt1', 'custom_prompt1')">
                    <option value="">--Select or Enter Prompt 1--</option>
                    <option value="Default Prompt 1">Default Prompt 1</option>
                    <option value="Custom">Custom</option>
                </select><br><br>
                <p id="default_prompt1" style="display:none;">What are the keywords from this pharma ad?</p>
                <div id="custom_prompt1" style="display:none;">
                    <input type="text" id="custom_prompt1_text" name="custom_prompt1_text" placeholder="Enter your prompt 1 text">
                </div>
            </div>

            <div id="prompt2_section" style="display:none;">
                <label for="prompt2_text">Prompt 2:</label>
                <select id="prompt2_select" name="prompt2_select" onchange="updatePromptDisplay(this, 'default_prompt2', 'custom_prompt2')">
                    <option value="">--Select or Enter Prompt 2--</option>
                    <option value="Default Prompt 2">Default Prompt 2</option>
                    <option value="Custom">Custom</option>
                </select><br><br>
                <p id="default_prompt2" style="display:none;">Based on these keywords and your knowledge, 
                what is the company name and drug name?.</p>
                <div id="custom_prompt2" style="display:none;">
                    <input type="text" id="custom_prompt2_text" name="custom_prompt2_text" placeholder="Enter your prompt 2 text">
                </div>
            </div>

            <div id="prompt3_section" style="display:none;">
                <label for="prompt3_text">Prompt 3:</label>
                <select id="prompt3_select" name="prompt3_select" onchange="updatePromptDisplay(this, 'default_prompt3', 'custom_prompt3')">
                    <option value="">--Select or Enter Prompt 3--</option>
                    <option value="Default Prompt 3">Default Prompt 3</option>
                    <option value="Custom">Custom</option>
                </select><br><br>
                <p id="default_prompt3" style="display:none;">Based on the company name, drug name, and your knowledge, 
                is this drug for men, women, or both? What conditions does the drug treat?.</p>
                <div id="custom_prompt3" style="display:none;">
                    <input type="text" id="custom_prompt3_text" name="custom_prompt3_text" placeholder="Enter your prompt 3 text">
                </div>
            </div>

            <button type="submit">Submit</button>

            <script>
                function showPrompts(value) {
                    document.getElementById('prompt1_section').style.display = value >= 1 ? 'block' : 'none';
                    document.getElementById('prompt2_section').style.display = value >= 2 ? 'block' : 'none';
                    document.getElementById('prompt3_section').style.display = value >= 3 ? 'block' : 'none';
                }

                function updatePromptDisplay(selectElement, defaultId, customId) {
                    const defaultPara = document.getElementById(defaultId);
                    const customDiv = document.getElementById(customId);

                    if (selectElement.value.startsWith('Default')) {
                        defaultPara.style.display = 'block';
                        customDiv.style.display = 'none';
                    } else if (selectElement.value === 'Custom') {
                        defaultPara.style.display = 'none';
                        customDiv.style.display = 'block';
                    } else {
                        defaultPara.style.display = 'none';
                        customDiv.style.display = 'none';
                    }
                }

                document.getElementById('prompt1_select').addEventListener('change', function() {
                    updatePromptDisplay(this, 'default_prompt1', 'custom_prompt1');
                });

                document.getElementById('prompt2_select').addEventListener('change', function() {
                    updatePromptDisplay(this, 'default_prompt2', 'custom_prompt2');
                });

                document.getElementById('prompt3_select').addEventListener('change', function() {
                    updatePromptDisplay(this, 'default_prompt3', 'custom_prompt3');
                });
            </script>
        </form>
    </body>
    </html>
    '''
    return render_template_string(form_html)

@app.route('/analyze_ad', methods=['POST'])
def analyze_ad():
    data = request.form

    image_url = data.get('image_url')
    num_prompts = int(data.get('num_prompts'))

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    default_prompts = {
        'Default Prompt 1': 'What are the keywords from this pharma ad?',
        'Default Prompt 2': 'Based on these keywords and your knowledge,'
                            'what is the company name and drug name?',
        'Default Prompt 3': 'Based on the company name, drug name, and your knowledge,'
                            'is this drug for men, women, or both? What conditions does the drug treat?'
    }

    def get_prompt_text(prompt_key, custom_key):
        prompt_text = data.get(prompt_key)
        if prompt_text == 'Custom':
            prompt_text = data.get(custom_key)
        elif prompt_text in default_prompts:
            prompt_text = default_prompts[prompt_text]
        return prompt_text

    prompt1_text = get_prompt_text('prompt1_select', 'custom_prompt1_text')
    prompt2_text = get_prompt_text('prompt2_select', 'custom_prompt2_text')
    prompt3_text = get_prompt_text('prompt3_select', 'custom_prompt3_text')

    class PromptConditions(BaseModel):
        prompt1: Optional[str]
        prompt2: Optional[str]
        prompt3: Optional[str]

    prompt_conditions = PromptConditions(
        prompt1=prompt1_text,
        prompt2=prompt2_text,
        prompt3=prompt3_text
    )

    responses = {}

    def call_openai(prompt_text, image_url):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=300,
            temperature=0.0,
            top_p=0.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].message.to_dict()

    def call_openai_text(prompt_text):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                    ],
                }
            ],
            max_tokens=300,
            temperature=0.0,
            top_p=0.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].message.to_dict()

    if prompt_conditions.prompt1:
        response1 = call_openai(prompt_conditions.prompt1 + ' in a few words only', image_url)
        responses['prompt1'] = response1

    if prompt_conditions.prompt2:
        response1_str = str(response1)
        prompt2_text = prompt_conditions.prompt2 + response1_str + ' in a few words only'
        response2 = call_openai_text(prompt2_text)
        responses['prompt2'] = response2

    if prompt_conditions.prompt3:
        response2_str = str(response2)
        prompt3_text = prompt_conditions.prompt3 + response2_str + ' in a few words only'
        response3 = call_openai_text(prompt3_text)
        responses['prompt3'] = response3

    return jsonify(responses)


if __name__ == '__main__':
    app.run(debug=True)





