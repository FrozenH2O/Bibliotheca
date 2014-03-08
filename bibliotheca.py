# Import CherryPy global namespace
import sqlite3 as lite
import cherrypy

def connect(thread_index): 
    # Create a connection and store it in the current thread 
    cherrypy.thread_data.db = lite.connect('../Database/MyVideos75.db')

def format_seconds_to_hhmmss(seconds):
	hours = seconds // (60*60)
	seconds %= (60*60)
	minutes = seconds // 60
	seconds %= 60
	return "%02i:%02i:%02i" % (hours, minutes, seconds)	
	
# Tell CherryPy to call "connect" for each thread, when it starts up 
cherrypy.engine.subscribe('start_thread', connect)	
	
class Bibliotheca:
    def index(self):
        # CherryPy will call this method for the root URI ("/") and send
        # its return value to the client. Because this is tutorial
        # lesson number 01, we'll just send something really simple.
        # How about...
		
		# Database Cursor
		c = cherrypy.thread_data.db.cursor()
		
		# SQL to fetch the stuff we need
		text_sql  = ' SELECT  c00, c08, c09, iVideoHeight, ivideoduration, drvAudioStream.iMaxAudioStream'
		text_sql += ' FROM movie'
		text_sql += ' LEFT JOIN streamdetails ON movie.idfile = streamdetails.idfile'
		text_sql += '   AND streamdetails.istreamtype = 0'
		text_sql += ' LEFT JOIN (select idfile, MAX(iAudioChannels) AS iMaxAudioStream FROM streamdetails WHERE istreamtype = 1 GROUP BY idfile) AS drvAudioStream'
		text_sql += '   ON movie.idfile = drvAudioStream.idFile'
		text_sql += ' ORDER by c00'
		# Execute the sql into the cursor
		c.execute(text_sql) 
		# fetch it all
		rows = c.fetchall()
		c.close() 
		
		# This is a string to hold HTML
		text_file = open ("html_top.html","r")
		text_HTML = text_file.read()

		text_HTML += ('<div class="container">')
		
		count = 1

		# print all the first cell of all the rows
		for row in rows :
			# Movie Name
			text_movie_name = row[0].encode("utf-8")
			
			# Link to Thumbnail, best I can do atm
			arr_file_name = row[1].encode("utf-8").split('http')
			if len(arr_file_name) > 1:
				text_movie_thumbnail = "http" + arr_file_name[1].replace('">','')
			else:
				text_movie_thumbnail = ""
			
			# IMDB code, I do not know why some have too many t's
			text_imdb = "tt" + row[2].encode("utf-8").replace("t","")
			
			# Height of video for 480p, 720p or 1080p
			int_videoheight = row[3]
			# Default to 480p unless its bigger
			text_video_quality = "480p"
			
			# Assume if it is bigger than 480 high it is 720p
			if int_videoheight > 480:
				text_video_quality = "720p"

			# Assume if it is bigger than 720 high it is 1080p
			if int_videoheight > 720:
				text_video_quality = "1080p"
			
			# Movie Duration in seconds, but we want it in HH:MM:SS and as a string
			int_videoduration = row[4]
			if int_videoduration > 0:
				text_TimeInhhmmss = format_seconds_to_hhmmss(int_videoduration)
			else:
				text_TimeInhhmmss = ""

			# Movie Duration in seconds, but we want it in HH:MM:SS and as a string
			int_audiochannels = row[5]
			if int_audiochannels > 2:
				text_AudioChannels = ' / 5.1'
			else:
				text_AudioChannels = ""
				
			# Put all this into a HTML cell
			text_HTML += ('\n<div class="three columns grid-item">')
			text_HTML += (' <a href="http://www.imdb.com/title/' + text_imdb + '">')
			text_HTML += ('  <img src="' + text_movie_thumbnail + '" alt="' + text_movie_name + '"></a>')
			text_HTML += ('<br />' + text_movie_name + '<br />')
			text_HTML += (text_video_quality + text_AudioChannels + ' - ' + text_TimeInhhmmss + ' ')
			text_HTML += ('</div>')

			#every 5th start a new row
			if count == 5:
				text_HTML += ('</div><br />')
				text_HTML += ('<div class="container">')
				count = 1
			else:
				count += 1

		text_HTML += ('<!-- Footer -->')
		text_HTML += ('</div><!-- container -->')
		text_HTML += ('<!-- End Document')
		text_HTML += ('================================================== -->')
		text_HTML += ('</body>')
		text_HTML += ('</html>		')
		
		# display the web page
		return text_HTML

    # Expose the index method through the web. CherryPy will never
    # publish methods that don't have the exposed attribute set to True.
    index.exposed = True
	
import os.path
bibliothecaconf = os.path.join(os.path.dirname(__file__), 'bibliotheca.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to Bibliotheca().index().
    cherrypy.quickstart(Bibliotheca(), config=bibliothecaconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(Bibliotheca(), config=bibliothecaconf)
