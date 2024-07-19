#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier

##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
    def __init__(self, theMovie_ID, theTitle, theRelease_Year):
        
       self._Movie_ID = theMovie_ID
       self._Title = theTitle
       self._Release_Year = theRelease_Year

    @property
    def Movie_ID(self):
        return self._Movie_ID
 
    @property
    def Title(self):
        return self._Title
 
    @property
    def Release_Year(self):
        return self._Release_Year

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
    
    def __init__(self, theMovie_ID, theTitle, theRelease_Year, nReviews, avgRating):
       
       self._Movie_ID = theMovie_ID
       self._Title = theTitle
       self._Release_Year = theRelease_Year
       self._Num_Reviews = nReviews
       self._Avg_Rating = avgRating
       
    @property
    def Movie_ID(self):
        return self._Movie_ID
       
    @property
    def Title(self):
        return self._Title
       
    @property
    def Release_Year(self):
        return self._Release_Year
        
    @property
    def Num_Reviews(self):
        return self._Num_Reviews
        
    @property
    def Avg_Rating(self):
        return self._Avg_Rating
        
##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
    
    def __init__(self, theMovie_ID, theTitle, theRelease_Date, theRuntime, origLanguage, 
                 theBudget, theRevenue, nReviews, avgRating, theTagline, theGenres = [], prodCompanies = []):
        
       self._Movie_ID = theMovie_ID
       self._Title = theTitle
       self._Release_Date = theRelease_Date
       self._Runtime = theRuntime
       self._Original_Language = origLanguage
       self._Budget = theBudget
       self._Revenue = theRevenue
       self._Num_Reviews = nReviews
       self._Avg_Rating = avgRating
       self._Tagline = theTagline
       self._Genres = theGenres
       self._Production_Companies = prodCompanies
       
    @property
    def Movie_ID(self):
        return self._Movie_ID
       
    @property
    def Title(self):
        return self._Title
       
    @property
    def Release_Date(self):
        return self._Release_Date
        
    @property
    def Runtime(self):
        return self._Runtime
        
    @property
    def Original_Language(self):
        return self._Original_Language
       
    @property
    def Budget(self):
        return self._Budget
       
    @property
    def Revenue(self):
        return self._Revenue
       
    @property
    def Num_Reviews(self):
        return self._Num_Reviews
        
    @property
    def Avg_Rating(self):
        return self._Avg_Rating
        
    @property
    def Tagline(self):
        return self._Tagline
       
    @property
    def Genres(self):
        return self._Genres
        
    @property
    def Production_Companies(self):
        return self._Production_Companies
        
##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
   sql = ("SELECT COUNT(MOVIE_ID) "
          "FROM Movies ")
   row = datatier.select_one_row(dbConn, sql)
   
   if row is None:
       return -1
   else:
       return row[0]
   
##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    sql = ("SELECT COUNT(Rating) "
           "FROM Ratings ")
    row = datatier.select_one_row(dbConn, sql)
    
    if row is None:
        return -1
    else:
        return row[0]

##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
   sql = ("SELECT Movie_ID, Title, strftime('%Y', Release_Date) "
          "FROM Movies "
          "WHERE Title LIKE ? "
          "ORDER BY Title ASC")

   rows = datatier.select_n_rows(dbConn, sql, [pattern])

   if rows is None:
       return []
  
   M = [] 
   for row in rows:
       
       # Create Movie Object
       nextMovie = Movie(row[0], row[1], row[2])
       # Append Movie Object to List
       M.append(nextMovie)

   return M;

def moviesSQL(dbConn, movie_id):
    # Movie details Query
    movieSql = ("SELECT Movie_ID, Title, date(Release_Date), Runtime, Original_Language, Budget, Revenue "
               "FROM Movies " 
               "Where Movie_ID = ? ")
    movieDataRow = datatier.select_one_row(dbConn, movieSql, [movie_id])
    if len(movieDataRow) == 0:
        return None
    else:
        return movieDataRow

def ratingsSQL(dbConn, movie_id):
    
    # Number of reviews and sum of ratings Query
    #  -ratCountAndSum[0] has total number of reviews
    #  -ratCountAndSum[1] has the sum of ratings
    ratingSql = ("SELECT COUNT(Rating), SUM(Rating) "
                 "FROM Ratings "
                 "Where Movie_ID = ? ")
    
    return datatier.select_one_row(dbConn, ratingSql, [movie_id])

def movie_TaglinesSQL(dbConn, movie_id):
   # Tagline Query
    taglineSql = ("SELECT Tagline "
                 "FROM Movie_Taglines "
                 "Where Movie_ID = ?")
    taglineRow = datatier.select_one_row(dbConn, taglineSql, [movie_id])
    
    tagline = ""
    if len(taglineRow) != 0:
        tagline = taglineRow[0]
               
    return tagline

