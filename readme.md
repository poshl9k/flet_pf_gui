Запакован в exe с помощью pyinstaller
    pip install pyinstaller
    или 
    pip install -r .\requirements.txt


Создать spec файл:
    pyi-makespec --onefile --name pfsense_cam_control pfsense_gui.py


В файл spec был добавлен код для копирования конфиг файла, в целом он не сильно нужен, так как создается в случае отсутствия

# КОД
```
import shutil

shutil.copyfile('config.json', '{0}/config.json'.format(DISTPATH))
```
Запаковка:
    pyinstaller --clean .\pfsense_cam_control.spec

    готовый .exe и конфигурационный файл будут в папке ./dist

Настройка чеерз файл конфигурации:
    Это обычный файл .json
    !Все значения должны быть в кавычках!
    Структура:\
        {\
        "address": "192.168.0.1",\
        "login": "admin",\
        "password": "123Pa$$word!",\
        "rule-desc": "home to VM-cisco-mgmt"\
        }\
    address - IP адрес\
    login - Логин от роутера\
    password - Пароль от роутера\
    rule-desc - описание правила на роутере\

    Про описание:
        Если правило одно - рекомендую писать точно, копируя описание из правила на роутере
        Если правил больше, то привети их описания к очень близкому описанию, отличному от других
        Логика фильтрации правил такова, что она ищет часть или целую строку описания
        Например:
            на роутере есть 2 правила ->
            "fuu bar camera-control"
            "baz bar camera-control"
        #Если поле "rule-desc" будет "camera-control",
        #То оба правила будут отфильтрованы 
        #Если же поле "rule-desc" будет "fuu bar",
        #То под фильтр попадет лишь одно правило -> "fuu bar camera-control"


        

