# HydrateU

HydrateU is a website designed for the user to keep track of their hydration by recording daily glasses, setting hydration goals for that day, seeing a "calendar" of
the glasses they have logged, as well as having access to their hydration statistics such as days they have met their goal, days they have
not, and other relevant statistics. The site also includes webpages for the user to educate themselves on the global water crisis, as well
as another menu to learn more about organizations in the space and accordingly donate.
## Installation

HydrateU is currently housed on the CS50 IDE. To begin running the application in the IDE, run,

```bash
flask run
```
This will create a temporary server where you can see HydrateU.

## Usage

HydrateU makes use of the CS50 IDE (where it is housed), as well as Flask (also Session), Bootstrap, and SQLite. The site is built in HTML, CSS, and Python.
A few of the files with pertinent information include:

   -Static
        -Includes the folder "images" with the images the site has
        -styles.ccs, the CSS file the website uses

   -Templates
        -All of the webpage templates the site renders, including layout.html
        -application.py, where the Python code directing the website is sdtored
        -helpers.py, where helper functions like "apology" are stored
        -hydrateU.db, a database configured with SQLite
            -Has two tables
                -Users (keeps track of users registered)
                    -id [id of users]
                    -username
                    -hash [hash of password]
                    -first name
                    -last name
                    -goal [not relevant to rest of site, includes standard goal of 8]
                -Daily Goals (keeps track of goals/progress of a user by DAY)
                    -goal_id
                    -user_id
                    -goal [goal set by user]
                    -reachedGoal [boolean if the daily goal was reached]
                    -glassesDrank [glasses drank by the user that day]
                    -date
    -Preposal/proposal/status folders have documentation regarding progress of the project

For someone to run this website, they would require all of the contents of the hydrateU folder in addition to access to Flask, Bootstrap,
and SQLite. To compile, one must cd into the hydrateU folder and use Flask to host the site on a temporary server. To configure
any of the HTML code, look to the templates in the template folder (layout.html in particular controls the "foundation" for the other webpages).
To configure CSS, modify the styles.css folder under the static folder. To add or modify Python elements of the site, configure/modify application.py
(if wanting to modify Python helper functions, open helpers.py). Access and modify the databases via hydrateU.db, which includes the
users (keeps track of users registered) and dailyGoals (daily data per user) tables.

For a user to use the site, they must register using the register webpage (their information is then saved to the users table). They can then
login to the site using the login tab, where their credentials are checked using application.py and hydrateU.db.
