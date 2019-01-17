import pandas as pd
import requests

def get_analysis(url, csv_file):
    # load the input file and construct the payload for the request
    csv_ = open(csv_file, "rb").read()
    payload = {"csv": csv_}

    # submit the request
    r = requests.post(url, files=payload).json()

    # ensure the request was successful
    if r["success"]:
        print("\nSuccessful request\n")
        return r
    # otherwise, the request failed
    else:
        print("\nRequest failed\n")
        return []
        
analysis = get_analysis('https://stress-api-jgm.herokuapp.com/analysis', 'test.csv')
analysis.pop('success', None)
output_df = pd.DataFrame.from_dict(analysis)
output_df.to_csv('test_output.csv', index = None)