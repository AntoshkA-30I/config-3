import unittest
import parser
import xml.etree.ElementTree as ET

class TestDataParser(unittest.TestCase):
    def setUp(self):
        self.test_parser = parser.DataParser()

    def test_successful_parsing(self):
        test1 = ['struct application {',
                 '    max_users = 10',
                 '    version = 1',
                 '}']
        output = self.run_test(test1)
        expected_output = b'<root><application><max_users>10</max_users><version>1</version></application></root>'
        self.assertEqual(output, expected_output)

        test2 = [
            '// Конфигурация приложения',
            'const max_users = 1000',
            '',
            'struct application {',
            '    users = $[max_users]',
            '    struct features = {',
            '        logging_level = 2 // уровень логирования (1 - низкий, 2 - средний, 3 - высокий)',
            '    }',
            '}']
        output = self.run_test(test2)
        expected_output = b'<root><application><users>1000</users><features><logging_level>2</logging_level></features></application><max_users>1000</max_users></root>'
        self.assertEqual(output, expected_output)

    def test_error_handling(self):
        error_tests = [
            (['/ Конфигурация приложения'], 'Ошибка, строка: / Конфигурация приложения '),
            (['const max_users  1000'], 'Ошибка, строка: const max_users  1000 '),
            (['cost max_users = 1000'], 'Ошибка: имя константы cost max_users содержит недопустимые символы.'),
            (['const max_users = qwerty'], 'Ошибка: значение для max_users не является числом.'),
            (['struct application ', '    const max_users = 10', '    const version = 1', '}'], 'Ошибка, строка: struct application '),
            (['const max_users = 100', 'const users = $[min_users]'], 'Ошибка: Константа min_users не найдена'),
            (['const max_users = 100', 'const max_users = 150'], 'Ошибка: Константа max_users уже объявлена.')
        ]

        for input_data, expected_output in error_tests:
            output = self.run_test(input_data)
            self.assertEqual(output, expected_output)

    def run_test(self, input):
        self.test_parser.constants = {}  # Очищаем словарь констант
        try:
            data = self.test_parser.parse_data(input)
        except Exception as e:
            return str(e)

        root = ET.Element('root')
        self.test_parser.dict_to_xml(data, root)
        output = ET.tostring(root, 'utf-8')
        return output

if __name__ == '__main__':
    unittest.main()
