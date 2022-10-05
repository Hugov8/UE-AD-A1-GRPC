# UE-AD-A1-GRPC
Implémentation du TP gRPC. Movie, Booking, Showtime sont des services gRPC. User, qui est le point d'entrée de l'application est un service REST.  
Aucun appel asynchrone n'est effectué.

## Installation
Pour installer et lancer le projet, lancer dans le terminal les lignes de commandes suivantes à la racine du projet :

```bash
#Récupération des dépendances gRPC
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

#Copie des fichiers protos là où c'est nécessaire
./install_proto.sh

#Lancement de l'application via Docker
docker-compose build
docker-compose up
```

Après avoir lancé l'application, l'accès au service User (qui est le point d'entrée de l'application) se fait via le lien http://localhost:3004/


Pour arrêter les services, faites Ctrl+C et entrez les lignes de commandes : 
```bash
docker-compose down
docker images purge
```

## Utilisation des autres services
Les autres services sont accessibles via les ports suivants :
| Service  | Port      | Accès         |
|----------|-----------|---------------|
| User     | 3004  | user:3004     |
| Movie    | 3001  | movie:3001   |
| Booking  | 3003  | booking:3003   |
| Showtime | 3002  | showtime:3002   |

Pour utiliser un des services, il faut copier les fichiers *_pb2.py et *_pb2_grpc.py (avec * le nom du service) dans le répertoire où se situe le script python utilisant le service.
Le script python doit importer ces deux fichiers (par exemple pour movie) : 
```python
import movie_pb2, movie_pb2_grpc
```
La connexion au service se fait par les lignes suivantes :

```python
with grpc.insecure_channel('movie:3001') as channel:
    stub = movie_pb2_grpc.MovieStub(channel)
    # code ici
    channel.close()
```
La récupération des informations et services offerts par l'API se fait via les méthodes de stub. Par exemple, pour récupérer les informations d'un film via son id et afficher son titre : 
```python
with grpc.insecure_channel('movie:3001') as channel:
    stub = movie_pb2_grpc.MovieStub(channel)
    #Code
    movie_details = stub.GetMovieByID(movieID)
    print(movie_details.title)
    #Fermeture de la connexion
    channel.close()
```
Le dossier client permet de tester le bon fonctionnement de toutes les API. Pour l'utiliser, lancer les différents services (cf [partie précédente](#installation)) et lancer le fichier client.py via la commande :
```bash
python3 client/client.py
```

## Documentation
La documentation de l'API est disponible via les fichiers protos ou une documentation Open API dans le cas du service User.  
Les documentations pour les différents servcies sont disponibles dans leur répertoire respectifs :

| Service  | Documentation OpenAPI     |
|----------|---------------------------|
| User     | [Documentation user](user/User-1.0.0.yaml)  |
| Movie    | [Documentation movie](movie/protos/movie.proto)   |
| Booking  | [Documentation booking](booking/protos/booking.proto)   |
| Showtime | [Documentation showtime](showtime/protos/showtime.proto)   |

Les fichiers protos regroupent toutes les méthodes offertes par le service ainsi que la structure des informations renvoyées.

## Authors
- [@Hugov8](https://github.com/Hugov8)
- [@remiCzn](https://github.com/remiCzn) 