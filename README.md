# Reseptisovellus

## Toiminnot

* Käyttäjä pystyy: 
	- luomaan tunnuksen ja kirjautumaan sisään [x]
	- lisäämään, muokkaamaan ja poistamaan reseptejä [x]
	- hakemaan reseptejä [x]
	- tallentamaan reseptejä suosikkeihin [x]
	- kommentoimaan reseptejä [x]
* Sovelluksessa on käyttäjäsivut, josta löytyy lisätyt reseptit sekä tilastoja. [x]

## Asennus

Asenna flask-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:

```
$ flask run
```
