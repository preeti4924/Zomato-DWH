INSERT_TABLE_RESTAURANTS = """
INSERT INTO restaurants (restaurant_id, name, average_cost_for_two, price_range, all_reviews_count, photo_count, ratings_id, url_details_id, booking_details_id, delivery_id, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

INSERT_TABLE_URL_DETAILS = """
INSERT INTO url_details (events_url, menu_url, book_form_web_view_url, book_again_url,restaurants_url, restaurant_id) 
VALUES (%s, %s, %s, %s, %s, %s);
"""

INSERT_TABLE_USER_RATINGS = """
INSERT INTO user_ratings (aggregate_rating, rating_text, rating_color, votes, rating_title_text,rating_color_type, rating_color_tint, restaurant_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

INSERT_TABLE_BOOKING_DETAILS = """
INSERT INTO booking_details (is_table_reservation_supported, has_table_booking, opentable_support, is_zomato_book_res, is_book_form_web_view, restaurant_id)
VALUES (%s, %s, %s, %s, %s, %s);
"""

INSERT_TABLE_DELIVERY_DETAILS = """
INSERT INTO delivery_details (has_online_delivery, is_delivering_now, restaurant_id)
VALUES (%s, %s, %s);
"""

INSERT_TABLE_LOCATION_DETAILS = """
INSERT INTO location_details (address, locality, city, city_id, latitude, longitude, zipcode, country_id, locality_verbose, restaurant_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

tables_insertion = [INSERT_TABLE_RESTAURANTS, INSERT_TABLE_URL_DETAILS, INSERT_TABLE_USER_RATINGS, INSERT_TABLE_BOOKING_DETAILS, INSERT_TABLE_DELIVERY_DETAILS,
					INSERT_TABLE_LOCATION_DETAILS]