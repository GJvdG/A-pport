import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def parser(filepath):
    athlete_input = pd.read_csv(filepath, header=None, dtype=str)

    no_athletes = len(athlete_input)

    # dung beetling
    athlete_input[2] = np.nan
    athlete_input[2] = athlete_input[2].astype(object)

    for i in range(no_athletes):
        # ath = athlete_input.iloc[0] # debug
        name = athlete_input.iloc[i, 0].replace(' ', '+')  # Replace spaces with '+'

        if pd.isna(athlete_input.iloc[i, 1]):
            year = ''
        else:
            year = athlete_input.iloc[i, 1]

        url = f'https://uitslagen.nl/zoek.html?naam={name}&exct=j&gbjr={year}'

        athlete_input.iloc[i, 2] = url

    logging.info(f"Created urls for {no_athletes} athletes")
    athlete_list = athlete_input.values.tolist()

    return athlete_list

def scrape(athlete_list):
    # initialize output df
    headers = ['Datum', 'Evenement', 'Plaats', 'Categorie', 'Afstand', 'Positie', 'Naam', 'Woonplaats/vereniging',
               'Bruto', 'Netto', 'Snelheid', 'Tempo']
    tot_results = pd.DataFrame(columns=headers)

    for ath in athlete_list:
        # ath = athlete_list[3] # debugging
        logging.info(f"Scraping for athlete {ath[0]}")
        url = ath[2]
        scrape_results = pd.read_html(url)
        scrape_clean = scrape_results[4:-1] # drop some bullshit
        logging.info(f"{len(scrape_clean)} results found for {ath[0]}")

        if scrape_clean: # if results are found
            # temp df for current athlete-race
            race_results = pd.DataFrame(index=range(len(scrape_clean)), columns=tot_results.columns)

            for i in range(len(scrape_clean)):
                # Evenement, Datum, Plaats
                dat_event_loc = str(scrape_clean[i].columns[1]).split(",")
                dat_event = dat_event_loc[0].split(" ")
                race_results.loc[i, 'Datum'] = dat_event[0]
                race_results.loc[i, 'Evenement'] = dat_event[1]
                race_results.loc[i, 'Plaats'] = dat_event_loc[1]

                # Categorie, Afstand
                cat_dist = str(scrape_clean[i].iloc[1,0]).split(",")
                race_results.loc[i, 'Categorie'] = cat_dist[0]
                race_results.loc[i, 'Afstand'] = cat_dist[1]

                # Positie, Naam, Woonplaats/vereniging, Bruto, Netto
                race_results.iloc[i, 5:] = scrape_clean[i].iloc[3, :]

        else: # if no race results
            # create empty row with name only
            race_results = pd.DataFrame(index=[0], columns=tot_results.columns)
            race_results['Naam'] = ath[0]

        # append current athlete-race to output
        tot_results = tot_results._append(race_results, ignore_index=True)

        # clean up
        tot_results['Snelheid'] = tot_results['Snelheid'].str.replace('\xa0km/u', '', regex=False)
        tot_results['Tempo'] = tot_results['Tempo'].str.replace('\xa0min/km', '', regex=False)

    return tot_results

def main():
    input_file = 'Data/test.csv'
    athlete_list = parser(filepath = input_file)
    tot_results = scrape(athlete_list=athlete_list)

    return tot_results

if __name__ == '__main__':
        main()


