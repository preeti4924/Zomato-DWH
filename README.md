<h2> Zomato Database Project </h2>

The goal of this project is to develop a datapipeline which extracts, transforms and loads data from Zomato API to the database in MySQL.
The database contains top 100 restaurants in Mumbai with their location, reservations, delivery and rating details. Data stored 
in the database can be used to derive insights and reporting purposes.

<h2> Project Architecture </h2>


<ol>1) Airflow retrieves JSON data from Zomato API and stores it in a file locally once the dag run_zomato_api is triggered</ol>
<ol>2) Tables are created in MySQL Zomato database</ol>
<ol>3) Data is loaded in each of the six tables in the database schema after appropriate transformations have been applied through Airflow python callables</ol>
<ol>4) Validation checks are performed on the loaded tables to comply with data quality checks</ol>

<h2> Database ER Diagram </h2>
![ERD](https://github.com/preeti4924/Zomato-DWH/blob/master/ER-Diagram.jpg)
<h2> Airflow DAG </h2>
![DAG](https://github.com/preeti4924/Zomato-DWH/blob/master/Airflow-DAG.jpg)
<h2> Installation and Local Execution </h2>

<ol>1) Create a new environment on your local machine and activate it </ol>

<ol>2) Install python 3.7.4 in the new python environment</ol>

<ol>3) Install Airflow 1.10.12 in the new python environment along with CeleryWorker and RabbitMq</ol>

<ol>4) Set up database for airflow</ol>

<ol>5) Open terminal, start airflow webserver, worker and scheduler</ol>

<ol>6) Set up connection for MySQL in Airflow </ol>

<ol>7) Got to http://localhost:8080 and trigger DAG run_zomato_api</ol>
