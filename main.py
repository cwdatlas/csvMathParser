import glob

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

    # Iterate over each row in the original DataFrame
    for index, row in df_2015.iterrows():
        institution_name = row['Institution']  # get the value for institution, used as a dictionary key
        # Check if the institution is already in the institutions DataFrame
        if institution_name not in institution_ids:
            # If not, add it with a new Institution ID
            new_id = len(institution_ids) + 1  # Generate a new ID (simple increment)
            institution_ids[institution_name] = new_id  # Add the new institution name to the dictionary
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

    # Write the DataFrames to CSV files
    df_institutions.to_csv('output/Institutions.csv', index=False)
    df_teams.to_csv('output/Teams.csv', index=False)
    # Update user on the current status
    print("Processing 100% complete", end='\r')
    return True


if __name__ == '__main__':
    parse_math()
