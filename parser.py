import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import sys
import re


class DataParser:
    # Инициализация
    def __init__(self):
        self.data = {}  # Словарь для хранения имен и значений
        self.constants = {}  # Словарь для хранения констант

    # Функция преобразования синтаксиса учебного языка в словарь
    def parse_data(self, lines):
        stack = [self.data]

        for line in lines:
            line = line.strip()

        #--- Комментарий
            if '//' in line:
                line = line.split('//', 1)[0].strip()

        #--- Пустая строка
            if not line:
                continue

        #--- Объявление словаря
            if line.startswith('struct ') and (line.endswith('{') or line.endswith('= {')):
                current_dict = {}
                name = line[7:-1].strip()  # Извлекаем имя словаря, начиная с 8-го символа
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
                        name = name[6:]  # Извлекаем имя 
                    if not re.match(r'^[a-z_]+$', name):
                        raise ValueError(f"Ошибка: имя константы {name} содержит недопустимые символы.")

        #--- Вычисление константы
                    if value.startswith('$[') and value.endswith(']'):
                        ref_name = value[2:-1]  # Извлекаем имя константы
                        if ref_name in self.constants:
                            self.constants[name] = self.constants[ref_name]  # Присваиваем значение из другой константы
                            stack[-1][name] = self.constants[name]  # Добавление константы в stack
                        else:
                            raise ValueError(f"Ошибка: Константа {ref_name} не найдена")
        #--- Объявление константы
                    else:
                            # Проверка на существование константы
                        if name in self.constants:
                            raise ValueError(f"Ошибка: Константа {name} уже объявлена.")
                        try:
                            self.constants[name] = int(value.strip())
                            stack[-1][name] = self.constants[name]  # Добавление константы в stack
                        except ValueError:
                            raise ValueError(f"Ошибка: значение для {name} не является числом.")

                else:
                    raise ValueError(f"Ошибка, строка: {line} ")

        return self.data


    # Функция создания XML-элементов
    def dict_to_xml(self, data, root):
        for key, value in data.items():
            if isinstance(value, dict):
                sub_element = ET.SubElement(root, key)
                self.dict_to_xml(value, sub_element)
            else:
                sub_element = ET.SubElement(root, key)
                sub_element.text = str(value)


    # Функция форматирования XML
    def format_xml(self, element):
        rough_string = ET.tostring(element, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")



if __name__ == "__main__":
    parser = DataParser()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("config_path", help="Введите путь до вашего файла", type=str)
    args = arg_parser.parse_args()
    
    # Чтение данных из файла
    with open(args.config_path, "r", encoding='utf-8') as file:
        lines = file.readlines()

    # Парсинг данных
    try:
        data = parser.parse_data(lines)
    except Exception as e:
        print(e)
        sys.exit()

    # Создание корневого элемента
    root = ET.Element('root')
    parser.dict_to_xml(data, root)

    # Вывод данных
    pretty_xml = parser.format_xml(root)
    print(pretty_xml)


