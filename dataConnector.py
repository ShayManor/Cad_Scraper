import json
import os


def convert_step_to_txt(folder_name):
    # Iterate over all files in the given folder
    for filename in os.listdir(folder_name):
        # Check if the file has a .step or .STEP extension
        if filename.endswith('.step') or filename.endswith('.STEP'):
            step_file_path = os.path.join(folder_name, filename)
            with open(step_file_path, 'r') as s:
                print('got here')
                return s.read()


with open('../Data/data.json', 'r') as d:
    data = json.load(d)
with open('../Data/processedData.json', 'r') as p:
    descriptions = json.load(p)

finalData = []
for d in data:
    try:
        final = {
            'name': d['name'],
            'description': d['description'],
            'categories': d['categories'],
            'tags': d['tags'],
            'images': d['images'],
            'zip name': d['zip name'],
            'step name': convert_step_to_txt(os.path.join('/users/shay/Downloads/New_Zips/', d['zip name'])),
            'ai description': descriptions[d['name']]
        }
        finalData.append(final)
    except:
        print('fail')
with open('../Data/consolidatedData.json', 'w') as f:
    f.write(json.dumps(finalData))
