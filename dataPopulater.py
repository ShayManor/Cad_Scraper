import json
import jsonlines
import os
import sys

# open('finalData.jsonl', 'w').close()
# print('here')
# with open('finalData.jsonl', 'w') as file:
#     pass
# sys.exit()

# with open('/users/shay/pycharmprojects/CadScraper/Data/finalData.jsonl', 'w') as file:
#     pass

prompt = ('You are a cad creater. Your job is to take a user description and return a .STEP file, perfectly formatted '
          'and completely correct with no bugs that models the users description. Do not invent details, '
          'ensure everything matches the users description and that your code can be run first try.')

with open('/Users/shay/PycharmProjects/CadScraper/Data/consolidatedData.json', 'r') as d:
    data = json.load(d)

message_pre = {
    "messages": [
        {
            "role": "system",
            "content": prompt
        }
    ]
}
with jsonlines.open('/users/shay/pycharmprojects/CadScraper/Data/finalData.jsonl', mode='a') as writer:
    for cad in data:

        try:
            if cad['ai description'] != None and cad['step name'] != None:
                message = {
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": cad['ai description']
                        },
                        {
                            "role": "assistant",
                            "content": cad['step name'],
                        }
                    ]
                }
                writer.write(message)
        except Exception as e:
            print(f"Error processing {cad['name']}: {e}")

# with open('finalData.jsonl', 'a') as f:
#     jsonlines.
#     f.write(message + ']}')
