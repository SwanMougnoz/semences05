# Semences05

## Installation

Installer les paquets :
`sudo aptitude install python-dev python-mysqldb libmysqlclient-dev`

Configurer django pour utiliser Mysql :
`pip install MySQL-python`

Installer compass : [http://compass-style.org/install/]()

Les fichiers css ne sont pas commités. Pour les mettres à jour, se déplacer dans le répertoire **frontend/sass** puis :
`compass compile` ou `compass watch`

Mettre à jour la base de donnée après une modification :
`make db`

Lancer un serveur de développement :
`make server`

Lancer les tests :
`make tests`