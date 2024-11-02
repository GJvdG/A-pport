import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def input_parsers(csv_file):
    input = pd.read_csv('Data/test.csv', header=None)

def scrape(athlete_list):
    # initialize output df
    headers = ['Datum', 'Evenement', 'Plaats', 'Categorie', 'Afstand', 'Positie', 'Naam', 'Woonplaats/vereniging',
               'Bruto', 'Netto', 'Snelheid', 'Tempo']
    tot_results = pd.DataFrame(columns=headers)

    for ath in athlete_list:
        # ath = athlete_list[3] # debugging
        logging.info(f"Scraping for athlete {ath[0]}")
        url = ath[3]
        scrape_results = pd.read_html(url)
        scrape_clean = scrape_results[4:-1] # drop some bullshit

        if scrape_clean: # if results are found
            # temp df for current athlete-race
            race_results = pd.DataFrame(index=range(len(scrape_clean)), columns=tot_results.columns)

            for i in range(len(scrape_clean)):
                # Evenement, Datum, Plaats
                dat_event_loc = str(scrape_clean[i].columns[1]).split(",")
                dat_event = dat_event_loc[0].split(" ")
                race_results['Datum'] = dat_event[0]
                race_results['Evenement'] = dat_event[1]
                race_results['Plaats'] = dat_event_loc[1]

                # Categorie, Afstand
                cat_dist = str(scrape_clean[i].iloc[1,0]).split(",")
                race_results['Categorie'] = cat_dist[0]
                race_results['Afstand'] = cat_dist[1]

                # Positie, Naam, Woonplaats/vereniging, Bruto, Netto
                race_results.iloc[i, 5:] = scrape_clean[i].iloc[3, :]

        else: # if no race results
            # create empty row with name only
            race_results = pd.DataFrame(index=[0], columns=tot_results.columns)
            race_results['Naam'] = ath[0]

        logging.info(f"{len(race_results)} found for {ath[0]}")

        # append current athlete-race to output
        tot_results = tot_results._append(race_results, ignore_index=True)

    return tot_results

def main():
    tot_results = scrape(athlete_list=athlete_list)


if __name__ == '__main__':
        main()


