# Movie-Database
This is a a Movie Database project rest api using django rest framework where user can See the list and details of the movies, apart from that they can `create`, `view`, `delete` the *watchlater* list as well.

Following are the capability of the projects- 
-list Movies,
-Detail Movies
-logged in users can save movies to a watchlist or mark them watched.  
-logged in users can view a list of movies in their watchlist or watched list.

To populate the movies in your database, we have a scraper to scrape IMDb’s top list (https://www.imdb.com/chart/top/). This scrapper follow each movie’s url and extract details from the movie’s page. This scraper should ideally be triggered by an endpoint in your django api and accept any similar url e.g. https://www.imdb.com/india/top-rated-indian-movies.
Already existing movies should be only updated. Not replaced/duplicated.





## To see the API Documentations please follow following URL

https://documenter.getpostman.com/view/3153512/TVCb3pi2
