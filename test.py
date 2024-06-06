def convert_to_bytes(size_str):
    multipliers = {'GB': 1e9, 'TB': 1e12} 
    size = int(size_str[:-2])
    unit = size_str[-2:]
    return size * multipliers[unit]

def convert_to_str(size_bytes):
    if size_bytes >= 1e12:
        return f"{size_bytes / 1e12:.0f}TB"
    elif size_bytes >= 1e9:
        return f"{size_bytes / 1e9:.0f}GB"

data = {'SSD': ['120GB', '240GB', '480GB', '1TB', '2TB', '4TB'], 'HDD': ['500GB', '1TB', '2TB', '4TB', '8TB']}

# Инициализация минимальных и максимальных значений
min_size = float('inf')
max_size = float('-inf')

# Проходим по всем значениям в словаре
for category, sizes in data.items():
    for size in sizes:
        # Преобразуем размеры в байты
        size_bytes = convert_to_bytes(size)
        
        # Обновляем минимальное и максимальное значения
        min_size = min(min_size, size_bytes)
        max_size = max(max_size, size_bytes)

# Конвертируем минимальное и максимальное значения обратно в строковый формат
min_size_str = convert_to_str(min_size)
max_size_str = convert_to_str(max_size)

# Выводим результаты
print("От", min_size_str, "до", max_size_str)
