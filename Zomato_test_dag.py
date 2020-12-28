import datetime
import logging

from airflow import DAG
from airflow.hooks.http_hook import HttpHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.http_operator import SimpleHttpOperator
import json
from jsonmerge import Merger
import sql_statements_zomato
import insert_into_sql_statements
import pandas as pd
from airflow.operators.bash_operator import BashOperator



dfNameDict={	'restaurant': [
					'restaurant.id',
					'restaurant.name',
					'restaurant.average_cost_for_two',
					'restaurant.price_range',
					'restaurant.all_reviews_count', 
					'restaurant.photo_count'
					] ,
              
					'delivery' : ['restaurant.has_online_delivery',
					'restaurant.is_delivering_now',
					'restaurant.id'] ,
              
					'booking' : ['restaurant.is_table_reservation_supported',
								 'restaurant.has_table_booking', 
								 'restaurant.opentable_support', 
								 'restaurant.is_zomato_book_res',
								 'restaurant.is_book_form_web_view',
								 'restaurant.id'] ,
              
					'url' : [
							 'restaurant.events_url',
							 'restaurant.menu_url',
							 'restaurant.book_form_web_view_url',
							 'restaurant.book_again_url',
							 'restaurant.url',
							 'restaurant.id'
							 ] ,
              
					'user_rating' : ['restaurant.user_rating','restaurant.id'] , 
              
					'location' : ['restaurant.location','restaurant.id'] ,
              
					'currency': ['restaurant.currency', 'restaurant.id']}


def get_data_zomato_api(*args, **kwargs):
	
	
	api_hook = HttpHook(http_conn_id = "zomato_api", method = 'GET')
	
	data_dict = {}

	schema ={
				"properties": {
					"restaurants": {
						"mergeStrategy": "append"
					}
				}
			}
	merger=Merger(schema)

	for i in range(0, 100, 20):
		
		endpoint_url = "search?entity_id=3&entity_type=city&start={}&count=20&sort=rating".format(i)
		
		resp_url = api_hook.run(endpoint = endpoint_url)
		resp = json.loads(resp_url.content)
		
		if i == 0:

			data_dict.update(resp)
			result = data_dict
		else:			
			result = merger.merge(result, resp)    
		with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "w") as f:
			json.dump(result, f)
		f.close()

	

def create_tables_mysql(*args, **kwargs):
	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_uri()
	print(conn)



# def prep_json(*args, **kwargs):
# 	task_instance = kwargs['get_data_zomato_api']
# 	ti = kwargs['ti']
# 	result = ti.xcom_pull(task_ids = 'get_data_zomato_api')
# 	global result	
# 	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
# 		result = json.load(f)
# 	f.close()

# 	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')
	


# 	daL2 = normalizedL1.reset_index()


# 	restaurant = daL2[dfNameDict['restaurant']]
# 	delivery = daL2[dfNameDict['delivery']]
# 	booking = daL2[dfNameDict['booking']]
# 	url = daL2[dfNameDict['url']]
# 	user_rating = daL2[dfNameDict['user_rating']]
# 	user_rating = pd.concat([pd.json_normalize(user_rating.drop(['restaurant.id'], axis = 1)['restaurant.user_rating']), user_rating['restaurant.id']], axis = 1)	
# 	location = daL2[dfNameDict['location']]
# 	location = pd.concat([pd.json_normalize(location.drop(['restaurant.id'], axis = 1)['restaurant.location']), location['restaurant.id']], axis = 1)
# 	currency = daL2[dfNameDict['currency']]
# 	dataframe_dict = {'restaurant': restaurant, }
# 	print('Tables created')




	
	

def user_ratings_insert(*args, **kwargs):
	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
		result = json.load(f)
	f.close()
	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')

	daL2 = normalizedL1.reset_index()

	
	user_rating = daL2[dfNameDict['user_rating']]
	user_rating = pd.concat([pd.json_normalize(user_rating.drop(['restaurant.id'], axis = 1)['restaurant.user_rating']), user_rating['restaurant.id']], axis = 1)	
	user_rating['restaurant.id'] = pd.to_numeric(user_rating['restaurant.id'])
	user_rating['aggregate_rating'] = user_rating['aggregate_rating'].astype(float)
	user_rating['rating_text'] = user_rating['rating_text'].astype(str)
	user_rating['rating_color'] = user_rating['rating_color'].astype(str)
	user_rating['rating_obj.title.text'] = user_rating['rating_obj.title.text'].astype(float)
	user_rating['rating_obj.bg_color.type'] = user_rating['rating_obj.bg_color.type'].astype(str) 
	user_rating['rating_obj.bg_color.tint'] = user_rating['rating_obj.bg_color.tint'].astype(str)

	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_conn()
	connection = conn
	curr = connection.cursor()


	for i, row in user_rating.iterrows():
		# print(row)
		curr.execute(insert_into_sql_statements.INSERT_TABLE_USER_RATINGS, row)
		connection.commit()
	curr.close()



	
def bookings_details_insert(*args, **kwargs):
	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
		result = json.load(f)
	f.close()
	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')

	daL2 = normalizedL1.reset_index()

	
	booking = daL2[dfNameDict['booking']]		
	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_conn()
	connection = conn
	curr = connection.cursor()

	
	for i, row in booking.iterrows():
		curr.execute(insert_into_sql_statements.INSERT_TABLE_BOOKING_DETAILS, row)
		connection.commit()
	curr.close()



def delivery_details_insert(*args, **kwargs):
	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
		result = json.load(f)
	f.close()
	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')

	daL2 = normalizedL1.reset_index()

	
	delivery = daL2[dfNameDict['delivery']]		

	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_conn()
	connection = conn
	curr = connection.cursor()

	
	for i, row in delivery.iterrows():
		curr.execute(insert_into_sql_statements.INSERT_TABLE_DELIVERY_DETAILS, row)
		connection.commit()
	curr.close()



