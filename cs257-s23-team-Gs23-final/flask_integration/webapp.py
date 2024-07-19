import flask
from flask import render_template
import json
import sys
from api import *
from url import *

app = flask.Flask(__name__)

violent_crime_types = ["murder_and_nnm","rape","robbery","aggravated_assault"]
property_crime_types = ["burglary","larceny_theft","motor_vehicle_theft","arson"]

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    US_map = map_urls.get_heat_map_URL("US")
    return render_template('home.html', US_map = US_map)

@app.route('/about')
def about_the_data():
    return render_template('about_this_data.html')

@app.route('/state_result/<state>/')
def state_results(state):
    '''
    The user query we implemented is the user wanting to find the crime statistic 
    information for the state of Iowa. They do this by clicking the Iowa link in the left
    navigation.
    '''

    # creating crime type count lists for bar charts
    violent_crime_counts = []
    for crime_type in violent_crime_types:
        result = api.num_of_crime_type_committed(crime_type, state)
        if result != None:
            result = result[0][0]
            violent_crime_counts.append(result)

    property_crime_counts = []
    for crime_type in property_crime_types:
        result = api.num_of_crime_type_committed(crime_type, state)
        result = result[0][0]
        if result != None: 
            property_crime_counts.append(result)
    
    # aggregated list for pie chart
    crime_type_values = property_crime_counts + violent_crime_counts
                    
    # store the highest and lowest cities
    result = api.find_area_with_highest_crime_rate_among("City", state)
    city_highest_CR = result[0][0]
    result = api.find_area_with_lowest_crime_rate_among("City",state)
    city_lowest_CR = result[0][0]
    # url stuff for embedded maps
    heat_map_url = map_urls.get_heat_map_URL(state)
    US_map = map_urls.get_heat_map_URL("US")
    highest_CR_map = map_urls.get_highest_CR_map_URL(state)
    lowest_CR_map = map_urls.get_lowest_CR_map_URL(state)

    #store the crime rate and ranking of the stat
    result = api.get_crime_rate_and_ranking_for(state)
    state_CR = result[0][1]
    state_ranking = result [0][2]

    return render_template('state_results.html', 
                           state=state, 
                           heat_map_url=heat_map_url, 
                           US_map = US_map, 
                           highest_CR_map=highest_CR_map, 
                           lowest_CR_map=lowest_CR_map, 
                           city_highest_CR=city_highest_CR,
                           city_lowest_CR=city_lowest_CR,
                           crime_type_values=crime_type_values, 
                           property_crime_counts=property_crime_counts, 
                           violent_crime_counts=violent_crime_counts,
                           state_CR = state_CR,
                           state_ranking = state_ranking,)

'''
Run the program by typing 'python3 localhost [port]', where [port] is one of 
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    api = CrimeDataAPI()
    map_urls = EmbeddedURLs()

    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
