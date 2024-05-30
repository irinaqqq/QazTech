import json

# Открываем файл с явным указанием кодировки (UTF-16)
with open('QazTech\dump2.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

# Записываем данные в новый файл с кодировкой UTF-8
with open('QazTech\dump2_utf8.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)