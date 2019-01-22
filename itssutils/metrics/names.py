class MetricNames(object):
    """ Define metric names and their descriptions """

    def __init__(self):
        self.metrics = {
            # High-level descriptions
            'AgencyName': 'Name of police agency',
            'DriverRace': 'Race of driver',

            # Stop stuff
            'StopCount': 'Number of traffic stops',
            'StopHitRate': 'Contraband "hit" rate for stops (# hits / # stops)',
            'StopsPerPop': 'Stops per 1,000 population (race-specific)',

            # Searches
            'SearchCount': 'Number of searches',
            'SearchRate': 'Search rate (# searches / # stops)',
            'SearchHitCount': 'Countraband "hits"',
            'SearchHitRate': 'Contraband "hit" rate (# hits / # searches)',
            'SearchRequestRate': 'Request rate for consent search (# requests / # stops)',
            'SearchRequestedCount': 'Requests for consent search',
            'SearchWithConsentContrabandCount': 'Consent searchs with contraband found',
            'SearchWithConsentContrabandRate': 'Rate of contraband "hits" for consent searches (# hits / # searches)',
            'SearchWithConsentCount': 'Consent searches performed',
            'SearchWithConsentRate': 'Search rate with consent (# searches / # requests)',
            'SearchWithConsentStopsRate': 'Search rate with consent (# consent searches / # stops)',
            'SearchWithoutConsentContrabandCount': 'Searches conducted when consent denied where contraband found',
            'SearchWithoutConsentContrabandRate': 'Rate of contraband "hits" for searches when consent denied '
                                                  '(# hits / # searches)',
            'SearchWithoutConsentCount': 'Searches conducted when consent denied',
            'SearchWithoutConsentRate': 'Rate of searches conducted when consent denied (# searches / # requests)',
            'OtherSearchCount': 'Searches conducted without consent request',
            'OtherSearchRate': 'Rate of searches without consent request (# searches / # stops)',
            'OtherSearchContrabandCount': 'Searches conducted without consent request yielding contraband',
            'OtherSearchContrabandRate': 'Searches without request contraband "hit" rate (# hits / # searches)',
            'ConsentGivenCount': 'Consent requests granted',
            'ConsentGivenRate': 'Rate of consent (# consents / # requests)',

            # Results
            'Result-CitationCount': 'Citations',
            'Result-CitationRate': 'Citation rate (# citations / # stops)',
            'Result-VerbalCount': 'Verbal warnings',
            'Result-VerbalRate': 'Verbal warning rate (# warnings / # stops)',
            'Result-WrittenCount': 'Written warnings',
            'Result-WrittenRate': 'Written warning rate (# warnings / # stops)',

            # Dog stuff
            'DogAlertCount': 'Dog sniffs with dog alert',
            'DogAlertRate': 'Dog alert rate (# alerts / # sniffs)',
            'DogFoundContrabandCount': 'Dog searches yielding contraband',
            'DogFoundContrabandRate': 'Contraband "hit" rate for dog searches (# hits / # searches)',
            'DogInvolvedCount': 'Stops with dog involved',
            'DogSearchCount': 'Dog searches',
            'DogSearchRate': 'Dog search rate (# searches / # sniffs)',
            'DogSniffCount': 'Dog sniffs',
            'DogSniffRate': 'Dog sniff rate (# sniffs / # stops)',

            # Reason for stop and results (searches + citations)
            'Reason-CommercialVehicleCitationCount': 'Citations for "commercial vehicle" stop',
            'Reason-CommercialVehicleCitationRate': 'Citation rate for "commercial vehicle" stops '
                                                    '(# commercial citations / # commercial stops)',
            'Reason-CommercialVehicleCount': 'Stops for "Commercial Vehicle"',
            'Reason-CommercialVehicleRate': 'Commercial vehicle stop rate (# commercial vehicle stops / # stops)',
            'Reason-EquipmentCitationCount': 'Equipment citations',
            'Reason-EquipmentCitationRate': 'Equipment citation rate (# equipment citations / # equipment stops)',
            'Reason-EquipmentCount': 'Stops for "Equipment"',
            'Reason-EquipmentHitCount': 'Count of contraband found after equipment stops',
            'Reason-EquipmentHitRate': 'Hit rate for searches after equipment stops (# hits / # equipment searches)',
            'Reason-EquipmentRate': 'Equipment stop rates (# equipment stops / # stops)',
            'Reason-EquipmentSearchCount': 'Count of searches after equipment stops',
            'Reason-EquipmentSearchRate': 'Rate of searches after equipment stops (# searches / # equipment stops)',
            'Reason-LicenseRegistrationCitationCount': 'License/Registration citations',
            'Reason-LicenseRegistrationCitationRate': 'License/Registration citation rate'
                                                      '(# L/R citations / # L/R stops)',
            'Reason-LicenseRegistrationCount': 'Stops for "License/Registration"',
            'Reason-LicenseRegistrationHitCount': 'Count of contraband hits after L/R stops',
            'Reason-LicenseRegistrationHitRate': 'Contraband hit rate after L/R stops (# hits / # L/R searches)',
            'Reason-LicenseRegistrationRate': 'License/Registration stop rates (# L/R stops / # stops)',
            'Reason-LicenseRegistrationSearchCount': 'Searches after stops for license/registration',
            'Reason-LicenseRegistrationSearchRate': 'Search rate for stops due to L/R (# searches / # L/R stops)',
            'Reason-MovingViolationCitationCount': 'Moving Violation citations',
            'Reason-MovingViolationCitationRate': 'Moving Violation citation rate (# MV citations / # MV stops)',
            'Reason-MovingViolationCount': 'Stops for "Moving Violation"',
            'Reason-MovingViolationHitCount': 'Count of contraband hits after moving violation stops',
            'Reason-MovingViolationHitRate': 'Contraband hit rate after moving violation stops '
                                             '(# hits / # mv searches)',
            'Reason-MovingViolationRate': 'Moving Violation stop rate (# MV stops / # stops)',
            'Reason-MovingViolationSearchCount': 'Searches conducted after moving violation stops',
            'Reason-MovingViolationSearchRate': 'Search rate after moving violation stop (# searches / # mv stops)',

            # Moving violation sub-category
            'move-FollowCitationCount': 'Citations issued for following',
            'move-FollowCitationRate': 'Citation rate for following (# citations / # following stops)',
            'move-FollowCount': 'Count of stops for following',
            'move-FollowHitCount': 'Count of contraband hits after following stops ',
            'move-FollowHitRate': 'Contraband hit rate after following stops (# hits / # following searches)',
            'move-FollowRate': 'Rate of stops for following (# following stops / # moving violation stops)',
            'move-FollowSearchCount': 'Searches conducted after following stop',
            'move-FollowSearchRate': 'Search rate after following stops (# searches / # following stops)',
            'move-LaneCitationCount': 'Citations for lane change violation',
            'move-LaneCitationRate': 'Citation rate for lange change violation (# citations / # lane stops)',
            'move-LaneCount': 'Stops for lane change',
            'move-LaneHitCount': 'Count of contraband hits after lane change stops ',
            'move-LaneHitRate': 'Contraband hit rate after lange change stops (# hits / # lane change searches)',
            'move-LaneRate': 'Stop rate for lane change violation (# lane stops / # moving violation stops)',
            'move-LaneSearchCount': 'Searches conducted after lane change stop',
            'move-LaneSearchRate': 'Search rate after lane change stops (# searches / # lane change stops)',
            'move-NACount': 'Other moving violation stop count',
            'move-NARate': 'Other moving violation stop rate (# other stops / # moving violation stops)',
            'move-OtherCitationCount': 'Other citation count',
            'move-OtherCitationRate': 'Other citation rate',
            'move-OtherCount': 'Other moving violation count',
            'move-OtherHitCount': 'Other moving violation hit count',
            'move-OtherHitRate': 'Other moving violation hit rate',
            'move-OtherRate': 'Other moving violation rate',
            'move-OtherSearchCount': 'Other moving violation search count',
            'move-OtherSearchRate': 'Other moving violation search rate',
            'move-SeatCitationCount': 'Citations for seatbelt violation',
            'move-SeatCitationRate': 'Citation rate for seatbelt violation (# citations / # seatbelt stops)',
            'move-SeatCount': 'Stops for seatbelt violation',
            'move-SeatHitCount': 'Contraband hit count after seatbelt violation stop',
            'move-SeatHitRate': 'Contraband hit rate after seatbelt violation stop (# hits / # searches)',
            'move-SeatRate': 'Stop rate for seatbelt violation (# seatbelt stops / # moving violation stops)',
            'move-SeatSearchCount': 'Searches after seatbelt violation stops',
            'move-SeatSearchRate': 'Search rate after seatbelt violation stops (# searches / # seatbelt stops)',
            'move-SpeedCitationCount': 'Citations for speeding',
            'move-SpeedCitationRate': 'Citation rate for speeding (# citations / # speeding stops)',
            'move-SpeedCount': 'Stops for speeding',
            'move-SpeedHitCount': 'Speeding hit count',
            'move-SpeedHitRate': 'Speeding hit rate',
            'move-SpeedRate': 'Stop rate for speeding (# speeding stops / # moving violation stops)',
            'move-SpeedSearchCount': 'Speeding search count',
            'move-SpeedSearchRate': 'Speeding search rate',
            'move-TrafficCitationCount': 'Citations for traffic violation',
            'move-TrafficCitationRate': 'Citation rate for traffic violation '
                                        '(# citations / # traffic violation stops)',
            'move-TrafficCount': 'Stops for traffic violation',
            'move-TrafficHitCount': 'Traffic hit count',
            'move-TrafficHitRate': 'Traffic hit rate',
            'move-TrafficRate': 'Stop rate for traffic violation '
                                '(# traffic violation stops / # moving violation stops)',
            'move-TrafficSearchCount': 'Traffic search count',
            'move-TrafficSearchRate': 'Traffic search rate',

        }

        self.zscore_map = [('SearchWithConsentStopsRate', 'StopCount'),
                ('ConsentGivenRate', 'SearchRequestCount'),
                ('DogAlertRate', 'DogSniffCount'),
                ('DogFoundContrabandRate', 'DogSniffCount'),
                ('DogInvolvedRate', 'StopCount'),
                ('DogSearchRate', 'StopCount'),
                ('DogSniffRate', 'StopCount'),
                ('OtherSearchContrabandRate', 'OtherSearchCount'),
                ('OtherSearchRate', 'StopCount'),
                ('Reason-CommercialVehicleCitationRate', 'Reason-CommercialVehicleCount'),
                ('Reason-CommercialVehicleHitRate', 'Reason-CommercialVehicleSearchCount'),
                ('Reason-CommercialVehicleRate', 'StopCount'),
                ('Reason-CommercialVehicleSearchRate', 'Reason-CommercialVehicleCount'),
                ('Reason-EquipmentCitationRate', 'Reason-EquipmentCount'),
                ('Reason-EquipmentHitRate', 'Reason-EquipmentSearchCount'),
                ('Reason-EquipmentRate', 'StopCount'),
                ('Reason-EquipmentSearchRate', 'Reason-EquipmentCount'),
                ('Reason-LicenseRegistrationCitationRate', 'Reason-LicenseRegistrationCount'),
                ('Reason-LicenseRegistrationHitRate', 'Reason-LicenseRegistrationSearchCount'),
                ('Reason-LicenseRegistrationRate', 'StopCount'),
                ('Reason-LicenseRegistrationSearchRate', 'Reason-LicenseRegistrationCount'),
                ('Reason-MovingViolationCitationRate', 'Reason-MovingViolationCount'),
                ('Reason-MovingViolationHitRate', 'Reason-MovingViolationSearchCount'),
                ('Reason-MovingViolationRate', 'StopCount'),
                ('Reason-MovingViolationSearchRate', 'Reason-MovingViolationCount'),
                ('Result-CitationRate', 'StopCount'),
                ('Result-VerbalRate', 'StopCount'),
                ('Result-WrittenRate', 'StopCount'),
                ('SearchHitRate', 'SearchCount'),
                ('SearchRate', 'StopCount'),
                ('SearchRequestRate', 'StopCount'),
                ('SearchWithConsentContrabandRate', 'SearchWithConsentCount'),
                ('SearchWithConsentRate', 'StopCount'),
                ('SearchWithoutConsentContrabandRate', 'SearchWithoutConsentCount'),
                ('SearchWithoutConsentRate', 'StopCount'),
                ('move-FollowCitationRate', 'move-FollowCount'),
                ('move-FollowHitRate', 'move-FollowSearchCount'),
                ('move-FollowRate', 'StopCount'),
                ('move-FollowSearchRate', 'Reason-MovingViolationCount'),
                ('move-LaneCitationRate', 'move-LaneCount'),
                ('move-LaneHitRate', 'move-LaneSearchRate'),
                ('move-LaneRate', 'Reason-MovingViolationCount'),
                ('move-LaneSearchRate', 'move-LaneCount'),
                ('move-OtherCitationRate', 'Reason-MovingViolationCount'),
                ('move-OtherHitRate', 'move-OtherSearchCount'),
                ('move-OtherRate', 'Reason-MovingViolationCount'),
                ('move-OtherSearchRate', 'move-OtherCount'),
                ('move-SeatCitationRate', 'Reason-MovingViolationCount'),
                ('move-SeatHitRate', 'move-SeatSearchCount'),
                ('move-SeatRate', 'StopCount'),
                ('move-SeatSearchRate', 'Reason-MovingViolationCount'),
                ('move-SpeedCitationRate', 'Reason-MovingViolationCount'),
                ('move-SpeedHitRate', 'move-SpeedSearchCount'),
                ('move-SpeedRate', 'StopCount'),
                ('move-SpeedSearchRate', 'Reason-MovingViolationCount'),
                ('move-TrafficCitationRate', 'Reason-MovingViolationCount'),
                ('move-TrafficHitRate', 'move-TrafficSearchCount'),
                ('move-TrafficRate', 'StopCount'),
                ('move-TrafficSearchRate', 'Reason-MovingViolationCount'),
            ]

    def get_names(self):
        return list(self.metrics.keys())

    def get_description(self, metric):
        return self.metrics.get(metric, metric)

    def add_metric(self, metric, description):
        if metric in self.metrics:
            raise KeyError(f'Metric {metric} already in metrics.')
        self.metrics[metric] = description

    def change_metric(self, metric, description):
        if metric not in self.metrics:
            raise KeyError(f'Metric {metric} must be added.')
        self.metrics[metric] = description

    def remove_metric(self, metric):
        return self.metrics.pop(metric, None)
