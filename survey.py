import streamlit as st

import os
import time

# Create a survey app that collects the user's rating from the levels listed below
levels = ["Like it", "Expect it", "Don't care", "Can live with it", "Dislike it"]

# Each survey has a name that (in lowercase) is used as the filename for the survey
# When the user completes a survey, their answer is added to the file

# Get the name of the survey from the URL
def get_survey_name():
    # Get URL parameters
    params = st.experimental_get_query_params()
    # Get the name parameter
    name = params.get('s', ['survey'])[0]
    # Return the name in lowercase
    return name.lower()

# Acquire the lock
def acquire_lock(lockfile):
    # Try to acquire the lock every 1 second for 5 seconds
    attempts = 5
    while attempts > 0:
        if os.path.exists(lockfile):
            attempts -= 1
            time.sleep(1)
        else:
            open(lockfile, 'a').close()
            # If the lock is acquired, return True
            return True
    # If the lock is not acquired, return False
    return False

# Release the lock
def release_lock(lockfile):
    # Release the lock from the lockfile
    os.remove(lockfile)

# Ask the user a question about a feature and return the answer
def ask_about_feature(feature):
    st.info(feature)
    answer = st.radio("How would you feel about this feature?", levels, key=f"{feature}")
    return answer

# Add the answer to the file
# The file is a CSV file with the following columns: feature and answer
def add_answer(filename, feature, answer):
    # Append the answer to the file
    with open(filename, 'a') as f:
        f.write(f"{feature},{answer}\n")

st.header('Survey')
st.markdown('''
This is a survey app.
''')

# Create a form with a feature and a submit button
with st.form(key='survey'):
    feature1 = ask_about_feature("Feature 1")
    survey_submitted = st.form_submit_button(label='Submit')

# When the user submits the form, add the answer to the file
if survey_submitted:
    # Get the name of the survey
    survey_name = get_survey_name()
    # To prevent multiple users from adding to the same file, the file is locked
    if acquire_lock(f"{survey_name}.lock"):
        add_answer(f"{survey_name}.csv", 'Feature 1', feature1)
        release_lock(f"{survey_name}.lock")
    else:
        st.error("A problem occurred. Try again later.")

