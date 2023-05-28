import pandas as pd
import spacy
from collections import defaultdict, Counter

# Load the Spacy model
nlp = spacy.load('en_core_web_sm')

# Load the data
df = pd.read_csv('/Volumes/Jasonthewha/mimic-iv-0.4/hosp/d_icd_diagnoses.csv', delimiter=',')

# Convert the diagnosis descriptions to Spacy documents
df['long_title'] = df['long_title'].apply(nlp)

# Create a dictionary for the diagnosis groups
diagnosis_groups = defaultdict(list)

# Iterate over the diagnosis descriptions
for i, diagnosis in enumerate(df['long_title']):
    # Assume initially that the diagnosis is a new group
    new_group = True
    # Iterate over the existing groups
    for group, diagnoses in diagnosis_groups.items():
        # If the diagnosis is similar to the group, add it to the group
        if diagnosis.similarity(nlp(group)) > 0.6:  # similarity threshold
            diagnoses.append(diagnosis.text)
            new_group = False
            break
    # If the diagnosis was not similar to any existing group, create a new group
    if new_group:
        diagnosis_groups[diagnosis.text].append(diagnosis.text)

    if i % 1000 == 0:
        print(f"still fetching {i}, {diagnosis}")

# Count the frequency of each group
group_counts = {group: len(diagnoses) for group, diagnoses in diagnosis_groups.items()}

# Sort the groups by their frequency and get the top 3
top_3_groups = Counter(group_counts).most_common(3)

print(f"The top 3 most common diagnosis groups are:")
for group, count in top_3_groups:
    print(f"'{group}' with a count of {count}.")
    

# The top 3 most common diagnosis groups are:
# 'Chronic intestinal amebiasis without mention of abscess' with a count of 28168.
# 'Cholera, unspecified' with a count of 13497.
# 'Infectious colitis, enteritis, and gastroenteritis' with a count of 5523.


Some possible diagnosis has been provided, but this diagnosis actuaaly cones from some college medical student, pls do you best to argue this treatment with high-order reasoning.