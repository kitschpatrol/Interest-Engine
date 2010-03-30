import flickrapi
import urllib2

api_key = '677baa52240b5f6988cf3f13c0791428'

flickr = flickrapi.FlickrAPI(api_key)
photos = flickr.photos_search(user_id='73509078@N00', per_page='10')
sets = flickr.photosets_getList(user_id='73509078@N00')

for photo in photos:
	print photo