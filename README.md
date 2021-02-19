# ratestask

Implementation part of https://github.com/xeneta/ratestask




# Deployment 

1. Env Update From /config/settings
Create .env file by copying .env.example. Update Db Credentials if different 
   



**`Without Docker Configurations`**

**2.Installing Requirements**
`pip install -r requirements.txt`

**3. Run Migrations**
`python3 manage.py migrate`
   
**4. Dump Rates into Postgres**
`psql ratestask < rates.sql`
   
**5. Run the Server**
`python3 manage.py runserver`


**`With Docker Configurations`**

2. Run `docker-compose up` and you are ready to go
check the browser on `127.0.0.1:8000`
   

**`Task 1 : Part 1`**

`curl "http://127.0.0.1/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"

[
    {
        "day": "2016-01-01",
        "average_price": 129
    },
    {
        "day": "2016-01-02",
        "average_price": 139
    },
    ...
]`


**`Task 1: Part 2`**

`curl "http://127.0.0.1/rates_null?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"

[
    {
        "day": "2016-01-01",
        "average_price": 129
    },
    {
        "day": "2016-01-02",
        "average_price": null
    },
    {
        "day": "2016-01-03",
        "average_price": 215
    },
    ...
]`

**`Post Request Task : Part 1 & 2`**

 
API endpoint `http://127.0.0.1/price_insert` where you can upload a price using POST method, including the following parameters:


date_from
date_to
origin_code,
destination_code
price

**`Task 2: Batch Processing Task`**

If i have to handle thousands of data using existing system, i would first convert the db structure into Django models and Data insertion will be allowed from  API End Points.

And Those End points will be handled from celery background tasks using Parallel computing to make it more faster.

Also, About the SQL Query. I have written loop in python  and then select query from sql query. There were two approaches i could apply.
1. to use Loop for date inside SQL query Like `generate_series` and avoid python loop.
2. Use Parallel computing to speed things up in the current code.
