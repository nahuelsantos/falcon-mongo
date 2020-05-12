# Falcon - Mongo

#### Disclaimer
The following application is just an example on running a [Falcon API](https://falcon.readthedocs.io/en/stable/) with [MongoDB](https://www.mongodb.com/) in Docker containers. This application does not have any security or authentication (yet). **Use it at your own risk**.

#### Description

This application creates and runs 3 docker containers:
* Falcon API running on port 9009. Gunicorn serves as web server.
* Mongo database running in default port 27017
* Mongo Express web based mongo client running on port 8081

To run the API just run

```sh
docker-compose up --build
```

Once the Gunicorn is up and running, you can test that everything is ok going to 
```html
http://localhost:9009/ping
```
#### Postman
In postman folder you can get a Postman collection with examples to test the API

##### List all existing players
To get a list of all existing players, do a **GET** request to
```html    
http://localhost:9009/players
```
**Pay attention to the lack of trailing slash**

##### Get an specific player
To get a player, do a **GET** request to
```html 
http://localhost:9009/players/{_id}
```
##### Create a new player
To create a new Player do a **POST** request to
```html 
http://localhost:9009/players
```
    
Example JSON body

```json
{
    "username": "BestPlayer",
    "email": "bestplayer@personalemail.com",
    "first_name": "Anibal",
    "last_name": "Fernandez",
    "phone": "+0118796353",
    "date_of_birth": "1984-02-29 10:10:10",
    "gender": "M"
}
```

##### Create a edit an existing player
To create a new Player do a **PATCH** request to
```html
http://localhost:9009/players/{_id}
```
    
Example JSON

```json
{
    "first_name": "Cristina",
    "last_name": "Fernández",
    "phone": "+0118796353",
    "date_of_birth": "1953-02-19 10:10:10",
    "gender": "F"
}
```

##### Delete an existing player
To delete an existing player, do a **DELETE** request to
```html 
http://localhost:9009/players/{_id}
```
    
#### Troubleshooting

##### Solving standard_init_linux error
If you run this in a Windows environment and you get this error:
```sh
standard_init_linux.go:211: exec user process caused "no such file or directory"
```
you may need to set up your git to run the follwing script in order to avoid git to rewrite the End of Lines in the files.
```sh
git config core.eol lf
git config core.autocrlf input
```

Or you can set it up globally 
```sh
git config --global core.eol lf
git config --global core.autocrlf input
```

##### If you get an error while trying to start the backend container like:
```sh
ERROR: for backend  Cannot create container for service backend: status code not OK but 500: {"Message":"Unhandled exception: Drive has not been shared"}
```
If you are in Windows, you need to enable file sharing between your host and the container by going right click in Docker's icon in system tray and Settings > Resources > File Sharing