import numpy as np
import pandas as pd

# Hardcoded elements
# The default code to use to translate values in the raw data file
DEFAULT_CODE = {0:np.NAN, 1: True, 2: False, 'Yes': True, 'No': False}

# For searches, translate number code to string search type
SEARCH_CONDUCTED_CODE = {0: 'NA', 1: 'Consent', 2: 'Other',
                         'Incident to Arrest': 'Incident to Arrest',
                         'Other': 'Other',
                         'Probable Cause': 'Probable Cause',
                         'Custodial Arrest': 'Custodial Arrest',
                         'Drug Dog Alert': 'Drug Dog Alert',
                         'Reasonable Suspicion': 'Reasonable Suspicion'}

# For drugs, translate number code to amount
DRUG_CODE = {0:'NA',
             1:'< 2 grams',
             2: '2-10 grams',
             3:'11-50 grams',
             4:'51-100 grams',
             5:'> 100 grams',
             'Less than 2 grams': '< 2 grams',
             '2-10 grams': '2-10 grams',
             '11-50 grams': '11-50 grams',
             'More than 100 grams': '> 100 grams',
             '51-100 grams': '51-100 grams'}

# Columns to decode using the decoder
DECODE_COLUMNS = ['DriverSex',
                  'DriverRace',
                  'ResultOfStop',
                  'ReasonForStop',
                  'TypeOfMovingViolation',
                  'VehicleDrugAmount',
                  'DriverPassengerDrugAmount']

DEFAULT_COLUMNS = ['AgencyName',
                   'AgencyCode',
                   'DateOfStop',
                   'TimeOfStop',
                   'DurationOfStop',
                   'ZIP',
                   'VehicleMake',
                   'VehicleYear',
                   'DriversYearofBirth',
                   'DriverSex',
                   'DriverRace',
                   'ReasonForStop',
                   'TypeOfMovingViolation',
                   'ResultOfStop',
                   'BeatLocationOfStop',
                   'VehicleConsentSearchRequested',
                   'VehicleConsentGiven',
                   'VehicleSearchConducted',
                   'VehicleSearchConductedBy',
                   'VehicleContrabandFound',
                   'VehicleDrugsFound',
                   'VehicleDrugParaphernaliaFound',
                   'VehicleAlcoholFound',
                   'VehicleWeaponFound',
                   'VehicleStolenPropertyFound',
                   'VehicleOtherContrabandFound',
                   'VehicleDrugAmount',
                   'DriverConsentSearchRequested',
                   'DriverConsentGiven',
                   'DriverSearchConducted',
                   'DriverSearchConductedBy',
                   'PassengerConsentSearchRequested',
                   'PassengerConsentGiven',
                   'PassengerSearchConducted',
                   'PassengerSearchConductedBy',
                   'DriverPassengerContrabandFound',
                   'DriverPassengerDrugsFound',
                   'DriverPassengerDrugParaphernaliaFound',
                   'DriverPassengerAlcoholFound',
                   'DriverPassengerWeaponFound',
                   'DriverPassengerStolenPropertyFound',
                   'DriverPassengerOtherContrabandFound',
                   'DriverPassengerDrugAmount',
                   'PoliceDogPerformSniffOfVehicle',
                   'PoliceDogAlertIfSniffed',
                   'PoliceDogVehicleSearched',
                   'PoliceDogContrabandFound',
                   'PoliceDogDrugsFound',
                   'PoliceDogDrugParaphernaliaFound',
                   'PoliceDogAlcoholFound',
                   'PoliceDogWeaponFound',
                   'PoliceDogStolenPropertyFound',
                   'PoliceDogOtherContrabandFound',
                   'PoliceDogDrugAmount']

# Set all other appropriate values
DECODER_RING = {'DriverSex' : {np.NAN:np.NAN, 1:'Male', 2:'Female', 9:np.NAN,
                               'Male': 'Male', 'Female': 'Female'},

                'DriverRace' : {1: 'White', 2:'Black', 3:'Native American',
                                4: 'Hispanic/Latino', 5:'Asian', 6:'Pacific',
                                7: 'UnknownOther',
                                9: 'UnknownOther',
                                999: 'UnknownOther',
                                'Caucasian': 'White',
                                'African American': 'Black',
                                'African/American': 'Black',
                                'Asian/Pacific Islander': 'Asian',
                                'Hispanic': 'Hispanic/Latino',
                                'Native American/Alaskan': 'Native American',
                                'Other': 'UnknownOther'}, # this was 'unknown'

                'DriversYearofBirth': {i:i for i in range(1900, 2010)},

                'ReasonForStop' : {1:'MovingViolation',
                                   2:'Equipment',
                                   3:'LicenseRegistration',
                                   4:'CommercialVehicle',
                                   #    5:np.NAN,
                                   6:np.NAN,
                                   9:np.NAN,
                                   'Moving Violation': 'MovingViolation',
                                   'Moving ViolationMoving Violation': 'MovingViolation',
                                   'Equipment': 'Equipment',
                                   'License Plate/Registration': 'LicenseRegistration'},

                'TypeOfMovingViolation': {0: 'NA',
                                          1: 'Speed', 'Speed': 'Speed',
                                          2: 'Lane Violation', 'Lane Violation': 'Lane Violation',
                                          3: 'Seat Belt', 'SeatBelt': 'Seat Belt',
                                          4: 'Traffic Sign or Signal', 'Traffic Sign or Signal': 'Traffic Sign or Signal',
                                          5: 'Follow too close', 'Follow too Close': 'Follow too close',
                                          6: 'Other', 'Other': 'Other'},

                'ResultOfStop': {1: 'Citation',
                                 2: 'Written Warning',
                                 3: 'Verbal Warning (stop card)',
                                 'Citation': 'Citation',
                                 'Written Warning': 'Written Warning',
                                 'Verbal Warning': 'Verbal Warning (stop card)',
                                 'Verbal Warning (Stop Card)': 'Verbal Warning (stop card)'},

                'VehicleSearchConductedBy': SEARCH_CONDUCTED_CODE,
                'DriverSearchConductedBy': SEARCH_CONDUCTED_CODE,
                'PassengerSearchConductedBy': SEARCH_CONDUCTED_CODE,
                'SearchConductedBy': SEARCH_CONDUCTED_CODE,
                'VehicleDrugAmount': DRUG_CODE,
                'DriverPassengerDrugAmount': DRUG_CODE,
                'PoliceDogDrugAmount': DRUG_CODE,
                }


class Decoder(object):
    """Decoder is for interpreting the codes used in the ITSS traffic data"""
    def __init__(self):
        self.decoder_ring = DECODER_RING
        self.default_code = DEFAULT_CODE

        # Set our decoder to use the default if the column isn't known
        self.decoder = lambda x: self.decoder_ring.get(x, self.default_code)

    def decode_column(self, df, col_name):
        """Translate the raw data into useful, human-readable values"""
        df = df.copy()
        decoder = self.decoder(col_name)
        new_values = []
        for i, val in df[col_name].items():
            try:
                new_val = decoder[val]
            except:
                new_val = val
            new_values.append(new_val)
        df[col_name] = new_values
        return df


if __name__ == '__main__':
    decoder = Decoder()
    index = np.arange(10)
    df = pd.DataFrame(data=1, index=index, columns=DEFAULT_COLUMNS)
    new_df = decoder.decode_column(df, col_name='DriverSex')
    print(df.head().T)
    print(new_df.head().T)
