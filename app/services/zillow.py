
import requests
import json
from fake_useragent import UserAgent
import urllib.parse

def zillow_scraper(query: str,get_all_pages=False) -> dict:

    # create a request session

    headers = {
        'accept': '*/*',
        'x-caller-id': 'static-search-page-graphql',
        'content-type': 'application/json'
    }
    page=1

    ua = UserAgent()
    headers['user-agent'] = ua.chrome
    session = requests.Session()

    request_body = {
        "operationName": "getAutocompleteResults",
        "variables": {
            "query": query,
            "queryOptions": {"maxResults": 1, "userSearchContext": "FOR_SALE"},
            "resultType": ["REGIONS", "FORSALE", "RENTALS", "SOLD", "SEMANTIC_REGIONS", "BUILDER_COMMUNITIES"]
        },
        "query": "query getAutocompleteResults($query: String!, $queryOptions: SearchAssistanceQueryOptions, $resultType: [SearchAssistanceResultType]) {\n  searchAssistanceResult: zgsAutocompleteRequest(\n    query: $query\n    queryOptions: $queryOptions\n    resultType: $resultType\n  ) {\n    requestId\n    results {\n      __typename\n      id\n      ...RegionResultFields\n      ...SemanticResultFields\n      ...RentalCommunityResultFields\n      ...BuilderCommunityResultFields\n    }\n  }\n}\n\nfragment RegionResultFields on SearchAssistanceRegionResult {\n  regionId\n  subType\n}\n\nfragment SemanticResultFields on SearchAssistanceSemanticResult {\n  nearMe\n  regionIds\n  regionTypes\n  regionDisplayIds\n  queryResolutionStatus\n  viewLatitudeDelta\n  filters {\n    basementStatusType\n    baths {\n      min\n      max\n    }\n    beds {\n      min\n      max\n    }\n    excludeTypes\n    hoaFeesPerMonth {\n      min\n      max\n    }\n    homeType\n    keywords\n    listingStatusType\n    livingAreaSqft {\n      min\n      max\n    }\n    lotSizeSqft {\n      min\n      max\n    }\n    parkingSpots {\n      min\n      max\n    }\n    price {\n      min\n      max\n    }\n    searchRentalFilters {\n      monthlyPayment {\n        min\n        max\n      }\n      petsAllowed\n      rentalAvailabilityDate {\n        min\n        max\n      }\n    }\n    searchSaleFilters {\n      daysOnZillow {\n        min\n        max\n      }\n    }\n    showOnlyType\n    view\n    yearBuilt {\n      min\n      max\n    }\n  }\n}\n\nfragment RentalCommunityResultFields on SearchAssistanceRentalCommunityResult {\n  location {\n    latitude\n    longitude\n  }\n}\n\nfragment BuilderCommunityResultFields on SearchAssistanceBuilderCommunityResult {\n  plid\n}\n"
    }
    url=f'https://www.zillow.com/zg-graph?query={urllib.parse.quote(query)}&queryOptions=&resultType=REGIONS&resultType=FORSALE&resultType=RENTALS&resultType=SOLD&resultType=SEMANTIC_REGIONS&resultType=BUILDER_COMMUNITIES&operationName=getAutocompleteResults'
    url_manual=f'https://www.zillow.com/zg-graph?query={urllib.parse.quote(query)}&queryOptions=&resultType=REGIONS&resultType=FORSALE&resultType=RENTALS&resultType=SOLD&resultType=SEMANTIC_REGIONS&querySource=MANUAL&operationName=getQueryUnderstandingResults'
    response = session.post(url, headers=headers, data=json.dumps(request_body))
    # get json from response
    json_data = response.json()
    if not json_data['data']['searchAssistanceResult']['results']:
        response = session.post(url_manual, headers=headers, data=json.dumps(request_body))
        json_data = response.json()
    # get data from json
    region_id = json_data['data']['searchAssistanceResult']['results'][0].get('regionId', None)
    if not region_id:
        region_id =json_data['data']['searchAssistanceResult']['results'][0]['regionIds'][0]

    bounds_url = 'https://www.zillow.com/async-create-search-page-state'
    bounds_body = {"searchQueryState": {"regionSelection": [{"regionId": region_id}]}, "wants": {"regionResults": ["regionResults"]}}
    response = session.put(bounds_url, headers=headers, data=json.dumps(bounds_body))
    json_data = response.json()

    # get regionBounds from json
    region_bounds = json_data['regionState']['regionBounds']

    result_url = 'https://www.zillow.com/async-create-search-page-state'
    result_body = {
        "searchQueryState": {
            "isMapVisible": False,
            "mapBounds": region_bounds,
            "filterState": {"sortSelection": {"value": "globalrelevanceex"}, "isAllHomes": {"value": True}},
            "isListVisible": True,
            "category": "cat1",
            "regionSelection": [{"regionId": region_id}],
            "usersSearchTerm": query,
            "pagination": {"currentPage": page}
        },
        "wants": {"cat1": ["listResults"], "cat2": ["total"]}
    }

    response = session.put(result_url, headers=headers, data=json.dumps(result_body))
    json_data = response.json()
    if get_all_pages:
        while True:
            page += 1
            result_body = {
                "searchQueryState": {
                    "isMapVisible": False,
                    "mapBounds": region_bounds,
                    "filterState": {"sortSelection": {"value": "globalrelevanceex"}, "isAllHomes": {"value": True}},
                    "isListVisible": True,
                    "category": "cat1",
                    "regionSelection": [{"regionId": region_id}],
                    "usersSearchTerm": query,
                    "pagination": {"currentPage": page}
                },
                "wants": {"cat1": ["listResults"], "cat2": ["total"]}
            }
            response = session.put(result_url, headers=headers, data=json.dumps(result_body))
            print(f'current page: {page}')
            if  len(response.json()['cat1']['searchResults']['listResults'])==0:
                break
            json_data['cat1']['searchResults']['listResults'].extend(response.json()['cat1']['searchResults']['listResults'])
            print(len(json_data['cat1']['searchResults']['listResults']))

    return json_data
