
import json

path = r'C:/Users/Javier/.gemini/antigravity/brain/fccf5445-47e7-43fc-938d-dd9bfe34ae29/.system_generated/logs/transcript.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    capture = False
    count = 0
    for line in f:
        data = json.loads(line)
        content = data.get('content', '')
        if 'me sale error y es un problema' in content:
            capture = True
        if capture:
            print('--- ' + str(data.get('type')) + ' ---')
            print(content[:500])
            count += 1
            if count > 5:
                break
