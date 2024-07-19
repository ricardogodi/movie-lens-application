#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 12:12:29 2022

@author: Ricardo Gonzalez
"""
import sqlite3
import objecttier

def print_genStats(dbConn):
    print("\nGeneral stats:")
    numMovies = objecttier.num_movies(dbConn)
    numReviews = objecttier.num_reviews(dbConn)
    print("  # of movies:", f"{numMovies:,}")
    print("  # of reviews:",f"{numReviews:,}\n" )
    
def cmnd1(dbConn):
    movieName = input("\nEnter movie name (wildcards _ and % supported): ")
    moviesFound = objecttier.get_movies(dbConn, movieName)
    print("\n# of movies found:", len(moviesFound))
    
    if len(moviesFound) > 100:
        print("There are too many movies to display, please narrow your search and try again...")
        return
    
    print()
    for movie in moviesFound:
        print(movie.Movie_ID,":",movie.Title,f"({movie.Release_Year})")  
    print()


def cmnd2(dbConn):
    movieID = input("\nEnter movie id: ")
    movie = objecttier.get_movie_details(dbConn, movieID) 
    
    print()
    if movie is None:
        print("No such movie...\n")
        return
    
    print(movie.Movie_ID,":", movie.Title)
    print("  Release date:", movie.Release_Date)
    print("  Runtime:", movie.Runtime, "(mins)")
    print("  Orig language:", movie.Original_Language)
    print("  Budget:", f"${movie.Budget:,} (USD)" )
    print("  Revenue:", f"${movie.Revenue:,} (USD)" )
    print("  Num reviews:", movie.Num_Reviews)
    print("  Avg rating:", '{:.2f}'.format(movie.Avg_Rating),"(0..10)")
    
    print("  Genres:" ,end =" ")
    for genre in movie.Genres:
       print(genre + ",", end =" ")  
    print()
   
    print("  Production companies:" ,end =" ")
    for company in movie.Production_Companies:
       print(company + ",", end =" ")  
    print()
    print("  Tagline:", movie.Tagline)
    print()
    
def cmnd3(dbConn):
    N = int(input("\nN? "))
    if N <= 0:
        print("Please enter a positive value for N...\n")
        return
    
    min_num_reviews = int(input("min number of reviews? "))

    if min_num_reviews <= 0:
        print("Please enter a positive value for min number of reviews...\n")
        return
    
    print()
    topNMovies = objecttier.get_top_N_movies(dbConn, N, min_num_reviews) 
    
    if len(topNMovies) == 0 :
        return
    
    for movie in topNMovies:
        print(movie.Movie_ID,":", movie.Title, f"({movie.Release_Year}),", 
                 "avg rating =", '{:.2f}'.format(movie.Avg_Rating), f"({movie.Num_Reviews} reviews)")
    print()
    
def cmnd4(dbConn):
        
        rating = int(input("\nEnter rating (0..10): "))
        if rating < 0 or rating > 10:
            print("Invalid rating...\n")
            return
        
        movie_id = int(input("Enter movie id: "))
        
        movieFound = objecttier.add_review(dbConn, movie_id, rating)
        
        print()
        if movieFound == 0:
            print("No such movie...\n")
            return
        else:
            print("Review successfully inserted\n")
            
def cmnd5(dbConn):
        tagline = input("\ntagline? ")
        movie_id = int(input("movie id? "))
        
        movieFound = objecttier.set_tagline(dbConn, movie_id, tagline)
        
        print()
        if movieFound == 0:
            print("No such movie...\n")
            return
        else:
            print("Tagline successfully set\n")
    
##################################################################  
#
# main
#
print('** Welcome to the MovieLens app **')
dbConn = sqlite3.connect('MovieLens.db')
print_genStats(dbConn)

while True:
    userInput = input("Enter a command (1: Search Movies, 2: View Movie Details, 3: Top Rated Movies, 4: Add Review, 5: Set/Update Tagline, x to exit): ")
    if userInput == '1':
       cmnd1(dbConn)
       
    elif userInput == '2':
        cmnd2(dbConn)
        
    elif userInput == '3':
         cmnd3(dbConn)
         
    elif userInput == '4':
         cmnd4(dbConn)
         
    elif userInput == '5':
      cmnd5(dbConn)
        
    elif userInput == 'x':
        break
    else: 
        print("**Error, unknown command, try again...\n")
        continue
# done
#
