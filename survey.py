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

# Read the features from the file
def get_features():
    # Get the name of the survey
    survey_name = get_survey_name()
    # Read the features from the file
    with open(f"surveys/{survey_name}.txt") as f:
        features = f.read().splitlines()
    return features

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

# Ask the user questions about the features
def ask_about_features(features):
    # Create a list to hold the answers
    answers = []
    # Ask the user a question about each feature
    for feature in features:
        answer = ask_about_one_feature(feature)
        answers.append(answer)
    return answers

# Ask the user a question about a feature and return the answer
def ask_about_one_feature(feature):
    st.info(feature)
    col1, col2 = st.columns(2)
    with col1:
        functional = st.radio("How would you feel about this feature?", levels, key=f"{feature} F")
    with col2:
        dysfunctional = st.radio("How would you feel if there was no such feature?", levels, key=f"{feature} D")
    return functional, dysfunctional

# Add the answers to the file
# The file is a CSV file with the following columns: feature and answer
def add_answers(filename, features, answers):
    with open(filename, 'a') as f:
        for feature, answer in zip(features, answers):
            f.write(f"{feature},{answer[0]},{answer[1]}\n")

st.header('Survey')
st.markdown('''
Thank you for taking the time to complete this survey.
''')

# Create a form with a feature and a submit button
with st.form(key='survey'):
    features = get_features()
    answers = ask_about_features(features)
    survey_submitted = st.form_submit_button(label='Submit')

# When the user submits the form, add the answer to the file
if survey_submitted:
    # Get the name of the survey
    survey_name = get_survey_name()
    # To prevent multiple users from adding to the same file, the file is locked
    if acquire_lock(f"data/{survey_name}.lock"):
        add_answers(f"data/{survey_name}.csv", features, answers)
        release_lock(f"data/{survey_name}.lock")
    else:
        st.error("A problem occurred. Try again later.")
