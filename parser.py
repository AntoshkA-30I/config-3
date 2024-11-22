import xml.etree.ElementTree as ET
from xml.dom import minidom


# Функция преобразования синтаксиса учебного языка в XML
def parse_data(lines):
    data = {}
    stack = [data]
    constants = {}  # Словарь для хранения констант

    for line in lines:
        line = line.strip()

    #--- Комментарий
        if '//' in line:
            line = line.split('//', 1)[0].strip()

    #--- Пустая строка
        if not line:
            continue

    #--- Объявление словаря
        if line.endswith('{') or line.endswith('= {'):
            current_dict = {}
            name = line[:-1].strip()  # Извлекаем имя словаря
            if name.endswith('='):
                name = name[:-1].strip()  # Убираем '='
            stack[-1][name] = current_dict  # Добавляем словарь в родительский
            stack.append(current_dict)

        elif line == '}':
            stack.pop()

        else:
            if '=' in line:
                name, value = map(str.strip, line.split('=', 1))

                if name.startswith('const '):
                    const_name = name[6:]  # Извлекаем имя константы
    #--- Вычисление константы
                    if value.startswith('$[') and value.endswith(']'):
                        ref_name = value[2:-1]  # Извлекаем имя константы
                        if ref_name in constants:
                            constants[const_name] = constants[ref_name]  # Присваиваем значение из другой константы
                            stack[-1][const_name] = constants[const_name]  # Добавление константы в stack
                        else:
                            print(f"Ошибка: Константа {ref_name} не найдена")
                            continue  # Пропускаем добавление в словарь
    #--- Обьявление константы
                    else:
                        try:
                            constants[const_name] = int(value.strip())
                            stack[-1][const_name] = constants[const_name]  # Добавление константы в stack
                        except ValueError:
                            print(f"Ошибка: значение для {name} не является числом.")

                else:
                    stack[-1][name] = value
            else:
                print(f"Warning: строка не содержит '=', пропускаем: {line}")

    return data


# Функция создания XML-элементов
def dict_to_xml(data, root):
    for key, value in data.items():
        if isinstance(value, dict):
            sub_element = ET.SubElement(root, key)
            dict_to_xml(value, sub_element)
        else:
            sub_element = ET.SubElement(root, key)
            sub_element.text = str(value)


# Функция форматирования XML
def format_xml(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")





# Чтение данных из файла
with open('C:/Users/anton/Desktop/config-3/config.txt', "r") as file:
    lines = file.readlines()

# Парсинг данных
data = parse_data(lines)

# Создание корневого элемента
root = ET.Element('root')
dict_to_xml(data, root)

# Вывод данных
pretty_xml = format_xml(root)
print(pretty_xml)
