from collections import defaultdict
import numpy as np
import pandas as pd
import tqdm
import itertools

RACE_TRANSLATION = {
    'All_DriverRace': 'total',
    'White': 'not_hispanic_or_latino_white',
    'Black': 'not_hispanic_or_latino_black',
    'HispanicLatino': 'hispanic',
    'Hispanic/Latino': 'hispanic',
    'UnknownOther': 'not_hispanic_or_latino_other',
    'Asian': 'not_hispanic_or_latino_asian',
    'Native American': 'not_hispanic_or_latino_native_american',
    'Pacific': 'not_hispanic_or_latino_native_hawaiian',
}


def calc_metrics(stops_df, population=None):
    """ Huge function to calculate all the metrics we want
        Pass in demographic df if available as population """
    # Default to returning NaN
    metrics = defaultdict(lambda: np.nan)

    # High level metrics
    stops = stops_df
    searches = stops[stops.SearchConducted]
    search_requests = stops[stops.SearchRequested]
    search_with_consent = search_requests[(search_requests.SearchConducted) & (search_requests.ConsentGiven)]
    search_without_consent = search_requests[(search_requests.SearchConducted) & (~search_requests.ConsentGiven)]
    other_searches = stops[stops.SearchConducted & ~stops.SearchRequested]
    dogs = stops[stops.DogInvolved]
    moving_violations = stops[stops.ReasonForStop == 'MovingViolation']

    # Get contraband hit counts
    stop_count = len(stops)
    stop_find_count = stops.IllegalFound.sum()
    search_count = len(searches)
    search_find_count = searches.IllegalFound.sum()
    search_request_count = len(search_requests)
    consent_count = search_requests.ConsentGiven.sum()
    moving_violation_count = len(moving_violations)
    search_with_consent_count = len(search_with_consent)
    search_with_consent_find_count = search_with_consent.IllegalFound.sum()
    search_without_consent_find_count = search_without_consent.IllegalFound.sum()
    search_without_consent_count = len(search_without_consent)
    other_search_count = len(other_searches)
    other_search_find_count = other_searches.IllegalFound.sum()
    dog_count = len(dogs)

    # Start storing values in the defaultdict
    metrics['StopCount'] = stop_count
    metrics['SearchCount'] = search_count
    metrics['SearchRequestCount'] = search_request_count
    metrics['ConsentGivenCount'] = consent_count
    metrics['SearchWithConsentCount'] = search_with_consent_count
    metrics['SearchWithConsentContrabandCount'] = search_with_consent_find_count
    metrics['SearchWithoutConsentCount'] = search_without_consent_count
    metrics['SearchWithoutConsentContrabandCount'] = search_without_consent_find_count
    metrics['OtherSearchCount'] = other_search_count
    metrics['OtherSearchContrabandCount'] = other_search_find_count
    metrics['DogInvolvedCount'] = dog_count
    metrics['SearchHitCount'] = search_find_count
    metrics['StopHitCount'] = stop_find_count

    # If we have any stops, calculate rates that are based on stops
    if stop_count:
        metrics['StopHitRate'] = stop_find_count / stop_count
        metrics['SearchRate'] = search_count / stop_count
        metrics['SearchRequestRate'] =  search_request_count / stop_count
        metrics['SearchWithConsentStopsRate'] = search_with_consent_count / stop_count
        metrics['OtherSearchRate'] = other_search_count / stop_count
        metrics['DogInvolvedRate'] = dog_count / stop_count

        # Calculate rates for searches
        if search_with_consent_count:
            metrics['SearchWithConsentContrabandRate'] = search_with_consent_find_count / search_with_consent_count
        if search_without_consent_count:
            metrics['SearchWithoutConsentContrabandRate'] = search_without_consent_find_count / search_without_consent_count
        if other_search_count:
            metrics['OtherSearchContrabandRate'] = other_search_find_count / other_search_count

        # Calculate counts and rates for various pullover reasons
        reason_counts = stops.ReasonForStop.value_counts()
        for (reason, reason_count) in reason_counts.iteritems():
            reasons = stops[stops.ReasonForStop == reason]
            metrics[f'Reason-{reason}Count'] = reason_count
            metrics[f'Reason-{reason}Rate'] = reason_count / stop_count
            citations = (reasons.ResultOfStop == 'Citation').sum()
            metrics[f'Reason-{reason}CitationCount'] = citations
            metrics[f'Reason-{reason}CitationRate'] = citations / reason_count
            reasons_searchcount = reasons.SearchConducted.sum()
            metrics[f'Reason-{reason}SearchCount'] = reasons_searchcount
            metrics[f'Reason-{reason}SearchRate'] = reasons_searchcount / reason_count
            reasons_hitcount = reasons.IllegalFound.sum()
            if reasons_searchcount:
                metrics[f'Reason-{reason}HitCount'] = reasons_hitcount
                metrics[f'Reason-{reason}HitRate'] = reasons_hitcount / reasons_searchcount

        # Calculate stop outcome counts and rates
        outcome_counts = stops.ResultOfStop.value_counts()
        for (outcome, outcome_count) in outcome_counts.iteritems():
            try:
                short_outcome = outcome.split()[0]
            except:
                print(outcome_counts)
            metrics[f'Result-{short_outcome}Count'] = outcome_count
            metrics[f'Result-{short_outcome}Rate'] = outcome_count / stop_count

        # If demographic data is available, calculate normalized stop rates
        try:
            if population:
                metrics['Population'] = population
                metrics['StopsPerPop'] = stop_count / population
        except ValueError:
            print(population)

    # Calculate search hit rate
    if search_count:
        metrics['SearchHitRate'] = search_find_count / search_count

        # If demographic data is available, caluclate normalized search rates
        if population:
            metrics['SearchesPerPop'] = search_count / population

    # Calculate consent rates
    if search_request_count:
        metrics['ConsentGivenRate'] = searches.ConsentGiven.sum() / search_request_count
        metrics['SearchWithConsentRate'] = search_with_consent_count / search_request_count
        metrics['SearchWithoutConsentRate'] = search_without_consent_count / search_request_count

        # Normalize by population if available
        if population:
            metrics['SearchRequestPerPop'] = search_request_count / population

    # Calculate counts and rates for various types of moving violations

    if moving_violation_count:
        moving_violation_counts = moving_violations.TypeOfMovingViolation.value_counts()
        for (violation, move_count) in moving_violation_counts.iteritems():
            short_violation = violation.split()[0]
            violation_specific = moving_violations[moving_violations.TypeOfMovingViolation == violation]
            metrics[f'move-{short_violation}Count'] = move_count
            metrics[f'move-{short_violation}Rate'] = move_count / moving_violation_count
            metrics[f'move-{short_violation}StopsRate'] = move_count / stop_count
            if move_count:
                citations = (violation_specific.ResultOfStop == 'Citation').sum()
                metrics[f'move-{short_violation}CitationCount'] = citations
                metrics[f'move-{short_violation}CitationRate'] = citations / move_count
                metrics[f'move-{short_violation}CitationStopsRate'] = citations / stop_count
                search_move_count = violation_specific.SearchConducted.sum()
                metrics[f'move-{short_violation}SearchCount'] = search_move_count
                metrics[f'move-{short_violation}SearchRate'] = search_move_count / move_count
                metrics[f'move-{short_violation}SearchStopsRate'] = search_move_count / stop_count
                search_hit_count = violation_specific.IllegalFound.sum()
                if search_move_count:
                    metrics[f'move-{short_violation}HitCount'] = search_hit_count
                    metrics[f'move-{short_violation}HitRate'] = search_hit_count / search_move_count

    # Calculate counts and rates for dog sniffs and searches
    if dog_count:
        dog_sniffs = len(dogs[dogs['PoliceDogPerformSniffOfVehicle'] == 1])
        dog_alerts = len(dogs[dogs['PoliceDogAlertIfSniffed'] == 1])
        dog_searches = len(dogs[dogs['PoliceDogVehicleSearched'] == 1])
        dog_hits = len(dogs[dogs['PoliceDogContrabandFound'] == 1])
        metrics['DogSniffCount'] = dog_sniffs
        metrics['DogSniffRate'] = dog_sniffs / stop_count
        metrics['DogAlertCount'] = dog_alerts
        if dog_sniffs:
            metrics['DogAlertRate'] = dog_alerts / dog_sniffs
        metrics['DogSearchCount'] = dog_searches
        if dog_sniffs:
            metrics['DogSearchRate'] = dog_searches / dog_sniffs
            metrics['DogSearchStopsRate'] = dog_searches / stop_count
        metrics['DogFoundContrabandCount'] = dog_hits
        if dog_searches:
            metrics['DogFoundContrabandRate'] = dog_hits / dog_searches

    return metrics