def genresSQL(dbConn, movie_id):
    # Genres Query
     genresSql = ("SELECT Genre_Name "
                 "FROM Movie_Genres "
                 "JOIN Genres ON(Movie_Genres.Genre_ID = Genres.Genre_ID) "
                 "WHERE Movie_ID = ? "
                 "ORDER BY Genre_Name")
     genresRows = datatier.select_n_rows(dbConn, genresSql, [movie_id])
     genresList = []
     
     if len(genresRows) != 0:
         for row in genresRows:
            genresList.append(row[0])
            
     return genresList
   
def prodCompaniesSQL(dbConn, movie_id):
     # Production Companies Query
     prodCompaniesSql = ("SELECT Company_Name "
                        "FROM Movie_Production_Companies "
                        "JOIN Companies ON(Movie_Production_Companies.Company_ID = Companies.Company_ID) "
                        "Where Movie_ID = ? "
                        "ORDER BY Company_Name ")
     prodCompaniesRows = datatier.select_n_rows(dbConn, prodCompaniesSql, [movie_id])
     prodCompaniesList = []
     
     if len(prodCompaniesRows) != 0:
         for row in prodCompaniesRows:
            prodCompaniesList.append(row[0])
            
     return prodCompaniesList
##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
    
    movieDataRow = moviesSQL(dbConn,movie_id)
    
    if movieDataRow is None:
        return None
    
    ratCountAndSumRow = ratingsSQL(dbConn, movie_id) 
    
    num_reviews = ratCountAndSumRow[0]
    avgRating = 0
    
    if num_reviews != 0:    
        avgRating = ratCountAndSumRow[1]/ratCountAndSumRow[0] # calculate average

    tagline = movie_TaglinesSQL(dbConn, movie_id)

    genresList = genresSQL(dbConn, movie_id)
  
    prodCompaniesList = prodCompaniesSQL(dbConn, movie_id)

    return MovieDetails(movieDataRow[0], #Movie_ID
                        movieDataRow[1], #Title
                        movieDataRow[2], #Release_Date
                        movieDataRow[3], #Runtime
                        movieDataRow[4], #Original_Language
                        movieDataRow[5], #Budget
                        movieDataRow[6], #Revenue
                        num_reviews, #Num_Reviews
                        avgRating,          #Avg_Rating
                        tagline,            #Tagline
                        genresList,         #Genres
                        prodCompaniesList)  #Production_Companies

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
    
    sql = ("SELECT Movies.Movie_ID, Title, strftime('%Y', Release_Date), COUNT(Rating) as num_reviews, SUM(Rating)*1.0/COUNT(Rating) as avgRating "
          "FROM Movies "
          "JOIN Ratings ON(Movies.Movie_ID = Ratings.Movie_ID) "
          "GROUP BY Movies.Movie_ID "
          "HAVING num_reviews >= ? "
          "ORDER BY avgRating DESC "
          "LIMIT ? ")
    
    movieRows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N]) 
    
    moviesList = []
    # order of data in row:
    #  movie_id, title, release date, number of reviews, average rating
    for row in movieRows:
       nextMovie = MovieRating(row[0], row[1], row[2], row[3], row[4]) 
       moviesList.append(nextMovie)
      
    return moviesList

    
##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
    checkSql = ("SELECT distinct Movie_ID " 
           "FROM Movies "
           "Where Movie_ID = ?")  # Query just to check whether movie actually exists
    row = datatier.select_one_row(dbConn, checkSql, [movie_id])
    
    if len(row) == 0: # movie_id was not found
        return 0
    else:
        sql = ("INSERT INTO Ratings(Movie_ID, Rating) "
               "VALUES(?, ?)")  # So we INSERT
        datatier.perform_action(dbConn, sql, [movie_id, rating])
        return 1
    
##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    checkSql = ("SELECT Movie_ID "
                "FROM Movies "
                "Where Movie_ID = ?")    # Query just to check whether movie actually exists
    row = datatier.select_one_row(dbConn, checkSql, [movie_id])
    
    if len(row) == 0: # movie_id does not exist
        return 0
    else:       # movie exists
        checkSql = ("SELECT Tagline "
                    "FROM Movie_Taglines "
                    "Where Movie_ID = ?")  # Query just to check whether movie has a tagline
        row = datatier.select_one_row(dbConn, checkSql, [movie_id])
        
        if len(row) == 0: # tagline does not exist
            sql = ("INSERT INTO Movie_Taglines(Movie_ID, Tagline) "
               "VALUES(?, ?)")      # So we INSERT
            datatier.perform_action(dbConn, sql, [movie_id, tagline])
            return 1
        else: #tagline exists
            sql =  ("UPDATE Movie_Taglines "
                    "SET Tagline = ? "
                    "WHERE Movie_ID = ? ")   # So we UPDATE
            datatier.perform_action(dbConn, sql, [tagline, movie_id])
            return 1
    