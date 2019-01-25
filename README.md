# Stress API - v1

Algorithm used on the "[Eliciting Driver Stress Using Naturalistic Driving Scenarios on Real Roads](https://dl.acm.org/citation.cfm?id=3239090)" paper.

This algorithm help identify possible stress times during a time series. This algorithm does not discriminate the type of stress, therefore, it could also pick physiological as well as psychological stress.

For this work, stress can be defined as a state of physiological response to a stimulus that can be either internal or external, causing a major change in most of the systems of the body. These changes can be observed from visible behavior, such as breathing changes (change in rate or difficulties), mouth dryness, and an increase in speech speed, or be monitored by non-visible data such as the HR, ST, and GSR due to the effects of the cortisol hormone [1, 2].


## How to send request

The data has to be saved on a csv file at 1 Hz, and must contain 

- dateTime
- heart rate
- skin temperature
- galvanic skin response


### Example data

| datetime         | HR | ST     | GSR      |
|------------------|----|--------|----------|
| 7/12/16 10:51:31 | 83 | 90.716 | 0.000379 |
| 7/12/16 10:51:32 | 83 | 90.716 | 0.000379 |
| 7/12/16 10:51:33 | 83 | 90.716 | 0.00038  |
| 7/12/16 10:51:34 | 84 | 90.716 | 0.00038  |
| 7/12/16 10:51:35 | 83 | 90.716 | 0.00038  |

This algorithm have been tested with data from:

- Microsoft Band 2
- Empatica E4

To account for the differences in the sampling, the data must be averaged over one second windows.


### Using cURL

`curl -X POST -F csv=@test.csv 'https://stress-api-jgm.herokuapp.com/analysis'`


### Using python

```python
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

```

This repo also includes a python script to make the analysis easier:

```bash
usage: Python_example.py [-h] data

positional arguments:
  data        Filename with data to be analyzed (including .csv)
```

### Response

The service returns a json with:

- datetime
- stressLevel
- stressFlag

#### Example response

```json
{
  "datetime": [
    "2016-07-12 10:51:31",
    "2016-07-12 10:51:32",
    "2016-07-12 10:51:32",
    "2016-07-12 10:51:33",
    "2016-07-12 10:51:34"
  ],
  "stressFlag": [
    " ",
    " ",
    " ",
    " ",
    " "
  ],
  "stressLevel": [
    0.44802989788869596,
    0.44802989788869596,
    0.4480303958886647,
    0.4480303958886647,
    0.4551618972154855
  ],
  "success": true
}
```


## References

1. The APA Dictionary of Psychology. Amer Psychological Assn, 1 edition edition.
2. Inna Z. Khazan. The clinical handbook of biofeedback: a step-by-step guide for training and practice with mindfulness. Wiley.


# Cite

If used, please cite:

```
@inproceedings{baltodano2018eliciting,
  title={Eliciting Driver Stress Using Naturalistic Driving Scenarios on Real Roads},
  author={Baltodano, Sonia and Garcia-Mancilla, Jesus and Ju, Wendy},
  booktitle={Proceedings of the 10th International Conference on Automotive User Interfaces and Interactive Vehicular Applications},
  pages={298--309},
  year={2018},
  organization={ACM}
}

@inproceedings{garcia2015stress,
  title={Stress quantification using a wearable device for daily feedback to improve stress management},
  author={Garcia-Mancilla, Jesus and Gonzalez, Victor M},
  booktitle={International Conference on Smart Health},
  pages={204--209},
  year={2015},
  organization={Springer}
}
```


