# Reseptisovellus

## Toiminnot

* Käyttäjä pystyy: 
	- luomaan tunnuksen ja kirjautumaan sisään
	- lisäämään, muokkaamaan ja poistamaan reseptejä
	- hakemaan reseptejä
	- tallentamaan reseptejä suosikkeihin
	- kommentoimaan reseptejä
* Sovelluksessa on käyttäjäsivut, josta löytyy lisätyt reseptit sekä tilastoja.

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
