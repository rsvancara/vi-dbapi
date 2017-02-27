import re
import unicodedata
import os
from datetime import datetime
import logging
import errno


    
def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)
  

def summary_text(text):
    replace = ['&nbsp;',]
    text = re.sub('<[^<]+?>', '', text)
    for r in replace:
        text = text.replace(r,'')
    ret = ""
    
    items = text.split()
    size = 65
    if len(items) < 65:
        size = len(items)
    for item in items[0:size]:           
        ret = ret + " " + item.strip()
    if len(items) >= 65:
        ret = ret + "..." 
    return ret


def pathtodir(path):
    if not os.path.exists(path):
        l=[]
        p = "/"
        l = path.split("/")
        i = 1
        while i < len(l):
            p = p + l[i] + "/"
            i = i + 1
            if not os.path.exists(p):
                os.mkdir(p)

def path_hierarchy(path):
    hierarchy = {
        'type': 'folder',
        'name': os.path.basename(path),
        'path': path,
    }

    try:
        hierarchy['children'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy


def main():
    pass


if __name__ == "__main__":
    main()
    
