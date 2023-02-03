import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create a Kano analysis app that reads the user's ratings of features and
# plots them on a Kano chart (using a scatter plot)

# Each survey has a name that (in lowercase) is used as the filename for the survey

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
    # Convert the functional ratings to a scale of 1 to 5 using rating()
    df['Functional'] = df['Functional'].apply(rating)
    # Convert the dysfunctional ratings to a scale of 1 to 5 using rating() with inverse=True
    df['Dysfunctional'] = df['Dysfunctional'].apply(lambda x: rating(x, True))
    return df

# Plot the data on a Kano chart
def plot_kano(df):
    # Convert the ratings from levels to values on a scale of 1 to 5
    df = convert_ratings(df)

    # Subtract 1 from each value to make the scale 0 to 4 to plot the data
    df['Functional'] = df['Functional'] - 1
    df['Dysfunctional'] = df['Dysfunctional'] - 1

    # Create a scatter plot
    fig, ax = plt.subplots()
    # Plot data points as blue circles of size 100
    ax.scatter(df['Dysfunctional'], df['Functional'], color='blue', s=100)

    # Annotation for each data point with feature name
    for i, txt in enumerate(df['Feature']):
        ax.annotate(txt, (df['Dysfunctional'][i] + 0.1, df['Functional'][i] + 0.1))

    # Set the x and y axes limits
    plt.xlim(-0.5, 4.5)
    plt.ylim(-0.5, 4.5)

    # Set the x and y axes labels
    plt.xlabel('Dysfunctional')
    plt.ylabel('Functional')

    # Set the x and y axes ticks
    plt.xticks(np.arange(0, 5, 1))
    plt.yticks(np.arange(0, 5, 1))

    # Set the x and y axes tick labels
    plt.gca().set_xticklabels(levels)
    plt.gca().set_yticklabels(reversed(levels))

    # Show the plot
    st.pyplot(fig)

st.header('Kano analysis')
st.markdown('''
Kano analysis is a method for analyzing customer requirements. 
It is used to identify the features that customers want and the features that customers do not want. 
''')

survey_name = st.text_input('Enter the name of the survey', value='')

if survey_name:
    # Read the features from the file
    df = get_feature_ratings(survey_name)
    # Show the features and their ratings
    st.subheader('Features')
    st.dataframe(df)

    # Plot the data on a Kano chart
    st.subheader('Kano chart')
    plot_kano(df)