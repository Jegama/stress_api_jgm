import pandas as pd
import requests, argparse

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
    else:
        print("\nRequest failed\n")
        return []
        
def main():
    parser = argparse.ArgumentParser()

    # Data
    parser.add_argument("data", help="Filename with data to be analyzed (including .csv)", type=str)

    args = parser.parse_args()

    print('\nWorking on:', args.data)

    analysis = get_analysis('https://stress-api-jgm.herokuapp.com/analysis', args.data)
    analysis.pop('success', None)
    output_df = pd.DataFrame.from_dict(analysis)
    output_df.to_csv('test_output.csv', index = None)

    print('\nDone\n')


if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        print('\n\nExiting due to KeyboardInterrupt!\n')
