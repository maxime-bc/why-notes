# notes.io

**notes.io** is a website that allows you to write and share notes. It uses **postgresql** and **redis** to store data.

## Set up

In a terminal, execute the following commands :
```bash
git clone git@github.com:maxime-bc/no-sql-project.git
cd no-sql-project
docker-compose up
```

**notes.io** is now running at http://localhost:5000.

## Project structure

This project uses three Docker containers : a **python3** container with a Flask app, a **postgresql** container and a **redis** container.

This project uses a **postgresql** database to backup data from the app and a **redis** database is used as a mean to cache notes to avoid requesting them to the **postgresql** database each time the index page is shown.

When creating, updating or deleting a note, changes are applied to **postgresql** and **redis** databases.

Data stored in both **postgresql** and **redis** databases is persistent.

## Connecting to databases

Connecting to the **postgresql** database :
```bash
docker exec -it postgresql_service psql docker docker
```
List all tables with `SELECT * FROM pg_catalog.pg_tables;`

Connecting to the **redis** database :
```bash
docker exec -it redis_service redis-cli
```
List all keys with `keys *`

## Others

- [Subject](https://docs.google.com/spreadsheets/d/1K-9E6TljJhk7_0Cj3HICfgp03owfm7NNh_-ooE0LL28/edit#gid=0)
