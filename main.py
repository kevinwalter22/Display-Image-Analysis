from openai import OpenAI

client = OpenAI()

# Split the long URL into multiple lines
image_url = (
    "https://healiostrategicsolutions.com/wp-content/uploads/2022/08/evolution"
    "-of-pharma-marketing-the-rise-of-drug-commercials.jpg"
)

# Split the long text prompt into multiple lines
text_prompt_1 = (
    "Using keywords only, what is this pharmaceutical ad about?"
)
# First API call
response_1 = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": text_prompt_1},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
        }
    ],
    max_tokens=300,
    temperature=0.0,
    top_p=0.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

# Extract the relevant part of the output
keywords = response_1.choices[0].message

# Define the second prompt, incorporating the output from the first API call
text_prompt_2 = (
    f"Based on the following keywords and your knowledge: {keywords}, "
    f"what is the company name, and drug name from this advertisement?"
    f"Limit your response to a few words only."

)
# Second API call
response_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": text_prompt_2},
            ],
        }
    ],
    max_tokens=300,
    temperature=0.0,
    top_p=0.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

drug_name = response_1.choices[0].message

text_prompt_3 = (
    f"Based on the following drug name/company name and your knowledge: {drug_name}, "
    f"is this drug for men, women, or both?"
    f"What conditions does the drug treat?"
    f"Limit your response to a few words only."
)
# Second API call
response_3 = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": text_prompt_3},
            ],
        }
    ],
    max_tokens=300,
    temperature=0.0,
    top_p=0.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)
print(response_1.choices[0])
print(response_2.choices[0])
print(response_3.choices[0])

