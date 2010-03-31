import flickrapi
from urllib2 import Request, urlopen

# get the flickr lib here http://stuvel.eu/projects/flickrapi
api_key = '677baa52240b5f6988cf3f13c0791428'

flickr = flickrapi.FlickrAPI(api_key, format='etree')

# takes date as YYYY-MM-DD
interesting_photos = flickr.interestingness_getList(extras = 'url_sq', per_page = 500, date = '2009-03-10')

#print interesting_photos.items

# download each one
i = 1;
for photo in interesting_photos.getiterator('photo'):
	if 'url_sq' in photo.attrib:
		print 'Downloading photo ' + str(i) + ': ' + photo.attrib['url_sq']

		req = Request(photo.attrib['url_sq'])
		f = urlopen(req)

		# tk don't re-download photos

		# open our local file for writing
		local_file = open('images/' + photo.attrib['id'] + '.jpg', 'w')
	
		# write to the local file
		local_file.write(f.read())
		local_file.close()
	
	i += 1;