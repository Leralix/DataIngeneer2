# Projet Data Engineering 2 
### Présentation du projet
Notre projet de data engineering 2 porte sur la conception de la partie Back-end d'un aggrégateur RSS. 
Pour ce projet, nous nous sommes basés sur Apache Kafka et Apache Cassandra. 
Le projet s'articule autour de 3 objectifs majeurs : 
- La récupération des articles via des web scrappers 
- Le traitement et le stockage de ces articles via Kafka et Cassandra
- Le déploiement de ces articles via Flask

### User Guide
Comment lancer l'application Flask ?
##### Cloner le projet
Pour pouvoir accéder à notre projet, il faut pouvoir cloner l'original accessible depuis git.
Lancer un terminal gitbash (windows) dans le répertoite où vous allez stocker le projet.
Ecrire les instructions suivantes:
> git clone https://github.com/Leralix/DataIngeneer2.git

##### Déployer le projet

Pour déployer le projet, il faut avoir installé les packages nécessaires au lancement de l'application Flask. 
Pour cela, lancer la commande suivante dans un terminal : 
> pip install - r requirements.txt

Après avoir installé les différents packages, lancer la commande suivante (Docker Desktop doit être installé sur le pc) dans vs code ou un terminal: 
> docker compose up

Lancer dans un autre terminal :
> python flask_page.py

Puis lancer dans un autre terminal : 
> python LeMonde.py

Enfin, connectez vous à l'adresse suivante :
> http://127.0.0.1:3000/articles?user_id=1

Vous pouvez désormais visualiser l'application.
