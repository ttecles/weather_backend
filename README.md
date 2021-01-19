
# Backend connector
We would like to ask you for a test for this position! It should be a small agile project.
The target is that you do this task and show it to the development team. This will help us understand what you can bring to OneMind. This will also help you get to know the team and how we work!
We also want to be able to review and discuss your code, so it would be nice if you could share your most representative repository in Github with us.

# Exercise
We need to take data from an external API to obtain climatological data for a geoarea (chosen by you). Once these data are collected, we will save them in a database, any technology can be used to save that information. In turn, once the data is stored, the project must have a service (or several) exposed so that the Frontend can consume them. This Rest API to mount must be built with docker and developed with Python, a framework such as Flask or similar could be used to facilitate development.
It is very important that this project should have unit tests. You have total freedom to use libraries of your choice, but we would like to know why the selected ones have been used.

# Features
* Data from external API: https://api.tutiempo.net/json.html (You can use other Open API if wanted)
* Data saved on a DB
* API Rest that shows the data saved on the DB, filtered by city
* Project runs on Docker
* Python 3 and unit tests is a must

# Preparing environment files
Set .env file:

```dotenv
FLASK_APP=weather.py
FLASK_CONFIG=docker
SECRET_KEY=5a8as84c6a5s84as6sd8a3c2a
WEATHER_API_KEY=zwDX4azaz4X4Xqs
WEATHER_LOCATIONS=3200,3201,3202,3203,3204,3205,3206,3207,3208
DATABASE_URL=mysql+pymysql://weather:onemind@db/weather
```

Set .env-mysql 
```dotenv
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_DATABASE=weather
MYSQL_USER=weather
MYSQL_PASSWORD=<database-password>
```

Once done, run docker
```shell
docker-compose up -d --build
```

Endpoint | Description | Methods
--- | --- | --- 
/api/v1/localities | List of all available localities | GET
/api/v1/daily/locality/<locality-id> | 15-Daily Forecast on locality-id | GET
/api/v1/hourly/locality/<locality-id> | 7-Day Hourly Forecast on locality-id | GET