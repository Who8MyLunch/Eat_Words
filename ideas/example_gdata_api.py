
from __future__ import division, print_function, unicode_literals

import os

import gdata
import gdata.docs
import gdata.docs.client




def connect_client():
    # Credentials.
    username = 'pierre.villeneuve@gmail.com'
    gaspw = 'qjahvuisfmeyteve'

    # Application details.
    source = 'scrabble_helper'

    # Make a client and connect to Google.
    client = gdata.docs.client.DocsClient()
    client.client_login(username, gaspw, source)

    # Done.
    return client




#####################################
# Setup.
fname = os.path.abspath('2012-05-07 09.41.52 - grid.png')

title = 'My Sample Document - Grid'
description = 'This is just an example where I try to get OCR working.'

############
# Do it.
client = connect_client()

doc = gdata.docs.data.Resource(type='document', title=title)
doc.description = gdata.docs.data.Description(description)

# Create a MediaSource, pointing to the file
media = gdata.data.MediaSource()
media.SetFileHandle(fname, 'image/png')

# Pass the MediaSource when creating the new Resource
create_uri = gdata.docs.client.RESOURCE_UPLOAD_URI + '?ocr=true&ocr-language=en'
doc = client.CreateResource(doc, create_uri=create_uri, media=media)

# doc = client.create_resource(doc, media=media)
print('Created, and uploaded:', doc.title.text, doc.resource_id.text)


  

# Done.
