import pandas as pd
import spacy
from collections import defaultdict, Counter

# Load the Spacy model
nlp = spacy.load('en_core_web_sm')

# Load the data
df = pd.read_csv('./d_icd_diagnoses.csv', delimiter=',')

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

    if i % 1000 == 0 and i != 0:
        print(f"still fetching {i}, {diagnosis}")

# Count the frequency of each group
group_counts = {group: len(diagnoses) for group, diagnoses in diagnosis_groups.items()}


# Create a new DataFrame
df_new = pd.DataFrame(list(group_counts.items()), columns=['diagnosis_group', 'count'])

# Sort the DataFrame by 'count' in descending order
df_new = df_new.sort_values('count', ascending=False)

# Reset the index
df_new.reset_index(drop=True, inplace=True)

# Write the DataFrame to a new CSV file
df_new.to_csv('grouped_diagnoses.csv', index=False)

# # Sort the groups by their frequency and get the top 3
# top_3_groups = Counter(group_counts).most_common(3)

# print(f"The top 3 most common diagnosis groups are:")
# for group, count in top_3_groups:
#     print(f"'{group}' with a count of {count}.")
    

# The top 3 most common diagnosis groups are:
# 'Chronic intestinal amebiasis without mention of abscess' with a count of 28168.
# 'Cholera, unspecified' with a count of 13497.
# 'Infectious colitis, enteritis, and gastroenteritis' with a count of 5523.

"""
System:
You are a professional medical assistant, and you can always give detailed treatment based on acurate patient info. 

The treatment you give should refer to the patient info, data (temperature, blood pressure) and symptoms.

Pls be careful and accurate, this is a good learning source for medical students.

USER:
A 42 years old male patient is diagnosised as Chronic intestinal amebiasis. His body temperature is currently 39 \
Degrees Celsius, blood pressure systolic over 168 and heart rate is around 120 bpm. However, there is nothing \
severe reaction to this disease. What's a possible treatment based on this info?

ASSISTANT:
For chronic intestinal amebiasis, a common treatment involves a combination of medications, including metronidazole \
and paromomycin. However, the patient's elevated temperature and high blood pressure may require additional treatment \
to manage those symptoms.

To bring down the patient's fever and manage any discomfort, acetaminophen or ibuprofen can be given. Antihypertensive \
medications, such as angiotensin-converting enzyme inhibitors (ACE inhibitors) or calcium channel blockers may be prescribed \
to manage the patient's blood pressure.

It is important to monitor the patient's symptoms and vital signs closely to ensure that the treatment is working effectively \
and to identify any potential complications. Regular follow-up appointments and tests, such as stool cultures, may also be \
necessary to monitor the progress of the disease.
"""


