Bibliotheca - Pre-Alpha

Is a view only view on the XBMC database.  I wanted a way to allow my friends to see what movies I have.
This is basically a listing of the movies in the XBMC database.  I use openELEC so that what I've coded it to work with.

It is self contained-ish as it uses a cherrypy web server.

Installation - openELEC
Download and unzip all files onto your openELEC samba share to folder
\Userdata\bibliotheca

Inside \Userdata\bibliotheca there should be the cherrypy folder, css folder, bibliotheca.py, bibliotheca.conf and couple more files.

Then ssh onto your openELEC box.
cd .xbmc
cd userdata
cd bibilotheca
then run bibliotheca by using this command line:
python bibliotheca.py

If everything works, you'll be able to use a browser to go to http://openelec_box_ip:8088

If you need to change the port number edit bibliotheca.conf


Please note, I do not know what I am doing, so any advice would be welcome.