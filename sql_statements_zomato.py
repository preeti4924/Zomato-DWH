

CREATE_TABLE_URL_DETAILS_SQL = """
CREATE TABLE IF NOT EXISTS url_details (
url_details_id INTEGER NOT NULL AUTO_INCREMENT ,
events_url VARCHAR(200) ,
menu_url VARCHAR(200) ,
book_form_web_view_url VARCHAR(200) ,
book_again_url VARCHAR(200) , 
restaurants_url VARCHAR(200),
restaurant_id INTEGER NOT NULL,
PRIMARY KEY (url_details_id)
);
""" 

CREATE_TABLE_USER_RATINGS_SQL = """
CREATE TABLE IF NOT EXISTS user_ratings (
ratings_id INTEGER NOT NULL AUTO_INCREMENT, 
aggregate_rating REAL,
rating_text VARCHAR(50),
rating_color VARCHAR(50),
votes INTEGER,
rating_title_text REAL,
rating_color_type VARCHAR(50),
rating_color_tint INTEGER,
restaurant_id INTEGER NOT NULL,
PRIMARY KEY (ratings_id)
);
"""

CREATE_TABLE_BOOKING_DETAILS_SQL = """
CREATE TABLE IF NOT EXISTS booking_details (
booking_details_id INTEGER NOT NULL AUTO_INCREMENT,
is_table_reservation_supported CHAR(2),
has_table_booking CHAR(2),
opentable_support CHAR(2), 
is_zomato_book_res CHAR(2),
is_book_form_web_view CHAR(2),
restaurant_id INTEGER NOT NULL,
PRIMARY KEY (booking_details_id)
);
"""


CREATE_TABLE_DELIVERY_DETAILS_SQL = """
CREATE TABLE IF NOT EXISTS delivery_details (
delivery_id INTEGER NOT NULL AUTO_INCREMENT,
has_online_delivery CHAR(2),
is_delivering_now CHAR(2),
restaurant_id INTEGER NOT NULL,
PRIMARY KEY (delivery_id)
);
"""


CREATE_TABLE_LOCATION_DETAILS_SQL = """
CREATE TABLE IF NOT EXISTS location_details (
address VARCHAR(200),
locality VARCHAR(100),
city VARCHAR(20),
city_id INTEGER,
latitude REAL NOT NULL,
longitude REAL NOT NULL,
zipcode VARCHAR(10),
country_id INTEGER,
locality_verbose VARCHAR(100),
restaurant_id INTEGER NOT NULL,
PRIMARY KEY (restaurant_id,latitude, longitude)
);
"""

CREATE_TABLE_RESTAURANTS_SQL = """
CREATE TABLE IF NOT EXISTS restaurants (
restaurant_id INTEGER NOT NULL,
name VARCHAR(70) NOT NULL,
average_cost_for_two INTEGER,
price_range INTEGER ,
all_reviews_count INTEGER ,
photo_count INTEGER ,
ratings_id  INTEGER NOT NULL DEFAULT 0,
url_details_id  INTEGER NOT NULL DEFAULT 0,
booking_details_id  INTEGER NOT NULL DEFAULT 0,
delivery_id INTEGER NOT NULL DEFAULT 0,
latitude REAL NOT NULL ,
longitude REAL  NOT NULL ,
PRIMARY KEY (restaurant_id),
FOREIGN KEY (ratings_id) REFERENCES  user_ratings (ratings_id) ON DELETE SET DEFAULT ON UPDATE CASCADE,
FOREIGN KEY (url_details_id) REFERENCES  url_details (url_details_id) ON DELETE SET DEFAULT ON UPDATE CASCADE,
FOREIGN KEY (booking_details_id) REFERENCES  booking_details (booking_details_id) ON DELETE SET DEFAULT ON UPDATE CASCADE,
FOREIGN KEY (delivery_id) REFERENCES  delivery_details (delivery_id) ON DELETE SET DEFAULT ON UPDATE CASCADE,
FOREIGN KEY (restaurant_id,latitude, longitude) REFERENCES  location_details (restaurant_id,latitude, longitude) ON DELETE RESTRICT ON UPDATE RESTRICT
);
"""

create_all_tables = [CREATE_TABLE_URL_DETAILS_SQL, CREATE_TABLE_USER_RATINGS_SQL, CREATE_TABLE_BOOKING_DETAILS_SQL, CREATE_TABLE_DELIVERY_DETAILS_SQL, CREATE_TABLE_LOCATION_DETAILS_SQL , CREATE_TABLE_RESTAURANTS_SQL]