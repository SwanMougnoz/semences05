# Semences05

## Installation

Installer les paquets :
`sudo apt-get install python-dev python-pip mysql-server python-mysqldb libmysqlclient-dev libxml2 libxml2-dev libxslt1-dev ruby-full`

Installer nodejs et bower : [https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions]()
`curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -`
`sudo apt-get install -y nodejs`
`sudo npm install -g bower`

En mode dev :
`sudo pip install virtualenv`

Créer une base de donnée mysql :
`mysql> CREATE DATABASE semences05`
`mysql> CREATE USER 'semences05'@'localhost' IDENTIFIED BY 'password'`
`mysql> GRANT ALL PRIVILEGES ON semences05.* TO 'semences05'@'localhost'`

Installer compass : [http://compass-style.org/install/]()
`sudo gem update --system`
`sudo gem install compass`

Charger les dépendances javascript:
`python manage.py bower install`

Les fichiers css ne sont pas commités. Pour les mettres à jour, se déplacer dans le répertoire **frontend/sass** puis :
`compass compile` ou `compass watch`

## Référence make

`env` : Crée l'envirronement python à partir des dépendances dans requirements.txt

`db` : Met à jour la base en appliquant les migrations

`server`: Lance un serveur de dev sur 0.0.0.0:8000

`tests` : Lance les tests