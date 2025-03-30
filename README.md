# Reseptisovellus

## Toiminnot

* Käyttäjä pystyy: 
	- luomaan tunnuksen ja kirjautumaan sisään [x]
	- lisäämään, muokkaamaan ja poistamaan reseptejä [x]
	- hakemaan reseptejä [x]
	- tallentamaan reseptejä suosikkeihin
	- kommentoimaan reseptejä
* Sovelluksessa on käyttäjäsivut, josta löytyy lisätyt reseptit [x]  sekä tilastoja.

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