def location_details_insert(*args, **kwargs):
	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
		result = json.load(f)
	f.close()
	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')

	daL2 = normalizedL1.reset_index()

	
	location = daL2[dfNameDict['location']]		
	location = pd.concat([pd.json_normalize(location.drop(['restaurant.id'], axis = 1)['restaurant.location']), location['restaurant.id']], axis = 1)
	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_conn()
	connection = conn
	curr = connection.cursor()

	
	for i, row in location.iterrows():
		
		curr.execute(insert_into_sql_statements.INSERT_TABLE_LOCATION_DETAILS, row)
		connection.commit()
	curr.close()

def url_details_create_insert(*args, **kwargs):
	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
		result = json.load(f)
	f.close()
	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')

	daL2 = normalizedL1.reset_index()

	url_details = daL2[dfNameDict['url']]
	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_conn()
	connection = conn
	curr = connection.cursor()

	
	for i, row in url_details.iterrows():
		curr.execute(insert_into_sql_statements.INSERT_TABLE_URL_DETAILS, row)
		connection.commit()
	curr.close()

def restaurant_create_insert(*args, **kwargs):
	with open("/Users/preetiyerkuntwar/documents/Zomato-test/all_restro.json", "r") as f:
		result = json.load(f)
	f.close()
	normalizedL1 = pd.json_normalize(result["restaurants"], max_level = 1).drop(columns = ['restaurant.apikey']).set_index('restaurant.id')

	daL2 = normalizedL1.reset_index()

	restaurant = daL2[dfNameDict['restaurant']]
	mysql_hook = MySqlHook(mysql_conn_id = "mysql_zomato")
	conn = mysql_hook.get_conn()
	connection = conn
	curr = connection.cursor()

	
	for i, row in restaurant.iterrows():
		results_all = []
		sql_ratings = """SELECT ratings_id FROM user_ratings WHERE restaurant_id = {}""".format(pd.to_numeric(row[0]))
		sql_url = """SELECT url_details_id FROM url_details WHERE restaurant_id = {}""".format(pd.to_numeric(row[0]))
		sql_booking = """SELECT booking_details_id FROM booking_details WHERE restaurant_id = {}""".format(pd.to_numeric(row[0]))
		sql_delivery = """SELECT delivery_id FROM delivery_details WHERE restaurant_id = {}""".format(pd.to_numeric(row[0]))
		sql_latitude = """SELECT latitude FROM location_details WHERE restaurant_id = {}""".format(pd.to_numeric(row[0]))
		sql_longitude = """SELECT longitude FROM location_details WHERE restaurant_id = {}""".format(pd.to_numeric(row[0]))

		curr.execute(sql_ratings)
		result_ratings = curr.fetchone()
		resr = int(result_ratings[0])
		results_all.append(resr)
		

		curr.execute(sql_url)
		result_url = curr.fetchone()
		resu = int(result_url[0])
		results_all.append(resu)

		curr.execute(sql_booking)
		result_booking = curr.fetchone()
		resb = int(result_booking[0])
		results_all.append(resb)
		

		curr.execute(sql_delivery)
		result_delivery = curr.fetchone()
		resd = int(result_booking[0])
		results_all.append(resd)

		curr.execute(sql_latitude)
		result_latitude = curr.fetchone()
		resla = float(result_latitude[0])
		results_all.append(resla)

		curr.execute(sql_longitude)
		result_longitude = curr.fetchone()
		reslo = float(result_longitude[0])
		results_all.append(reslo)

		

		results_alll = pd.Series(results_all)
		row = row.append(results_alll)
		curr.execute(insert_into_sql_statements.INSERT_TABLE_RESTAURANTS, row)
		connection.commit()
	curr.close()



dag = DAG(
	'run_zomato_api',
	start_date = datetime.datetime.now()
	# max_active_runs = 1
	)



get_data_zomato_api = PythonOperator(
					task_id = 'get_data_zomato_api',
					python_callable = get_data_zomato_api,
					dag = dag)
	



create_tables_mysql = MySqlOperator(
					task_id = 'create_tables_mysql',
					mysql_conn_id = 'mysql_zomato',
					sql = sql_statements_zomato.create_all_tables,
					dag = dag)

# prep_json = PythonOperator(
# 			task_id = 'prep_json',
# 			python_callable = prep_json,
# 			provide_context = True,
# 			op_kwargs = {"result" : "{{ ti.xcom_pull(task_ids= 'get_data_zomato_api') }}"},
# 			dag = dag)



create_insert_url_details = PythonOperator(
							task_id = 'create_insert_url_details',
							python_callable = url_details_create_insert,
							dag = dag)

user_ratings_insert = PythonOperator(
							task_id = 'user_ratings_insert',
							python_callable = user_ratings_insert,
							dag = dag)
bookings_details_insert = PythonOperator(
							task_id = 'bookings_details_insert',
							python_callable = bookings_details_insert,
							dag = dag)
delivery_details_insert = PythonOperator(
							task_id = 'delivery_details_insert',
							python_callable = delivery_details_insert,
							dag = dag)
location_details_insert = PythonOperator(
							task_id = 'location_details_insert',
							python_callable = location_details_insert,
							dag = dag)

restaurant_create_insert = PythonOperator(
							task_id = 'restaurant_create_insert',
							python_callable = restaurant_create_insert,
							dag = dag)

get_data_zomato_api>> create_tables_mysql  >> user_ratings_insert >> bookings_details_insert >> delivery_details_insert >> location_details_insert >> create_insert_url_details >> restaurant_create_insert
# >> exec_py_script