def get_new_tuple_name(names, sublist, full_list):
    """ Returns the new tuple to use as the index based on a given combination
        of items from the full list """
    t = []
    if not (isinstance(names, list) or isinstance(names, tuple)):
        names = [str(names)]
    lookup = dict(zip(sublist, names))
    for element in full_list:
        if element in sublist:
            t.append(str(lookup[element]))
        else:
            t.append('All_' + element)
    return tuple(t)


def metrics_by_group(df, grouping, population_csv=None):
    """ Allow grouping by multiple columns, e.g. race and sex

    grouping: str or list of str

    examples:
    # Calculate the metrics for each racial group across all traffic stops
    mdf = metrics_by_group(raw_data_df, 'DriverRace')

    # Calculate yearly metrics by driver sex for each agency
    mdf = metrics_by_group(raw_data_df, ['AgencyName', 'Year', 'DriverSex'])
    """
    if isinstance(grouping, str):
        grouping = [grouping]
    metric_data = {}
    pop_df = None
    if population_csv:
        pop_df = pd.read_csv(population_csv)
        pop_df = pop_df.set_index('agency_name')

    # Make the aggregate tuples and groupings
    for i in range(1, len(grouping) + 1):
        for sub_cats in itertools.combinations(grouping, i):
            print('Grouping by', sub_cats)
            for group_name_tup, group_df in tqdm.tqdm(df.groupby(list(sub_cats))):
                population = get_population(pop_df, sub_cats, group_name_tup)
                metrics = calc_metrics(group_df, population=population)
                # Make a new list with the name replaced with "all" in the correct order
                new_name = get_new_tuple_name(group_name_tup, sub_cats, grouping)
                for (group_col_name, group_name) in zip(grouping, new_name):
                    metrics[group_col_name] = group_name
                metric_data[new_name] = metrics

    print('Calculating overall metrics...')
    total_population = None if not pop_df else pop_df.loc['ILLINOIS STATE POLICE', 'total']
    all_metrics = calc_metrics(df, population=total_population)
    for name in grouping:
        all_metrics[name] = 'All_' + name
    all_tup = tuple(['All_' + g for g in grouping])
    metric_data[all_tup] = all_metrics

    met_df = pd.DataFrame(metric_data).T

    print('Done!')
    return met_df


def get_population(pop_df, grouping, group):
    # If we don't have a population dataframe, just return NaN
    if not pop_df:
        return np.NaN

    if not isinstance(group, tuple):
        group = (group, )
    # Try to get the population but return the population of Illinois as a default
    try:
        name_index = grouping.index('AgencyName')
        ret = pop_df.loc[group[name_index].upper()]
    except ValueError:
        ret = pop_df.loc['ILLINOIS STATE POLICE']
    except KeyError:
        return np.NaN

    # Translate between the Census race categories and the ITSS Form race categories
    try:
        race_index = grouping.index('DriverRace')
        translation = RACE_TRANSLATION[group[race_index]]
        ret = ret[translation]
    except ValueError:
        translation = RACE_TRANSLATION['All_DriverRace']
        ret = ret[translation]
    return ret
