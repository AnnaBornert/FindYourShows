## TDLOG project - Findyourshows

Findyourshows App enables any user to search for TV Shows. 
Registered users can add TV Shows to their favourites in order to get more details on the show such as the episodes' description.
They also can enable notifications whenever a new episode of one of their favourites is aired.

We deployed it on Heroku: <a href='https://findyourshows.herokuapp.com'> this address <a/>.

## Installation
1. Download the projet directory. Once the files unzipped/downloaded, create a python virtual environment in the said directory: 

	`cd /project_directory`
	
	`python3 -m venv venv`
	
	Linux / MacOS: : `.venv/bin/activate`

	Windows : `venv\Scripts\activate`


2. From the same directory, install flask and requests:

	`pip install flask`

	`pip install requests`
  
  
## Running the MyFavShows
   
1. Go to your virtualenv. Add the app to your environment variables:

	Linux / MacOS:`export FLASK_APP=flaskr`
	
	Windows: `set FLASK_APP=flaskr`

2. Run the app:

	`flask run`


