import xml.etree.ElementTree as ET


def parse_data(lines):
    data = {}
    stack = [data]
    
    for line in lines:
        line = line.strip()
        
        # Удаляем комментарии, если они есть в конце строки
        if '//' in line:
            line = line.split('//', 1)[0].strip()
        
        # Игнорируем пустые строки
        if not line:
            continue
        
        if line.startswith('struct'):
            current_dict = {}
            stack[-1][line.split()[1]] = current_dict  # Имя структуры
            stack.append(current_dict)
        elif line == '}':
            stack.pop()
        else:
            # Проверяем, есть ли символ '=' в строке
            if '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                if 'struct' in value:  # Если значение - это структура
                    value = {}
                else:
                    value = value.strip().strip('"')  # Убираем кавычки
                stack[-1][key] = value
            else:
                print(f"Warning: строка не содержит '=', пропускаем: {line}")
    
    print(data)
    return data


def dict_to_xml(data, root):
    for key, value in data.items():
        if isinstance(value, dict):
            sub_element = ET.SubElement(root, key)
            dict_to_xml(value, sub_element)
        else:
            sub_element = ET.SubElement(root, key)
            sub_element.text = str(value)

# Чтение данных из файла
with open('C:/Users/anton/Desktop/config-3/config.txt', "r") as file:
    lines = file.readlines()

# Парсинг данных
data = parse_data(lines)

# Создание корневого элемента
root = ET.Element("root")
dict_to_xml(data, root)

# Запись в XML файл
tree = ET.ElementTree(root)
    #xml_string = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    #print(xml_string)
tree.write('C:/Users/anton/Desktop/config-3/config.xml', encoding='utf-8', xml_declaration=True)
