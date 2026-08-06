Середовище було налаштоване WSL на Ubuntu 24.04.
```bash
wsl --install -d Ubuntu-24.04
```

оновив всі системні пакети, python і суміжні пакети вже встановлені на Убунті
```bash
sudo apt update
sudo apt upgrade -y
```
Рухаючись по документації https://www.odoo.com/documentation/19.0/administration/on_premise/source.html

## 1. Зклонував репозиторій
```bash
   git clone --branch 19.0 --single-branch https://github.com/odoo/odoo.git
```
## 2. Встановив Postgres
```bash
  sudo apt install postgresql postgresql-client
```
## 3. Створив та активував віртуальне середовище
```bash
  cd ~/test-task/odoo
  python3 -m venv .venv
```
  Стикнувся з помилкою, через відсутність python3.12-venv пакетів
  ```bash
  source .venv/bin/activate
  ```
## 4. Встановлення Python залежностей
```bash
  pip install -r requirements.txt
```
  Стикнувся з помилкою
  <img width="998" height="437" alt="Знімок екрана 2026-08-04 231523" src="https://github.com/user-attachments/assets/7d68708d-9f12-41c5-8e9d-d72cba8cd181" />
  Через відсутність системних залежностей, вирішено їх встановленням
  ```bash
   sudo apt install -y build-essential python3-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev
```
## 5. Створення користувача та самої БД
  Створив користувача PostgreSQL:
  ```bash
  sudo -u postgres createuser -d -R -S test
```
  Початкову базу даних створив командою:
  ```bash
  sudo -u postgres createdb test
```
  Робочу базу test-task пізніше створив через менеджер баз даних Odoo
## 6. Запуск Odoo
Створив конфігураційний файл odoo.conf, з *addons_path = /home/test/test-task/odoo/addon* - пізніше доданий також шлях для власного модуля */home/test/test-task/custom-addons*
```bash
  [options]
  admin_passwd = qwerty
  
  db_user = test
  
  addons_path = /home/test/test-task/odoo/addons
  
  http_interface = 127.0.0.1
  http_port = 8069
  
  log_level = info
```
Запускав командою
```bash
python odoo-bin --addons-path=/home/test/test-task/odoo/addons --config=/home/test/test-task/odoo.conf --database=test
```
Під час першого запуску початкова база даних `test` ще не містила структури Odoo, тому отримав помилку 
<img width="941" height="354" alt="Знімок екрана 2026-08-05 203038" src="https://github.com/user-attachments/assets/e8fa4fa8-5e88-4a9d-9cb2-4582f194830d" />
тому повторно запустив команду з додатковим прапорцем *-i base*


