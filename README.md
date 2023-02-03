# Purpose
Make an all-in-one app that can be used to survey users and create a Kano model from the survey results, and does not require another app (eg Google forms) to administer a survey.

## Survey
This survey app collects the users's preferences about product feature but asking how they would rate a feature when is present and when it is absent. Present and absent map to functional and dysfunctional in Kano's model. I could not find a simple survey application in streamlit that could write the survey results to a file, so I wrote one.

## Kano
This app reads survey data and produces a Kano model. The y-axis shows the average rating of a feature when it is present in the product, and the x-axis the average rating of a feature when it is absent from the product. 

# Installation
Running the apps requires that streamlit is installed.

You also need to set the HOST and PORT parameters in kano.py to you match your configuration. These parameters are used to create a link to the survey.

# Usage
Start the Survey app on one port (default: 8501) and the Kano app on another port (default: 8502).

Connect to the Kano app to create your first survey. Simply enter the name of the survey, then one feature per line, and submit the survey. Done.

Next, use the "Take a survey" link to connect to the Survey app, or add the name of the survey as a parameter like this: HOST:PORT/?s=SURVEY_NAME. Share this survey link with your users and ask them to complete the survey questions.

Once some survey data is available, you can read the survey data and produce a Kano model.