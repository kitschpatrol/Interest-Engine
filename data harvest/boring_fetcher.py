import flickrapi
from urllib2 import Request, urlopen
import random

# get the flickr lib here http://stuvel.eu/projects/flickrapi
api_key = '677baa52240b5f6988cf3f13c0791428'

flickr = flickrapi.FlickrAPI(api_key, format='etree')

photos_wanted = 1000
photos_found = 0

while photos_found <  photos_wanted:
	# Give us a random ID between 1,500,000,000 and 3000000000
	random_id = int((random.random() * 1500000000) + 1500000000)
	print "looking for photo with id " + str(random_id)
	try:
		info = flickr.photos_getInfo(photo_id = random_id)
	except:
		print "no photo with that id, trying another"
		pass
	else:
		print "photo exists!"


		views = info[0].attrib['views']
		print "photo " + str(random_id) + " has " + str(views) + " views...",
		
		if int(views) == 0:
			print "perfect, downloading"
			
			# build the url
			# print info[0][0].attrib
			print info[0].attrib['server']
			
			# http://farm{farm-id}.static.flickr.com/{server-id}/{id}_{secret}_[mstb].jpg
			print info[0].attrib
			server = info[0].attrib['server']
			farm = info[0].attrib['farm']
			secret = info[0].attrib['secret']
			size = "s"
			
			url = "http://farm" + str(farm) + ".static.flickr.com/" + str(server) + "/" + str(random_id) + "_" + str(secret) + "_" + size + ".jpg"

			req = Request(url)
			f = urlopen(req)

			# open our local file for writing
			local_file = open('boring-images/' + str(random_id) + '.jpg', 'w')
			
			# write to the local file
			local_file.write(f.read())
			local_file.close()			
			
			photos_found += 1			
			
		else:
			print "too many"
			# download it


	print ""


#print interesting_photos.items

# download each one
# i = 1;
# for photo in interesting_photos.getiterator('photo'):
# 	if 'url_sq' in photo.attrib:
# 		
# 		print 'Downloading photo ' + str(i) + ': ' + photo.attrib['url_sq'] + " which has " + str(photo.attrib['views']) + " views."
# 
# 		req = Request(photo.attrib['url_sq'])
# 		f = urlopen(req)
# 
# 		# tk don't re-download photos
# 
# 		# open our local file for writing
# 		local_file = open('boring-images/' + photo.attrib['id'] + '.jpg', 'w')
# 	
# 	
# 		# write to the local file
# 		local_file.write(f.read())
# 		local_file.close()
# 	
# 	i += 1;