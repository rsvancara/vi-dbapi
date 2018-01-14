# Visual Intrigue Database API

This is the database api for the Visual Intrigue code base.  The goal of this sub project is to 
abstract the details of database calls away from the main application.  Although the admin
interface still has strong dependencies on the databse.  For now this only works with the front-end code
base.

## Front Page Service

Get the list of items to display on the front page image rotator.  Gives a random
list of images

/dbapi/api/v1.0/frontpageservice/<size>

## Front page 

Get the list of items to display in the conntiuous scroll

/dbapi/api/v1.0/frontpage

##Front Page (Paginated List)

Older API for getting a paginated list of items for disply 

/dbapi/api/v1.1/getfrontpage/<page>

## Get the List of Articles

Get a list of articles

/dbapi/api/v1.0/listarticles

## Get an article

Get an single article by id

/dbapi/api/v1.0/article/<id>

## List all the portfolios

Get a list of portfolios

/dbapi/api/v1.0/listportfolios/<portfolio>

## Get a Story

Get a single story

/dbapi/api/v1.0/getstory/<id>

## Get a photo

/dbapi/api/v1.0/getphoto/<id>

# Test the API

Returns status=success if it works

/dbapi/api/v1.0/test

# Test your API key

Returns status=success if it works

/dbapi/api/v1.0/testkey/<key>

