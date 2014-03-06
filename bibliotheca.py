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
		text_sql  = ' SELECT c00, c08, c09, iVideoHeight, ivideoduration'
		text_sql += ' FROM movie'
		text_sql += ' LEFT JOIN streamdetails ON movie.idfile = streamdetails.idfile'
		text_sql += '   AND streamdetails.istreamtype = 0'
		text_sql += ' ORDER by c00'
		# Execute the sql into the cursor
		c.execute(text_sql) 
		# fetch it all
		rows = c.fetchall()
		c.close() 
		
		# This is a string to hold HTML
		text_HTML = ("<!DOCTYPE html PUBLIC ""-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd""><html><head>")
		text_HTML += ("<meta content=""text/html; charset=ISO-8859-1"" http-equiv=""content-type"">")
		text_HTML += ("<link rel=""stylesheet"" href=""css/style.css"">")
		text_HTML += ("<title>Films</title>\n")
		text_HTML += ("</head><body>\n")
		text_HTML += ("<table>\n")
		text_HTML += ("<tbody><tr>\n")

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
			
			# IMDB code
			text_imdb = row[2].encode("utf-8")
			
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
			
			# Put all this into a HTML cell
			text_HTML += ('<td>')
			text_HTML += (' <a href="http://www.imdb.com/title/' + text_imdb + '">')
			text_HTML += ('  <img src="' + text_movie_thumbnail + '" alt="' + text_movie_name + '">')
			text_HTML += (' </a><BR>' + text_movie_name + ' (' + text_video_quality + ')')
			text_HTML += (' <BR>' + text_TimeInhhmmss + '<BR>')
			text_HTML += ('</td>\n')
			
			#every 6th start a new row
			if count == 6:
				text_HTML += ('</tr>\n<tr>\n')
				count = 1
			else:
				count += 1
			
		text_HTML += ("</tr></tbody></table><br></body></html>\n")

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
