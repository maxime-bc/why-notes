# No SQL Project

Subject [here](https://docs.google.com/spreadsheets/d/1K-9E6TljJhk7_0Cj3HICfgp03owfm7NNh_-ooE0LL28/edit#gid=0).

commands to run:
```
docker build -t postgresql-v1 .
docker run --name db postgresql-v1
docker exec -it db psql -U docker
```
