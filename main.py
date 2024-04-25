import glob
import re

import thefuzz
from thefuzz import fuzz
import pandas as pd


# Author Aidan Scott
# much help with data structure formatting by good ol chatgpt (I barely know how to use pandas)
# parse_math looks through the input file in the input folder and breaks it up into two separate files
# that can be used as data input for a database
# I wanted to use pandas to solve this problem. I think using pandas slowed the processing down quite a bit
# Compared to not using pandas. Just note, this is not very optimized solution.

def parse_math():
    # Load data up using the file in input
    csv_files = glob.glob('input/*.csv')
    if len(csv_files) == 0:
        print('No csv files in input, please add Math csv file in input')
        return False
    if len(csv_files) > 1:
        print('Too many csv files in directory input, please only have one csv file in directory')
        return False
    try:
        df_2015 = pd.read_csv(csv_files[0])
        print(f"File {csv_files[0]} found")
    except FileNotFoundError:
        print('File not found.')
        return False

    # Creating empty DataFrames for institutions and teams with specified columns
    institutions_cols = ['Institution ID', 'Institution Name', 'City', 'State/Province', 'Country']
    teams_cols = ['Team Number', 'Advisor', 'Problem', 'Ranking', 'Institution ID']
    # Actually creating the dataframes
    df_institutions = pd.DataFrame(columns=institutions_cols)
    df_teams = pd.DataFrame(columns=teams_cols)

    # Dictionary to map institution names to generated Institution IDs
    institution_ids = {}
    institution_teams = {}

    # Iterate over each row in the original DataFrame
    for index, row in df_2015.iterrows():
        # normalize that data!
        row = normalize_data(row)
        institution_name = row['Institution']  # get the value for institution, used as a dictionary key
        # Check if the institution is already in the institutions DataFrame TODO fuzzy matching
        if institution_name not in institution_ids:
            # If not, add it with a new Institution ID
            new_id = len(institution_ids) + 1  # Generate a new ID (simple increment)
            institution_ids[institution_name] = new_id  # Add the new institution name to the dictionary
            # adding institution to team number tracker
            institution_teams[institution_name] = 0
            # Create the dataframe that will be concatenated with the institutions dataframe
            institute_data = pd.DataFrame([{
                'Institution ID': new_id,
                'Institution Name': institution_name,
                'City': row['City'],
                'State/Province': row['State/Province'],
                'Country': row['Country']
            }])
            # Concatenate, while ignoring the indexes
            df_institutions = pd.concat([df_institutions, institute_data], ignore_index=True)

        # incrementing number of institution teams by 1
        institution_teams[institution_name] = institution_teams[institution_name] + 1
        # Add the team's information to the teams DataFrame (every row has the data of a time)
        team_date = pd.DataFrame([{
            'Team Number': row['Team Number'],
            'Advisor': row['Advisor'],
            'Problem': row['Problem'],
            'Ranking': row['Ranking'],
            'Institution ID': institution_ids[institution_name]
        }])
        # Concatenate
        df_teams = pd.concat([df_teams, team_date], ignore_index=True)
        # Print status of the current running job
        percent = f"{(index * 100 / len(df_2015))}"
        print(f"Processing {percent[:4]}% complete", end='\r')

    # make it all nice and neat!
    df_institutions = df_institutions.sort_values('Institution Name')
    df_teams = df_teams.sort_values('Team Number')
    # Save that data
    save_data(df_institutions, df_teams, institution_teams)
    print("Processing 100% complete", end='\r')
    return True


def normalize_data(data: pd.Series) -> pd.Series:
    # Loop through columns
    for column in data.index:
        # if the data is a string
        if isinstance(data[column], str):
            # get rid of strange characters
            data[column] = data[column].strip('"')
            data[column] = data[column].strip('.')
            data[column] = data[column].replace('&', 'and')
            # lowercase all letters
            data[column] = data[column].lower()
            # normalize spaces
            data[column] = re.sub(r'\s+', ' ', data[column]).strip()

    return data;


def save_data(institutions: pd.DataFrame, teams: pd.DataFrame, number: dict):
    # formatting df
    list_by_team_number = institutions[['Institution Name']]
    list_by_team_number['Team Number'] = institutions['Institution Name'].map(number)
    list_by_team_number = list_by_team_number.sort_values('Team Number', ascending=False)
    merged_df = pd.merge(institutions, teams, on='Institution ID')
    outstanding = merged_df[merged_df['Ranking'] == 'outstanding winner'][['Institution Name', 'Country']]
    outstanding = outstanding.sort_values('Institution Name')
    # I am assuming meritorious is one better than honorable mention.
    meritorious = merged_df[(merged_df['Ranking'] != 'honorable mention') & (merged_df['Country'] == 'usa')
                            ][['Institution Name', 'Team Number', 'Ranking']]
    # Assuming you might want to use the 'number' dict to add a column for team counts
    # Write the DataFrames to CSV files
    institutions.to_csv('output/Institutions.csv', index=False)
    teams.to_csv('output/Teams.csv', index=False)
    list_by_team_number.to_csv('output/teams_by_number_of_teams.csv', index=False)
    outstanding.to_csv('output/outstanding_institutions.csv', index=False)
    meritorious.to_csv('output/usa_meritorious_and_better.csv', index=False)
    print("Average number of teams per institution: ", len(teams) / len(institutions))


if __name__ == '__main__':
    parse_math()
