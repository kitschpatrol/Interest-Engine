import flickrapi
import urllib2

# get the flickr lib here http://stuvel.eu/projects/flickrapi
api_key = '677baa52240b5f6988cf3f13c0791428'

flickr = flickrapi.FlickrAPI(api_key, format='etree')
interesting_photos = flickr.interestingness_getList(extras = 'url_sq')

print dir(interesting_photos)
print interesting_photos
print interesting_photos.items

for photo in interesting_photos.getiterator('photo'):
	print photo.attrib['url_sq']