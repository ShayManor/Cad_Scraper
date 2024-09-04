import base64
import json
import os

import requests
from openai import OpenAI

supported_formats = [".c", ".cs", ".cpp", ".doc", ".docx", ".html", ".java", ".json", ".md", ".pdf", ".php", ".pptx",
                     ".py", ".rb", ".tex", ".txt", ".css", ".js", ".sh", ".ts"]
client = OpenAI()
client.api_key = ApiKey
assistant = client.beta.assistants.retrieve(
    assistant_id="asst_xJwJs3BC9IcZfLffHIDfGHuT"
)

with open('../Data/data.json', 'r') as f:
    lines = json.load(f)

downloads_folder = os.path.expanduser('~/Downloads')
folder = os.path.join(downloads_folder, 'New_Zips')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_description(line, folder):
    # get folder Path

    folder_name = line['zip name'].strip().replace('{', '').replace('}', '').replace('"', '')
    folder_path = os.path.join(folder, folder_name)

    # Step 2: Initialize a list to store file references
    attachments = []
    image_descriptions = []

    # Step 3: Check if the folder exists
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if os.path.splitext(filename)[1] in ['.jpeg', '.png', '.jpg']:
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    base64_image = encode_image(file_path)

                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {ApiKey}"
                    }

                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": image_describer_prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 300
                    }

                    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers,
                                             json=payload)
                    try:
                        image_descriptions.append(response.json()['choices'][0]['message']['content'])
                    except:
                        image_descriptions.append('')

        # Loop through each file in the folder
        for filename in os.listdir(folder_path):
            if os.path.splitext(filename)[1] in supported_formats:
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):  # Ensure it's a file
                    with open(file_path, 'rb') as file:
                        # Upload the file and store the reference
                        message_file = client.files.create(file=file, purpose="assistants")
                        # assistant.model_validate(message_file)
                        attachments.append({"file_id": message_file.id, "tools": [{"type": "file_search"}]})
        # Step 4: Generate the prompt from the line data
        prompt = (
            f"Model Name: {line['name']}\n"
            f"Description: {line['description']}\n"
            f"Categories: {', '.join(line['categories'])}\n"
            f"Tags: {', '.join(line['tags'])}"
            f"Image descriptions: {', '.join(str(image_descriptions))}"
        )
        # Step 5: Create and run the assistant thread
        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": prompt, "attachments": attachments}]
        )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=run.thread_id)
            ai_response = messages.data[0].content[0].text.value
            return ai_response
    else:
        return f"Folder {folder_name} not found."


# print(get_description(lines[0], folder))

data = {}
i = 0
for line in lines:
    i += 1
    data[line['name']] = get_description(line, folder)
    print(line['name'] + ' ' + str(i))
print(data)

# You are a describer designed to intake the name of a CAD model, a short unclear description, a list of one-word categories and tags, and the CAD files, and write a description of the model which is accurate and detailed. Your primary goal is to create a detailed prompt description that accurately describes the model. You should focus on being precise and concise, using numbers to describe sizes and specific details. You must avoid repeating words or phrases and aim to provide a description in 3-8 sentences. If brevity is required, prioritize accuracy over length. Write the description in paragraph form, similar to if you were describing the cad to a blind person. Don't talk about the uses of the cad file, rather describe it to the best of your abilities. What the model does is not relevant; rather, what pieces are located where, specific details about size, location, etc., are more important. Write everything in one paragraph with no headers, and do not reference me or these instructions in your response. Do not reference the user, just write the long paragraph with extreme detail.
