#!/usr/bin/python3


import os
import requests
import shutil


project_dir = os.path.dirname(os.path.realpath(__file__))


id = 1    # starting id.
max = 100000   # finish scraping after reaching max id.



print('\nArtfan Downloader\n')



session = None
wallpaper = None


while (id <= max):

    # start a session
    session = requests.Session()
    
    # store cookies. Required or else site won't let you download wallpapers.
    cookies = session.get('http://artfan.net/details.php?image_id='+ str(id))


    # get wallpaper from url
    wallpaper = session.get('http://artfan.net/download.php?image_id='+ str(id), stream=True)


    if (wallpaper.status_code == 200):
        
        headers = wallpaper.headers
        content_type = headers.get('content-type')

        # check if retrieved data is for an image.
        if (content_type == 'application/octet-stream'):

            with open(project_dir + '/wallpapers/' + str(id) + ".jpg", 'wb') as output_file:
                shutil.copyfileobj(wallpaper.raw, output_file)
                print('[ID: '+str(id)+'] Downloaded.')

        # not an image
        else:
            print('[ID: '+str(id)+'] Not an image. Discarded.')
            
    else:
        print('[ID: '+id+'] Error retrieving this wallpaper.')


    # increase wallpaper id value by one
    id = id + 1


print('Done.')


if session:
    del session

if wallpaper:
    del wallpaper