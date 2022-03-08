# Git-Voting-Tests
Repository to test the feasibility of using GitHub as a neutral voting platform.

# Game Rules
* Everyone gets 10 votes.
* All players get to allocate their votes to the contended projects.
* The projects will be resolved in descending order of total votes. (Ties are broken by descending order of project name)

* The resolve is as follows:
    1. Allocate integer ranges based on how many votes each player put into the project
    2. A random integer is chosen in the range
    3. The player who owns the range wins the project. Their votes in other projects are voided.

* If after the game is played, there are still leftover players and projects, the game is played again with the remaining players and projects.

*Step 1 of the resolve will allocate integer ranges in descending order of votes. (Ties broken in descending order of player name)*
