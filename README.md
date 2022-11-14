# Movie-Management-API
This API was created using Flask with the help of MongoDB. It includes protected and unprotected routes. Protected routes can only be accessed by logged-in users. Includes ADD, DELETE, UPVOTE/DOWNVOTE, SET FAVOURITE GENRE &amp; SORT BY YEAR OF RELEASE/NAME/VOTES.Coloured buttons in the Movie Center Page are the protected features. 
The application handles login using session and a login_required decorator.

The routes of the application are as follows:

/home (unprotected)

/movie (unprotected)

/sort/name (unprotected)

/sort/year (unprotected)

/sort/votes (unprotected)

/movie/add (protected)

/movie/delete (protected)

/movie/favGenre (protected)

/movie/upvote (protected)

/movie/downvote (protected)

/login

/register

/logout (protected)

The coloured buttons on the /movie route represent protected routes. 
