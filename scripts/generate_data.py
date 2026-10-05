import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCE = ROOT / 'q-vercel-latency.json'
TARGET = ROOT / 'api' / 'data.py'


with SOURCE.open('r', encoding='utf-8') as file:
    data = json.load(file)

with TARGET.open('w', encoding='utf-8') as file:
    file.write('DATA')
    file.write(' = ')
    file.write(repr(data))
    file.write('\n')

print('completed')
