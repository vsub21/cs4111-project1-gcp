The name and UNI of the members of the team.

Vivek Subramaniam
UNI: vs2575@columbia.edu

Sameer Jain
UNI: sj2736@columbia.edu

The PostgreSQL account where your database on our server resides. (This should be the same database that you used for Part 2, but we need you to confirm that we should check that database.)

vs2575

The URL of your web application.
URL: http://35.196.212.23:8111/

A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.

Original Proposal:

The application will be designed for NBA sports enthusiasts in mind. The database’s entity sets will include players, owners, colleges attended, teams, and geographic locations. Players will be considered as members of various teams in their professional and college careers. Players will have attributes including positions on the court, annual salary, and years having played basketball professionally. Users will be allowed to ask questions about the attributes of players, teams, and team owners. In addition, users will be allowed to ask questions about the relative abilities of specific players when compared to others. Constraints that may exist in this project include a tuple uniqueness constraint to make sure each row in the database for each player is unique. In addition, a key constraint must be created to ensure there is a way to uniquely identify each player.

In this application, users will be able to insert event-level data, including the schedule of games for the upcoming season (Schedule table), update the score within this table, update the wins/losses of the Team table, insert statistics of each player’s performance in a single game (Game table), update the summary statistics of a player for a given season based on changes in the game, etc. Users will also be able to search for certain players and teams and determine the summary statistics of the requested entity in a table. We will be aggregating event-level data, such as the summary statistics of players and their performance each game, and we will also collect dimension-level data on players (such as university, height, player number, team, demographics data, etc.), dimension-level data of teams, a schedule table, a table of managers, coaches, etc. A DBA is also present to oversee all aspects of the database and access all information.

Current Status:

All original goals were met. The following pages were added to add insight on player performance:

- List of Top 5 Scoring Players in a Game
- Number of Player Injuries per Team
- Total Statistics over Player Career
- Average Statistics over Player Career

Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

* List of Top 5 Scoring Players in a Game *

The page is related to our database operations because it looks across all game data and finds the players that scored the most points. We print out all data relating to these 5 top players. This is interesting, because basketball enthusiasts would want to know the best players in a basketball league. Also, coaches would want to know the best players on other teams that they might want to recruit for their own teams. We look for common player id's across various tables.

* Number of Player Injuries per Team *

The page is related to our database operations because it looks across all player and team data and finds the players that are injured. We then find the number of injuries per team. This is interesting, because sports doctors would want to know the teams that need immediate assistance. Coaches would be interested because they want to know how many available players on opposing teams.

* We have used JOINS to make data accessible to the user. As a result, we have removed all ID's and repeated player names. This is very useful because standard users using the database would know players by their names and not their player id's. Likewise, names of courts, coaches, and referees are more commonly known than ID numbers. *  
