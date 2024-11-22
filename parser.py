import xml.etree.ElementTree as ET
from xml.dom import minidom


# Функция преобразования синтаксиса учебного языка в XML
def parse_data(lines):
    data = {}
    stack = [data]
    constants = {}  # Инициализация словаря для хранения констант

    for line in lines:
        line = line.strip()

        #--- Комментарий
        if '//' in line:
            line = line.split('//', 1)[0].strip()

        #--- Пустая строка
        if not line:
            continue

        #--- Словарь
        if line.startswith('struct'):
            current_dict = {}
            stack[-1][line.split()[1]] = current_dict  # Имя словаря
            stack.append(current_dict)

        elif line == '}':
            stack.pop()

        else:
            if '=' in line:
                name, value = map(str.strip, line.split('=', 1))

                #--- Объявление константы
                if name.startswith('const '):
                    if value.startswith('$[') and value.endswith(']'):
                        # Обработка случая, когда константа зависит от другой константы
                        const_name = value[2:-1]  # Извлекаем имя константы
                        if const_name in constants:
                            constants[name[6:]] = constants[const_name]  # Присваиваем значение из другой константы
                            stack[-1][name[6:]] = constants[name[6:]]  # Добавление константы в stack
                        else:
                            print(f"Ошибка: Константа {const_name} не найдена")
                            continue  # Пропускаем добавление в словарь
                    else:
                        try:
                            constants[name[6:]] = int(value.strip())
                            stack[-1][name[6:]] = constants[name[6:]]  # Добавление константы в stack
                        except ValueError:
                            print(f"Ошибка: значение для {name} не является числом.")
                
                else:
                    #--- Вычисление константы
                    if value.startswith('$[') and value.endswith(']'):
                        const_name = value[2:-1]  # Извлекаем имя константы
                        if const_name in constants:
                            value = constants[const_name]
                        else:
                            print(f"Ошибка: Константа {const_name} не найдена")
                            continue  # Пропускаем добавление в словарь
                    else:
                        try:
                            value = int(value.strip())
                        except ValueError:
                            print(f"Ошибка: значение для {name} не является числом.")
                            continue  # Пропускаем добавление в словарь

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




constants = {} # Словарь для хранения констант

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
