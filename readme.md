# GUI Сделан с помощью flet  
https://flet.dev/  

Запакован в exe с помощью flet pack  
    pip install flet  
    или  
    pip install -r .\requirements.txt  

# Установка пакета на pfsense  

__для установки читать раздел Installation(https://github.com/jaredhendrickson13/pfsense-api#installation)__    



#   Запаковка:
```powershell
flet pack --icon .\icon.ico -n pfsense_cam_control .\pfsense_gui.py --product-name "pfsense_cam_control" --product-version "0.7" --file-version "0.7" --file-description "Pfsense camera control" --copyright "https://github.com/poshl9k"
```
    готовый .exe и конфигурационный файл будут в папке ./dist

Настройка чеерз файл конфигурации config.json:  
    Это обычный файл .json  
#    !Все значения должны быть в кавычках!  
#    Структура:
```json
{
"address": "192.168.0.1",
"login": "admin",
"password": "123Pa$$word!",
"rule-desc": "home to VM-cisco-mgmt"
}
```
__address - IP адрес__  
__login - Логин от роутера__  
__password - Пароль от роутера__  
__rule-desc - Описание правила на роутере__  

# Про описание:
    Если правило одно - рекомендую писать точно, копируя описание из правила на роутере
    Если правил больше, то привеcти их к очень близкому описанию, отличному от других
    Логика фильтрации правил такова, что она ищет часть или целую строку описания
    Например:
        на роутере есть 2 правила ->
        "fuu bar camera-control"
        "baz bar camera-control"
    Если поле "rule-desc" будет "camera-control",
    То оба правила будут отфильтрованы 
    Если же поле "rule-desc" будет "fuu bar",
    То под фильтр попадет лишь одно правило -> "fuu bar camera-control"


        

