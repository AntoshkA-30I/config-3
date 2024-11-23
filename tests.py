import parser
import xml.etree.ElementTree as ET


def test(input):
    test_parser.constants = {} # Очищаем словарь констант
    try:
        data = test_parser.parse_data(input)
    except Exception as e:
        output = e
        return str(output)
    
    root = ET.Element('root')
    test_parser.dict_to_xml(data, root)
    output = ET.tostring(root, 'utf-8')
    return output


#--------tests input--------#
error_test1 = ['/ Конфигурация приложения']

error_test2 = ['const max_users  1000']

error_test3 = ['cost max_users = 1000']

error_test4 = ['const max_users = qwerty']

error_test5 = ['application ',
    '    const max_users = 10',
    '    const version = 1',
    '}']

error_test6 = ['const max_users = 100',
               'const users = $[min_users]']

error_test7 = ['const max_users = 100',
               'const max_users = 150']

test1 = ['application {',
    '    const max_users = 10',
    '    const version = 1',
    '}']

test2 = [
    '// Конфигурация приложения',
    'const max_users = 1000',
    ''
    'application {',
    '    const users = $[max_users]',
    '    features = {',
    '        const logging_level = 2 // уровень логирования (1 - низкий, 2 - средний, 3 - высокий)',
    '    }',
    '}']
#--------tests input--------#


test_parser = parser.DataParser()

output = test(test1)
assert output == b'<root><application><max_users>10</max_users><version>1</version></application></root>'
output = test(test2)
assert output == b'<root><application><users>1000</users><features><logging_level>2</logging_level></features></application><max_users>1000</max_users></root>'
output = test(error_test1)
assert output == 'Ошибка, строка: / Конфигурация приложения '
output = test(error_test2)
assert output == 'Ошибка, строка: const max_users  1000 '
output = test(error_test3)
assert output == 'Ошибка: не указан тип для переменной cost max_users.'
output = test(error_test4)
assert output == 'Ошибка: значение для const max_users не является числом.'
output = test(error_test5)
assert output == 'Ошибка, строка: application '
output = test(error_test6)
assert output == 'Ошибка: Константа min_users не найдена'
output = test(error_test7)
assert output == 'Ошибка: Константа max_users уже объявлена.'

print('OK')