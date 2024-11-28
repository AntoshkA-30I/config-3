
# Домашнее задание №3 Вариант 29

## Описание

Данный инструмент командной строки предназначен для преобразования текстовых конфигураций, написанных на учебном конфигурационном языке, в формат XML. Инструмент принимает входной текст из файла, путь к которому задается через ключ командной строки. Если в процессе обработки входного текста возникают синтаксические ошибки, инструмент выдает соответствующие сообщения об ошибках.

## Синтаксис учебного конфигурационного языка

**Однострочные комментарии:**
```
// Это однострочный комментарий
```

**Словари:**
```
struct {
    имя = значение,
    имя = значение,
    имя = значение,
    ...
}
```

**Имена:**
```
[_a-z]+
```

**Значения:**
- Числа
- Словари

**Объявление констант на этапе трансляции:**
```
const имя = значение
```

**Вычисление констант на этапе трансляции:**
```
$[имя]
```



## Сборка и запуск проекта

Чтобы запустить инструмент, используйте следующую команду, указывая путь к вашему входному файлу с текстом на учебном конфигурационном языке: `python emulator.py <config_path>` Где <config_path> — это путь к входному файлу .txt.

## Примеры работы программы

### Конфигурация веб-сервера
**Входные данные:**
```
// Конфигурация веб-сервера
const port = 8080
const max_connections = 100

struct server {
    server_port = $[port]
    connections = $[max_connections]
    struct routes = {
        home = 1     // индекс для главной страницы
        about = 2    // индекс для страницы "О нас"
        contact = 3   // индекс для страницы "Контакты"
    }
}
```
**Выходные данные (XML):**
```xml
<?xml version="1.0" ?>
<root>
  <port>8080</port>
  <max_connections>100</max_connections>
  <server>
    <server_port>8080</server_port>
    <connections>100</connections>
    <routes>
      <home>1</home>
      <about>2</about>
      <contact>3</contact>
    </routes>
  </server>
</root>
```

### Конфигурация базы данных
**Входные данные:**
```
// Конфигурация базы данных
const db_port = 5432
const max_connections = 50

struct database {
    port = $[db_port]
    connections = $[max_connections]
    timeout = 30 // время ожидания в секундах
    retries = 3    // количество попыток подключения
}
```
**Выходные данные (XML):**
```xml
<?xml version="1.0" ?>
<root>
  <db_port>5432</db_port>
  <max_connections>50</max_connections>
  <database>
    <port>5432</port>
    <connections>50</connections>
    <timeout>30</timeout>
    <retries>3</retries>
  </database>
</root>
```

### Конфигурация приложения
**Входные данные:**
```
// Конфигурация приложения
const max_users = 1000
const version_number = 1 // версия приложения

struct application {
    users = $[max_users]
    version = $[version_number]
    struct features = {
        logging_level = 2 // уровень логирования (1 - низкий, 2 - средний, 3 - высокий)
        maintenance_mode = 0 // 0 - отключен, 1 - включен
    }
}
```
**Выходные данные (XML):**
```xml
<?xml version="1.0" ?>
<root>
  <max_users>1000</max_users>
  <version_number>1</version_number>
  <application>
    <users>1000</users>
    <version>1</version>
    <features>
      <logging_level>2</logging_level>
      <maintenance_mode>0</maintenance_mode>
    </features>
  </application>
</root>
```

## Результаты тестирования
В процессе тестирования были созданы как обычные тесты, так и тесты на проверку ошибок. Все тесты прошли успешно, что подтверждает корректность работы инструмента и его устойчивость к различным сценариям использования. <br />
![](https://github.com/AntoshkA-30I/config-3/blob/main/images/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202024-11-29%20014408.png)
