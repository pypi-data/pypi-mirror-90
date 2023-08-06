# Daboi Package

This is an instagram automation with selenium. 

## Prerequisities

* selenium
* chromedriver

## Features

* Likes - home feed and hashtags
* Follows - hashtags
* Unfollows
* Watch stories

## Install


```python
pip3 install daboi
```
## Update
```python
pip3 install -U daboi
```
## Run


```python
from daboi import instabot

config = {
	"user":"username",
	"password":"password"i,
	#"chromedriver_path":"", # path to chromedriver default is linux /usr/lib/chromium-browser/chromedriver
	#"path":"" # where the output files will be stored default is working directory
	"hashtag_list":["hashtag1","hashtag2"], #hashtags to give likes to photos 
	"likes":15,#likes per run to give
	"follow":0, #follow profiles per run
	"unfollow":0, #unfollow profiles per run
	"follow_profiles":["username1","username2"], #follow the followers of given profiles
	"wait_between_runs":2, #wait between two consecutive runs
	"watch_stories_minutes":5, #watch hasthags and progile stories in minutes
	"give_likes_when":0, #photo has to have also another one or more hashtags set in hashtag_list
	"api_key":"", # api token to authentificate
	"api_endpoint"="" # url where to send run statistics. you might need to change code for your own needs but you might want to implement two methods get and write

}
instabot.Client(config)

#enjoy the stonks
```