"""
System:
You are a professional medical assistant, and your job is to argue medical students' treatment in high order reasoning way, \
whcih includes Why, How, What if, How does and so on.

The real patient info including gender, age, color, data (temperature, blood pressure) and symptoms have been provided. And \
you are expexted to argue medical students' treatment which might have mistakes. Remeber to make reference to this real info \
as much as possible.

The response format should be like this example.
Why: I think this treatment is appropriate (improper), because...
How: To make the treatment better, you should consider...
What if: This treatment looks good in most parts, but what if you modify...

Pls be careful and accurate, this is a good learning source for medical students.

USER:
Patient Info:
A 42 years old male patient is diagnosised as Chronic intestinal amebiasis. His body temperature is currently 39 Degrees Celsius, \
blood pressure systolic over 168 and heart rate is around 120 bpm. However, there is nothing severe reaction to this disease. \
What's a possible treatment based on this info?

Student Treatment:
For chronic intestinal amebiasis, a common treatment involves a combination of medications, including metronidazole and paromomycin. \
However, the patient's elevated temperature and high blood pressure may require additional treatment to manage those symptoms.

To bring down the patient's fever and manage any discomfort, acetaminophen or ibuprofen can be given. Antihypertensive medications, \
such as angiotensin-converting enzyme inhibitors (ACE inhibitors) or calcium channel blockers may be prescribed to manage the patient's \
blood pressure.

It is important to monitor the patient's symptoms and vital signs closely to ensure that the treatment is working effectively and to \
identify any potential complications. Regular follow-up appointments and tests, such as stool cultures, may also be necessary to monitor \
the progress of the disease.

ASSISTANT (Turbo):
Why: I think this treatment is appropriate to some extent, but there are some concerns.
How: To make the treatment better, you should consider adjusting the dosage of the medications prescribed for the patient, depending on \
    his body weight, and creating a personalized treatment plan considering the patient's age and medical history. 
What if: This treatment looks good in most parts. However, what if the patient doesn't respond well to the prescribed medication? \
    In such cases, it would be important to reevaluate the diagnosis and consider other treatment options such as nitroimidazoles or \
    combination therapy. Additionally, lifestyle modifications such as a high-fiber diet and regular exercise can help manage the \
    symptoms of chronic intestinal amebiasis and lower blood pressure.

ASSISTANT (GPT-4):
Why: I agree that your proposed treatment is generally appropriate because chronic intestinal amebiasis is often treated with \
    anti-parasitic medications such as metronidazole and paromomycin, which are designed to eradicate the infecting organism. \
    However, the patient's high fever and high blood pressure could be indicative of a systemic response or a different underlying \
    condition that requires additional treatment. The use of antipyretics like acetaminophen and antihypertensive drugs such as ACE \
    inhibitors can be beneficial, but the root cause of these symptoms must be evaluated as well.

How: To make this treatment plan better, you should also consider the patient's hydration status. Given the patient's fever and the \
    nature of intestinal amebiasis, which can lead to diarrhea, the patient might be at risk of dehydration. Hence, ensuring the patient \
    has adequate fluid intake, and providing IV fluids if necessary, should be a crucial part of the treatment plan.

What if: This treatment looks good for the most part, but what if we also incorporated probiotics into the regimen? Research suggests \
    that probiotics may promote gut health and assist in recovery from infections like amebiasis. This could help restore the balance of \
    beneficial gut bacteria that may have been disrupted by the infection and the treatment.

How does: Understanding the mechanism of action of your prescribed treatments will help you make better decisions. Metronidazole works \
    by damaging the DNA of the microorganisms, which prevents them from reproducing and spreading. Paromomycin, on the other hand, \
    works by interfering with protein synthesis within the ameba, effectively killing them. For the antihypertensive medications, \
    ACE inhibitors work by inhibiting the formation of angiotensin II, a molecule that constricts blood vessels, thereby reducing \
    blood pressure.

Additionally, it would be necessary to carefully monitor the potential side effects of these medications. Metronidazole, for instance, \
can cause nausea, vomiting, and even neurological symptoms in some cases. Also, antihypertensive medications should be managed appropriately \
to avoid sudden drops in blood pressure. Regular check-ups and necessary investigations can help detect any potential complications early.

ASSISTANT (BARD):

I think the medical student's treatment plan is generally appropriate, but there are a few things that could be improved.

First, the student should consider using a combination of medications to treat the chronic intestinal amebiasis. Metronidazole \
is a good choice for treating this infection, but it is not always effective on its own. Paromomycin can be used in combination \
with metronidazole to improve the chances of a successful outcome.

Second, the student should monitor the patient's temperature and blood pressure closely. The patient's elevated temperature and \
high blood pressure may be a sign of a more serious infection, such as sepsis. If the patient's temperature or blood pressure does \
not improve with treatment, the student should consider consulting with a physician.

Finally, the student should educate the patient about the importance of completing the entire course of treatment, even if they \
start to feel better. Stopping treatment early can increase the risk of the infection recurring.

Here is a possible treatment plan:

Metronidazole 500 mg orally three times daily for 7 days
Paromomycin 30 mg/kg orally three times daily for 7 days
Monitor temperature and blood pressure closely
Educate patient about the importance of completing the entire course of treatment
I hope this helps!

ASSISTANT (Claude):
Here are my arguments for the student's treatment:
Why: I think this treatment for chronic intestinal amebiasis is appropriate because metronidazole and paromomycin are effective \
    medications for eliminating Entamoeba histolytica infection. Managing the patient's symptoms and vital signs is also necessary. 
How: To improve the treatment, the student should also consider:
1. Prescribing oral rehydration salts to prevent dehydration from diarrhea.
2. Monitoring the patient's electrolyte levels and supplementing if needed. Electrolyte imbalance can occur with severe diarrhea.
3. Considering corticosteroids in cases of severe inflammation or dysentery. This can help reduce inflammation in the intestines.

What if: This treatment looks good, but what if the patient does not respond to the initial medications or his symptoms worsen? \
    In that case, other anti-amebic drugs like tinidazole or nitroimidazole may need to be tried. If there are signs of toxic \
    megacolon or perforation, hospitalization and emergency surgery may be required. 

How does: How does the high fever and blood pressure relate to the intestinal amebiasis? The fever is likely due to the infection \
    and inflammation in the intestines. The elevated blood pressure may be due to pain, stress, or electrolyte imbalance from the \
    diarrhea. It's important to manage these symptoms along with treating the underlying infection.

Overall, this student has proposed an appropriate treatment plan for chronic intestinal amebiasis. My additional comments and \
    considerations can help strengthen the plan and prepare for potential complications. Please let me know if you have any other \
    questions!

"""