MovieLens Database Application

Overview

This Python-based application manages and queries a comprehensive movie database using a layered architectural approach. It integrates data handling and business logic across distinct layers, facilitating interactions with a SQLite database. This enables users to explore movie details, ratings, and reviews with various functionalities.

Architecture Description

	•	Data Access Layer (datatier.py): Handles all SQL operations directly related to the database, including fetching and updating data. This layer abstracts SQL queries and database connections, providing a foundation for operations on movie data.
	•	Business Logic Layer (objecttier.py): Constructs movie-related objects from data retrieved through the data tier. This layer encapsulates the logic needed to transform raw database data into functional objects that represent movies, movie details, and ratings.
	•	Application Layer: This script interacts with the user by parsing inputs and providing command-based interactions. It manages user commands, displays movie information, and interfaces directly with the business logic layer to serve user requests.

Functionality

	•	Search for Movies: Enter a movie name with optional SQL wildcards (_) and (%) to find matching movies in the database.
	•	View Movie Details: Input a movie ID to retrieve and display detailed information about a specific movie, including release date, runtime, ratings, and more.
	•	Top Rated Movies: Specify the number of top-rated movies to display and the minimum number of reviews each must have.
	•	Add a Movie Review: Provide a rating and a movie ID to add a new review for a movie.
	•	Set or Update a Movie’s Tagline: Enter a movie ID and a new tagline to update or add a tagline to a movie’s details.

Makefile

To compile any necessary components or setup the database, use the provided Makefile:
