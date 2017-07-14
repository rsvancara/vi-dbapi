#!/usr/bin/python
from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo
from dbapi import siteconfig
import pymongo
import logging
from datetime import datetime
from dbapi import util
import random

app = Flask(__name__)
app.config['MONGO_URI'] = siteconfig.MONGO_URI

mongo = PyMongo(app)

logger = logging.getLogger('app')

@app.route('/dbapi/api/v1.0/frontpageservice/<size>', methods=['GET'])
def frontpageservice(size):
    """ Returns a JSON String of the images included in the
        frontpage image rotation.  The order of the list is
        randomized
    """
    #imagelist = [{'url':'https://s3.amazonaws.com/visualintrigue-3556/92ff9249-ca37-48ed-aa65-c5e0f7a6b66b_lowrez_1600px.jpeg'}]
    imagelist = []
    photos = mongo.db.photos.find({'homepage':'yes','status':'active'})
    if photos is None:
        return jsonify(imagelist)

    tlist = []

    for photo in photos:
        if size in photo['files']:
            tlist.append(siteconfig.AMAZON_BASE_URL + photo['files'][size]['path'])

    i = len(tlist)-1

    while i > 1:
        j = random.randrange(i)  # 0 <= j <= i
        tlist[j], tlist[i] = tlist[i], tlist[j]
        i = i - 1

    for t in tlist:
        imagelist.append({'url':t})

    return jsonify({'urls':imagelist})


@app.route('/dbapi/api/v1.0/frontpage', methods=['GET'])
def get_frontpage():
    """ Get the list of results for the frontpage"""

    stories = []
    #blogs = mongo.db.blog.find({'status':'active','homepage':'yes'}).sort("created",-1)

    collections = mongo.db.collections.find({'status':'active'}).sort("created",-1)

    for c in collections:
        photos = mongo.db.photos.find({'status':'active','collection':c['collection'],'homepage':'yes'}).sort('displayorder').limit(1)

        for b in photos:

            b['ctitle'] = c['title']
            b['cslug'] = c['slug']
            b['created'] = datetime.strftime(c['created'],'%Y-%m-%dT%H:%M:%S.%fZ')
            b['summary'] = util.summary_text(c['body'])
            b['type'] = 'photo'
            b.pop('_id')
            stories.append(b)
            break

    articles = mongo.db.articles.find({'status':'active'}).sort("created",-1)

    for a in articles:
        r = {}
        r['created'] = datetime.strftime(a['created'],'%Y-%m-%dT%H:%M:%S.%fZ')
        r['summary'] = util.summary_text(a['body'])
        r['cslug'] = a['slug']
        r['type'] = 'article'
        r['title'] = a['title']
        r['teaserurl'] = a['teaserurl']
        stories.append(r)

    sorted_stories = sorted(stories,key=lambda x:x['created'],reverse=True)

    return jsonify(sorted_stories)


@app.route('/dbapi/api/v1.0/listarticles', methods=['GET'])
def get_listarticles():
    """ Get the list of articles from the database"""

    articles = mongo.db.articles.find({'status':'active'}).sort("created",-1)

    new_articles = []
    for article in articles:
      article['summary'] = util.summary_text(article['body'])
      article.pop('_id')
      article['created'] = datetime.strftime(article['created'],'%Y-%m-%dT%H:%M:%S.%fZ')
      new_articles.append(article)
    return jsonify(new_articles)

@app.route('/dbapi/api/v1.0/article/<id>',methods=['GET'])
def get_article(id):
    article = mongo.db.articles.find_one({'slug':id})
    article.pop('_id')
    try:
      return jsonify(article)
    except Exception as e:
      return jsonify({"title":"Error Finding Article","body":"Oh No!  There was an error finding this article.  We are terribly sorry. ","headerurl":" ","teaserurl":" "})

@app.route('/dbapi/api/v1.0/listportfolios/<portfolio>', methods=['GET'])
def get_portfolioslist_for_id(portfolio="all"):
    """ Get the list of articles from the database"""
    photos = None

    if portfolio != 'all':
        photos = mongo.db.photos.find({'status':'active','homepage':'yes','portfolio':portfolio},{'_id': False }).sort("created",-1)
    else:
        photos = mongo.db.photos.find({'status':'active','homepage':'yes'},{'_id': False }).sort("created",-1)
    if photos is not None:   
        
        return jsonify(list(photos))

    return jsonify([])
 
@app.route('/dbapi/api/v1.0/getstory/<id>')
def get_stories(id = None):
    """ Collection Detail Display """
    collection = None

    if id is not None:
        collection = mongo.db.collections.find_one({'slug':id},{'_id': False })

        collection['summary'] = util.summary_text(collection['body'])
    if collection is None:
        return redirect(url_for('notfound'))

    photos = mongo.db.photos.find({'collection':collection['collection'],'status':'active'},{'_id': False }).sort('displayorder',1)

    #collection['summary'] = util.summary_text(collection['body'])
    firstphoto = None
    if photos.count() > 0:
        firstphoto = photos[0]

    return jsonify({'collection':collection,'photos':list(photos),'firstphoto': firstphoto})

@app.route('/dbapi/api/v1.0/getphoto/<id>')
def get_photo(id = None):
    """
    Photo Detail
    """
    photo = None
    if id is not None:
        photo = mongo.db.photos.find_one({'slug':id},{'_id': False })
        photo['summary'] = util.summary_text(photo['body'])
        return jsonify(photo)
    #if photo is None:
    #    return jsonify({'error':'No photo found'})

    #image_url = siteconfig.AMAZON_BASE_URL + photo['files']['large']['path']
    #lowrez_url = siteconfig.AMAZON_BASE_URL + photo["files"]['lrlarge']['path']

    photo.pop('_id')
    return jsonify({"error":"No result found"})
    #return render_template('photo.html',title=photo['title'],photo=photo,image_url=image_url,lowrez_url=lowrez_url)
     

if __name__ == '__main__':

    app.debug = True

    if app.debug == True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    # create a file handler

    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)

    # create a logging format

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger

    logger.addHandler(handler)

    logger.info("Application started")

    app.run(host="0.0.0.0",port=8888,debug=True)
