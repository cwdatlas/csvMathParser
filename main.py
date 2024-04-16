import pandas as pd


def parse_math():
    # Assuming you have '2015.csv' loaded into a pandas DataFrame
    df_2015 = pd.read_csv('input/2015.csv')

    # Creating empty DataFrames for institutions and teams with specified columns
    institutions_cols = ['Institution ID', 'Institution Name', 'City', 'State/Province', 'Country']
    teams_cols = ['Team Number', 'Advisor', 'Problem', 'Ranking', 'Institution ID']

    df_institutions = pd.DataFrame(columns=institutions_cols)
    df_teams = pd.DataFrame(columns=teams_cols)

    # Dictionary to map institution names to generated Institution IDs
    institution_ids = {}

    # Iterate over each row in the original DataFrame
    for index, row in df_2015.iterrows():
        institution_name = row['Institution']
        # Check if the institution is already in the institutions DataFrame
        if institution_name not in institution_ids:
            # If not, add it with a new Institution ID
            new_id = len(institution_ids) + 1  # Generate a new ID (simple increment)
            institution_ids[institution_name] = new_id
            institute_data = pd.DataFrame([{
                'Institution ID': new_id,
                'Institution Name': institution_name,
                'City': row['City'],
                'State/Province': row['State/Province'],
                'Country': row['Country']
            }])
            df_institutions = pd.concat([df_institutions, institute_data], ignore_index=True)


        # Add the team's information to the teams DataFrame
        team_date = pd.DataFrame([{
            'Team Number': row['Team Number'],
            'Advisor': row['Advisor'],
            'Problem': row['Problem'],
            'Ranking': row['Ranking'],
            'Institution ID': institution_ids[institution_name]
        }])
        df_teams = pd.concat([df_teams, team_date], ignore_index=True)

    # Write the DataFrames to CSV files
    df_institutions.to_csv('output/Institutions.csv', index=False)
    df_teams.to_csv('output/Teams.csv', index=False)

    # Print the head of the DataFrames to verify
    print("Institutions DataFrame:")
    print(df_institutions.head())

    print("\nTeams DataFrame:")
    print(df_teams.head())


if __name__ == '__main__':
    parse_math()
