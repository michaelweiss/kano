import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
import re
import textwrap

# Host and port for the survey app
HOST = "localhost"
PORT = 8501

# Create a Kano analysis app that reads the user's ratings of features and
# plots them on a Kano chart (using a scatter plot)

# Each survey has a name that (in lowercase) is used as the filename for the survey

# Get the name of the survey from the URL
def get_survey_name():
    # Get URL parameters
    params = st.experimental_get_query_params()
    # Get the name parameter
    name = params.get('s', [''])[0]
    # Return the name in lowercase
    return name.lower()

# Check if the file for the survey exists
def check_survey_name(survey_name):
    # Check if the file exists
    if os.path.exists(f"surveys/{survey_name}.txt"):
        return True
    return False

# Check if the file for the survey data exists
def check_survey_data(survey_name):
    # Check if the file exists
    if os.path.exists(f"data/{survey_name}.csv"):
        return True
    return False

# Check if the survey name is well-formed
# The name must be a single word with only letters and numbers, dashes and underscores
def is_survey_name_well_formed(survey_name):
    # Check if the name contains only letters, numbers, dashes and underscores
    # using a regular expression
    return re.match(r'^[a-zA-Z0-9_-]+$', survey_name)

# Save the feature names for a new survey
def save_survey(survey_name, feature_names):
    with open(f"surveys/{survey_name}.txt", 'w') as f:
        f.write(f"{feature_names}")

# Each feature is rated on a scale with the levels listed below
levels = ["Like it", "Expect it", "Don't care", "Can live with it", "Dislike it"]

# Convert a level to a value on a scale of 1 to 5
# If inverse is True, the scale is reversed. This is used for dysfunctional ratings
def rating(level, inverse=False):
    if level == "Like it":
        value = 1
    elif level == "Expect it":
        value = 2
    elif level == "Don't care":
        value = 3
    elif level == "Can live with it":
        value = 4
    elif level == "Dislike it":
        value = 5
    if inverse:
        return 6 - value
    return value

# Read the features from the file
# Each row contains the feature name and its functional and dysfunctional ratings
def get_feature_ratings(survey_name):
    # Read the features from the file
    # No header row is included in the file
    df = pd.read_csv(f"data/{survey_name}.csv", header=None)
    # Set the column names
    df.columns = ['Feature', 'Functional', 'Dysfunctional']
    return df

# Convert the ratings to a scale of 1 to 5
def convert_ratings(df):
    # Convert the functional ratings to a scale of 1 to 5 using rating() with inverse=True
    df['Functional'] = df['Functional'].apply(lambda x: rating(x, True))
    # Convert the dysfunctional ratings to a scale of 1 to 5 using rating()
    df['Dysfunctional'] = df['Dysfunctional'].apply(lambda x: rating(x))
    return df

# Compute the average functional and dysfunctional ratings for each feature
def compute_average_ratings(df):
    # Group the data by feature and compute the average functional and dysfunctional ratings
    df = df.groupby('Feature').mean()
    # Reset the index to make the feature names a column
    df = df.reset_index()
    return df

# Create a multi-line string from a string
def multi_line_text(txt, max_width=12, max_lines=2):
    lines = textwrap.wrap(txt, width=max_width, break_long_words=False, max_lines=max_lines)
    return '\n'.join(lines)

# Plot the data on a Kano chart
def plot_kano(df):
    # Convert the ratings from levels to values on a scale of 1 to 5
    df = convert_ratings(df)

    # Subtract 1 from each value to make the scale 0 to 4 to plot the data
    df['Functional'] = df['Functional'] - 1
    df['Dysfunctional'] = df['Dysfunctional'] - 1

    # Compute the average functional and dysfunctional ratings for each feature
    df = compute_average_ratings(df)

    st.markdown('''
    The Kano chart shows the average functional and dysfunctional ratings for each feature.
    ''')
    with st.expander('Show average values'):
        st.dataframe(df)

    transform_value = st.checkbox('Transform values', value=False)
    if transform_value:
        df['Functional'] = transform(df['Functional'])
        df['Dysfunctional'] = transform(df['Dysfunctional'])

    # Create a scatter plot
    fig, ax = plt.subplots()
    # Plot data points as light blue circles of size 100
    ax.scatter(df['Dysfunctional'], df['Functional'], c='lightblue', s=100)

    # Annotation for each data point with feature name
    for i, txt in enumerate(df['Feature']):
        # Place text above and at the center of the data point
        # Limit the number of characters in each line to max length of 10
        ax.annotate(multi_line_text(txt), 
            (df['Dysfunctional'][i], df['Functional'][i]), ha='center', va='center')

    # Set the x and y axes limits
    plt.xlim(-0.5, 4.5)
    plt.ylim(-0.5, 4.5)

    # Set the x and y axes labels
    plt.xlabel('Dysfunctional (absence)')
    plt.ylabel('Functional (presence)')

    # Set the x and y axes ticks
    plt.xticks(np.arange(0, 5, 1))
    plt.yticks(np.arange(0, 5, 1))

    # Set the x and y axes tick labels
    plt.gca().set_xticklabels(levels)
    plt.gca().set_yticklabels(reversed(levels))

    # Show the plot
    st.pyplot(fig)

def transform(values, n=4):
    min_value = values.min()
    max_value = values.max()
    return n * (values - min_value) / (max_value - min_value)

st.header('Kano analysis')
st.markdown('''
Kano analysis is a method for analyzing customer requirements. 
It is used to identify the features that customers want and the features that customers do not want. 
''')

# Get the name of the survey either from the URL from the user
survey_name = get_survey_name()
if not survey_name:
    survey_name = st.text_input('Enter the name of the survey', value='')

# Check if the survey name is well-formed
# If it is, and the survey exists, read the features from the file and show the Kano chart
# Else, show a form to create a new survey
if not is_survey_name_well_formed(survey_name):
    st.error('The survey name must be a single word with only letters and numbers, dashes and underscores')
elif check_survey_name(survey_name):
    # Create a link to the survey
    st.markdown(f'[Take the survey](http://{HOST}:{PORT}/?s={survey_name})')
    # Reload the page to refresh the data
    st.button('Refresh')
    if check_survey_data(survey_name):
        # Read the features from the file
        df = get_feature_ratings(survey_name)
        # Show the features and their ratings
        st.subheader('Survey data')
        st.dataframe(df)
        # Download survey data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label='Download survey data', data=csv, file_name=f'{survey_name}.csv', mime='text/csv')
        # Plot the data on a Kano chart
        plot_kano(df)
    else:
        st.error('There is no data for this survey. Please take the survey.')
else:
    with st.form(key='new_survey'):
        st.markdown('''
        This survey does not yet exist. You can create it by entering the features you want to ask about.
        ''')
        feature_names = st.text_area("New survey (enter one feature per line)", height=150)
        new_survey_submitted = st.form_submit_button("Create survey")
    
    # Save the survey if the user submitted the form
    if new_survey_submitted:
        save_survey(survey_name, feature_names)
