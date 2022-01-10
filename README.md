## TDLOG project - Findyourshows

Findyourshows App enables any user to search for TV Shows. 
Registered users can add TV Shows to their favourites in order to get more details on the show such as the episodes' description.
They also can enable notifications whenever a new episode of one of their favourites is aired.

We deployed it on Heroku: <a href='https://findyourshows.herokuapp.com'> this address <a/>.

## Installation
1. Install the Python `virtualenv` package: 

	`pip install virtualenv`


2. Download the projet directory. Once the files unzipped/downloaded, create a python virtual environment in the said directory: 

	`cd /project_directory`
	
	`virtualenv venv`
	
	`source venv/bin/activate`


3. From the same directory, install the app and its dependencies:

	`pip install -e findyourshows/`
  
  
## Running the MyFavShows
   
1. Go to your virtualenv. Add the app to your environment variables:

	Linux / MacOS:`export FLASK_APP=findyourshows`
	
	Windows: `set FLASK_APP=myfavshows`

2. Run the app:

	`flask run`


