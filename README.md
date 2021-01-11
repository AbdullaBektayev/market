# market
For Chokofood

This Django project collect all data about devices from store like 'Technodom' , 'Mechta', 'Sulpak' and 'Белый ветер' in categories 'smartphone', 'tablets', 'cameras', 'notebook'

In data we have: name, price, description, which category, by which company provided
  
In this project we use 'Celenium', 'Celery', 'Django', 'Django Rest Framework'

1) first you need to create database on your local computer then rewrite some line of code in the project 

  1.1. setting.py 
  
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'market',      # place for your postgres database
          'USER': 'postgres',    # place for your postgres user_name
          'PASSWORD': 'root',    # place for your postgres password
          'HOST': 'localhost',   # place for your postgres host
          'PORT': '5432'         # place for your postgres port
      }
    }
    
    
   1.2. markets/tasks.py
   
        conn = psycopg2.connect(
            user= 'postgres',       # place for your postgres user_name
            database = 'market',    # place for your postgres database
            password = 'root',      # place for your postgres password
            host = 'localhost',     # place for your postgres host
            port = '5432'           # place for your postgres port
        )

        cursor = conn.cursor()
        
2) second you need to write this to the 3 terminal window 

  1 - terminal:
  
    1.1  go to the our django project file 
        $ cd markets_place
       
    1.2 start rabbitmq
        $ /usr/local/sbin/rabbitmq-server
      
  2 - terminal:
  
    2.1  go to the our django project file 
        $ cd markets_place
       
    2.2 start celery
        $ celery -A market_place worker -B -l INFO
        
  3 - terminal:
  
    2.1  go to the our django project file 
        $ cd markets_place
       
    2.2 run the django
        $ python manage.py runserver
        

Now your django and others ready

3) go to the admin page, with adding the end of main url  '/admin'
  
  3.1 select the 'pereodic tasks'
  
  3.2 run the task
  
Now your parser started the work

