# Movie Explorer Project Milestone 2 Subhash Tanikella

## Heroku URL

[Heroku Url](https://fast-ridge-64170.herokuapp.com/)

## After Forking this repository

First step would be to download the packages that have been added to the requirements.txt then you would have to go to TMDB and request your own API key and create a .env file that will contain the api key an example would tmdb*key = 'your-api-here' in the env file. Once you have created the api key if it is named different than the example then you would have to change the variable on line 17 in file tmdb.py where it says "api_key": os.getenv("your_key_name* here"). Since we will be also using a database we need to create one using Heroku. So first 'heroku create' then 'heroku addons:create heroku-postgresql:hobby-dev' -a {your app name}, then 'heroku config'. So once on the command line the link to the database will show up and you copy that till postgres and create a variable in your .env file called DATABASE_URL. So your variable should be something like DATABASE_URL = postgresql {add the link here}. Once this is done you then would have to create another variable called SECRET_KEY, now this can be anything it is just to protect your database. So once this is all done you would run the app.py and if there are no errors then your app will run.

## Difference from Project planning

There are a few differences I had when writing the code. I have not created a models.py for convenience because I did not want to switch over to a different file everytime so I made sure my database was in one file. The second difference was when working on this project I made my login function have '/' because it is the first page the user has to see it is not the full website so it makes it easier to run the code. Those were the differences I noticed while developing this project, it helps that the project works but if it did not then these would be the errors I would look into.

## Two technical problems

1. First problem was that my username was not being added to the database. For this issue I will be honest I was pulling my hair out for and I dont know why it was not being added and turned out that the simple solution to it was that I did not have a return statement. So that made me laugh at myself
2. attributeerror-user-object-has-no-attribute-is-active. This error I ran into while programming and I could not solve it so I figured I did not know what this error was so I might as well google it right. So google first link that pops up is this which helps me solve this problem. https://stackoverflow.com/questions/26606391/flask-login-attributeerror-user-object-has-no-attribute-is-active
3. The error of adding the comments but them showing for every movie instead of the one movie. This one was hard because it was at the end of my project so I messaged Wilbert Liu and he gave me a hint and from there I figured why not make an if statement that will check the entered movie id and will print the comments/ratings for the movie it self rather than other movies combined.
