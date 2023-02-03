import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.header('Kano analysis')
st.markdown('''
Kano analysis is a method for analyzing customer requirements. 
It is used to identify the features that customers want and the features that customers do not want. 
''')

levels = ["Like it", "Expect it", "Don't care", "Can live with it", "Dislike it"]

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

def question(feature):
    st.info(feature)
    col1, col2 = st.columns(2)
    with col1:
        feature_f = st.radio("How would you feel about this feature?", levels, key=f"{feature}_f")
    with col2:
        feature_d = st.radio("How would you feel if this feature was not there?", levels, key=f"{feature}_d")
    return feature_f, feature_d

feature1_f, feature1_d = question("Route search")
feature2_f, feature2_d = question("Training schedule")
feature3_f, feature3_d = question("GPS tracking")
feature4_f, feature4_d = question("Weather info")
feature5_f, feature5_d = question("Social media integration")

# Create a dataframe with functional and dysfunctional ratings
# on a scale of 1 to 5
df = pd.DataFrame({
    'Feature': ['Route search', 'Training schedule', 'GPS tracking', 'Weather info', 'Social media integration'],
    'Functional': [rating(feature1_f, True), rating(feature2_f, True), rating(feature3_f, True), rating(feature4_f, True), rating(feature5_f, True)],
    'Dysfunctional': [rating(feature1_d), rating(feature2_d), rating(feature3_d), rating(feature4_d), rating(feature5_d)]
})
# Subtract 1 from each value to make the scale 0 to 4
df['Functional'] = df['Functional'] - 1
df['Dysfunctional'] = df['Dysfunctional'] - 1

# Create a scatter plot
fig, ax = plt.subplots()
# Plot data points as blue circles of size 100
ax.scatter(df['Dysfunctional'], df['Functional'], color='blue', s=100)

# Annotation for each data point with feature name
for i, txt in enumerate(df['Feature']):
    ax.annotate(txt, (df['Dysfunctional'][i] + 0.1, df['Functional'][i] + 0.1))

ax.set_xlabel('Dysfunctional (absence)')
ax.set_ylabel('Functional (presence)')
ax.set_title('Kano analysis')

# Show grid lines in intervals of 2
ax.set_xticks(np.arange(0, 6, 2))
ax.set_yticks(np.arange(0, 6, 2))
ax.grid(True)

# Display the scatter plot
st.pyplot(fig)