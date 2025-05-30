## Запуск реализован как описано в тз, однако также добавлен обязательный флаг --output с вариантами json и console
### Пример запуска с json:
#### Linux
```shell
python3 main.py test_data\data1.csv test_data\data2.csv test_data\data3.csv --report payout --output json
```
#### Win
```shell
python main.py test_data\data1.csv test_data\data2.csv test_data\data3.csv --report payout --output json
```
### Результат:
![json_output](json_output.png)
### и т.д.
### Пример запуска с console:
#### Linux
```shell
python3 main.py test_data\data1.csv test_data\data2.csv test_data\data3.csv --report payout --output console
```
#### Win
```shell
python main.py test_data\data1.csv test_data\data2.csv test_data\data3.csv --report payout --output console
```
### Результат:
![console_output](console_output.png)
## Как добавить новый отчет?
### Добавить его с описанием получаемых с ним колонок в файле settings.py в словарь REPORT_CONFIGS
### В формате с названием как ключ, которое потом как аргумент при запуске передаем и самим конфигом в значении. [Пример с отчетом payout уже есть в настройках](https://github.com/jmblx/test-task/src/settings.py)