import flickrapi
import urllib2

api_key = 'YOUR API KEY'

flickr = flickrapi.FlickrAPI(api_key)
photos = flickr.photos_search(user_id='73509078@N00', per_page='10')
sets = flickr.photosets_getList(user_id='73509078@N00')

for photo in photos:
	print photo