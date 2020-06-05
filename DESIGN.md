# HydrateU (DESIGN)

Once I developed the concept of HydrateU, I initially used design apps to outline, visually, how my website would look from
background images to button colors to submenus. The bulk of HydrateU includes a variety of Bootstrap components from modals, buttons, to Jumbotrons, and cards, plus more


## Structure

    -An index starter page (index.html)
      -Before user logs in
            -This starter page would include the main HydrateU header
            -A mini jingle (Hydrate better. Learn about the global water crisis. Contribute to good.) to convey the purposes of HydrateU
            -A large button to allow the user to "Join"
                -Large to promote engagement
            -Statistics from hydrateU.db – done to promote engagement/interest
                -Number of users using HydrateU
                -Number of glasses logged
                -Average daily goal
            -Two upper-right buttons to allow the user to login if they have an account and/or a smaller register button using Bootstrap components
        -After user logs in
            -A space to update a goal – put on top to encourage the user to maximize their goals
            -Evenly spaced "cards" using Bootstrap
                -Log hydration
                -Learn about the global water crisis
                -Contribute to good

    -A login (login.html) and register (register.html) page, whose information is saved to hydrateU.db

    -A goals page (goals.html)
        -A modal button that allows the user to see that 8 glasses is recommend (created with Bootstrap)
        -A selector to choose their daily goal (starts at 8 to encourage at least the minimum)

    -A hydration log (hydrationLog.html)
        -Allows a user to see their progress
            -A progress bar is included so the user can see how many glasses they must drink to reach the minimum 8 glasses a day
        -Allows a user to see large statistics on how they're doing
            -How many days they have met their goal (in green for success)
             -How many days they haven't met their goal (in red for failure)
             -% of days they have met their goal (in blue for neutral)
        -Allows a user to see a hydration "log"
            -The date of each entry, how many glasses of water they have drank, as well as if they reached their goal (text in green
            for success) and if they hadn't (red for failure)
        -A select to log another glass of water


    -An education page (crisis.html)
        -A page dedicated to the global water crisis
        -Created with multiple Bootstrap components, such as Jumbotrons to emphasize information in large text blocks
        -A layout of Bootstrap components to showcase quotes, facts, and other pieces of pertinent information in order
        for the user to see a variety of content at the same time
        -Videos embedded for the user to interact with active content on the page that still lives on the site

    -A contribute/donation page (contribute.html)
        -Makes use of Bootstrap jumbotrons and embedded videos/images for the user to click on and explore
        -Donation links are BLUE buttons to invite engagement

    -A layout.html page that provided the HTML foundation for the other pages

    -An apology (apology.html) page for returning errors

## Visually
I made the design decision to have three submenus because there were 3 central parts of HydrateU I wanted emphasized – the existence of a
    daily hydration log, learning about the global water crisis, and contributing to various charities. As a result, these can be access at
    the top-right corner of the site after the user can log in. I also made the design decision to host the update goal content bar in index.html
    as I did not see it as a central part of the user experience, and thus, it is not given its own submenu.

I made the decision to use water themed background images to keep to the theme as well as a blue/dark grey/maroon color palette as I found
    it visually appealing. Other design decisions, like making the progress bar green (green for success) were done because of standards and
    less because of individual preferences.

## Technically

hydrate.db has two tables, because I wanted one table to primarily store user credentials (users) and the other to store daily goals for use in statistics and the hydration log (dailyGoals). Thus, users included an id, a username, and their password hash to check credentials in application.py. dailyGoals stored the current date, the goal they have set that day, a boolean value if they've reached their goal (to display in hydration log and for use in statistics) as well as the glasses they have drank for their day.

I split helper functions that would repeat (like apology.py) in helpers.py and the main python code in application.py to separate the "bulk" of functionality.

The intricacies of code are commented within the source code.

I also separated my images from templates, from the rest of files to keep files organized.