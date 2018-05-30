## RestFullAPI ( with token base authentication )
Simple python Flask RESTFull API which provides a service for storing, updating, retrieving and deleting Person entities
## Requirements:
For python see `requirements.txt`
## Dependencies:
- Install mongodb [Install mongodb](https://docs.mongodb.com/manual/installation/)
- Install python and pip (tested on python3, should works with python 2.x ). Check [Install python](http://docs.python-guide.org/en/latest/starting/installation/) for python installation instructions

## How to run the application:
( These steps means to build and run on Mac OSx or Linux only. For Windows you need to do your own research or just use docker )
- Make sure you have a running mongodb server and access right to it
- Clone this repo and go to **Development/RestFullAPI** folder
- Most of the configurations can be change inside `resources.py`. Please change accordingly 
- Run : 
	- `pip install virtualenv`
	- `virtualenv /opt/python`
	- `source /opt/python/bin/activate`
	- `pip install -r requirements.txt`
	- `python run.py`
- Flask application default bind at port 5000. ( http://127.0.0.1:5000 ) 
- If you prefer to run on `docker` then just execute `run_local_docker.sh`. ( Make sure you change MONGODB_HOST before running with docker )

## API References:
- ``` / -> index```
- ``` /api -> Method=Get to retrieve contents```
- ``` /login -> Method=Post for login ```
- ``` /logout -> Method=Post for logout ```
- ``` /search/<string:name> -> Method=Get for searching ```
- ``` /api/<string:id> -> Method=Get for filtering with id ```
- ``` /api/<int:maximum> -> Method=Get for limit result ```

## Unit Test
- You can perform a simple unit test by run `tests.py` ( This included most of the running functions of the application )
- Or if you have it run with docker you can run `docker run -ti --rm --link mongodb:mongodb -p 5000:5000 restfullapi python tests.py` to see the results. ( Assumed you have a mongodb instance running with name `mongodb`
## Sample client
- There is a quick dirty client for testing with the api inside **sample** folder ( You need pymongo libary, just `pip install pymongo` )
