from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(250), unique=True, nullable=False)
	name = db.Column(db.String(250))
	password = db.Column(db.String(250), nullable=False)

class Study(UserMixin, db.Model): #ie a user 'studies a stock
	id=db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	ticker = db.Column(db.Integer, nullable=False)
	studies = db.Column(db.Text, nullable=True)
	historical_data = db.Column(db.Text, nullable=True)
	results = db.Column(db.Text, nullable=True)
	#studies ex: "metric:threshold, metric2:threshold2"  Parse when calling api
	#Results listed in Text, format same "metric:value, metric2:value" Parse when displaying to frontend

#id, user_id, {ticker: metric_id}


class Metric(UserMixin, db.Model):#loop through yf ticker.info.* to get list of metrics
	id=db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))

#id, {metric: 30.0}

# class HistoricalData(UserMixin, db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	ticker = db.Column(db.String(250), nullable=False)


class Studied(UserMixin, db.Model):
	# Results table 
    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey("study.id"), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey("metric.id"), nullable=False)
	
	
#ok so the layout for what needs to go in the database
#-user credentials tagged to their individual data
#
#          -the stocks they are following which will have a                study group attached to it.
#
#          -the study groups they create which can then be            added to the stocks they want to follow
#
#  -the data we collect for stocks can be stored seperately to potentially reduce the amount calls if we actually had multiple users. with this data we can check if there has already been a call or two that day for that stock to limit the amount of calls.
#i kind of explained that poorely let me know if you want a clearer picture
#Shmitty — Yesterday at 6:31 PM
#I think this covers most of the data
#But we need to specify more of the specific user values
#blacknight94 — Yesterday at 6:32 PM
#but yes most likely each stock will have different metrics they are following
#DanielF — Yesterday at 6:35 PM
#Ok. So each stock should have a study group.  I assume each metric has a threshold that goes along with the study.  Besides that I am storing username, password, id, and email.
#I should probably add a result parameter in the database so it can determine when to send the email or let the user know
#Shmitty — Yesterday at 6:38 PM
#I’m not sure how sql is structured, but could we have a column that stores a data structure? 
#DanielF — Yesterday at 6:38 PM
#I assume so.  Let me check
#Shmitty — Yesterday at 6:39 PM
#And store the comparison/I put metrics in that instead of over a few rows
#DanielF — Yesterday at 6:47 PM
#I can store the data structure in another table and just associate that with the ID of the user account table. So there will be 2 tables in the database and one will store user info and the other the study groups.
#Shmitty — Yesterday at 6:50 PM
#That might be the way to go, it depends on how we choose to allow for the user to customize the tests
#DanielF — Yesterday at 6:53 PM
#For the front-end we should decide how the process for how the user selects the studies and stocks so we can integrate this easier.
