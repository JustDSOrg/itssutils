CONSENT_SUBJECTS = ['', 'Vehicle', 'Driver', 'Passenger']
SEARCH_REQUEST = ['{}ConsentSearchRequested'.format(subject)
                  for subject in CONSENT_SUBJECTS]
CONSENT_GIVEN = ['{}ConsentGiven'.format(subject)
                 for subject in CONSENT_SUBJECTS]
SEARCH_CONDUCTED = ['{}SearchConducted'.format(subject)
                    for subject in CONSENT_SUBJECTS] + ['WasConsentSearchPerformed']
SEARCH_JUSTIFY = ['{}SearchConductedBy'.format(subject)
                  for subject in CONSENT_SUBJECTS]

DOG_CONSENT_GROUP = ['PoliceDogPerformSniffOfVehicle',
                     'PoliceDogAlertIfSniffed',
                     'PoliceDogVehicleSearched',]

SEARCH_SUBJECTS = ['', 'Consent', 'Vehicle', 'DriverPassenger', 'PoliceDog']


OUTCOME_TYPES = ['ContrabandFound', 'DrugsFound',
                 'DrugParaphernaliaFound', 'AlcoholFound',
                 'WeaponFound', 'StolenPropertyFound',
                 'OtherContrabandFound', 'DrugAmount',]

ALL_OUTCOMES2 = []
for subject in SEARCH_SUBJECTS:
    for outcome in OUTCOME_TYPES:
        ALL_OUTCOMES2.append(subject + outcome)

VEHICLE_OUTCOMES = ['VehicleContrabandFound',
                    'VehicleDrugsFound',
                    'VehicleDrugParaphernaliaFound',
                    'VehicleAlcoholFound',
                    'VehicleWeaponFound',
                    'VehicleStolenPropertyFound',
                    'VehicleOtherContrabandFound',
                    'VehicleDrugAmount',
                    ]

DRIVER_PASSENGER_OUTCOMES = ['DriverPassengerContrabandFound',
                             'DriverPassengerDrugsFound',
                             'DriverPassengerDrugParaphernaliaFound',
                             'DriverPassengerAlcoholFound',
                             'DriverPassengerWeaponFound',
                             'DriverPassengerStolenPropertyFound',
                             'DriverPassengerOtherContrabandFound',
                             'DriverPassengerDrugAmount',
                             ]

DOG_OUTCOMES = ['PoliceDogContrabandFound',
                'PoliceDogDrugsFound',
                'PoliceDogDrugParaphernaliaFound',
                'PoliceDogAlcoholFound',
                'PoliceDogWeaponFound',
                'PoliceDogStolenPropertyFound',
                'PoliceDogOtherContrabandFound',
                'PoliceDogDrugAmount',
                ]

CONSENT_OUTCOMES = ['Consent' + x for x in OUTCOME_TYPES]

ALL_OUTCOMES = OUTCOME_TYPES + CONSENT_OUTCOMES + VEHICLE_OUTCOMES + DRIVER_PASSENGER_OUTCOMES + DOG_OUTCOMES

# Replace column names in old data files with newer versions
REPLACEMENTS = {'Race': 'DriverRace',
                'MovingViolationType': 'TypeOfMovingViolation',
                'ZIPCode': 'ZIP',
                'WasConsentGranted': 'ConsentGiven',
                'VehicleSearchType': 'VehicleSearchConductedBy',
                'PassengersSearchType': 'PassengerSearchConductedBy',
                'DriverSearchType': 'DriverSearchConductedBy',
                }

assert ALL_OUTCOMES == ALL_OUTCOMES2


def any_true(df, cols):
    return (df[cols] == 1).any(axis=1)


def merge_cols(df, new_name, cols):
    cols = [col for col in cols if col in df.columns]
    df[new_name] = any_true(df, cols)
    return df


def consolidate_columns(df):
    """
    Consolidate Driver/Passenger/Vehicle columns into a single column
    for easier parsing.
    """
    consolidations = [('SearchRequested', SEARCH_REQUEST),
                      ('ConsentGiven', CONSENT_GIVEN),
                      ('SearchConducted', SEARCH_CONDUCTED),
                      ('DogOutcomes', DOG_OUTCOMES),
                      ('IllegalFound', ALL_OUTCOMES),
                      ('DogInvolved', DOG_CONSENT_GROUP),
                      ]

    for to_replace, replace_with in REPLACEMENTS.items():
        if to_replace in df.columns:
            df[replace_with] = df[to_replace]
            df = df.drop(to_replace, axis=1)

    for new_col, col_group in consolidations:
        df = merge_cols(df, new_col, col_group)

    df.AgencyName = df.AgencyName.str.title()
    return df
