import psycopg2
import psqlConfig as config



# Declaring global lists to be used in input check functions 
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
violent_crime_types = ["murder_and_nnm","rape","robbery","aggravated_assault"]
property_crime_types = ["burglary","larceny_theft","motor_vehicle_theft","arson"]
valid_weapons = ['Firearm', 'Firearm (Automatic)', 'Handgun', 'Handgun (Automatic)', 'Rifle', 'Rifle (Automatic)', 'Shotgun', 'Shotgun (Automatic)', 'Other Firearm', 'Other Firearm (Automatic)', 'Knife/Cutting Instrument', 'Blunt Object', 'Motor Vehicle/Vessel', 'Poison', 'Explosives', 'Fire/Incendiary Device', 'Drugs/Narcotics/Sleeping Pills', 'Asphyxiation', 'Other', 'Unknown', 'Personal Weapons', 'None', 'Unarmed', 'Lethal Cutting Instrument', 'Club/Blackjack/Brass Knuckles', 'Pushed or Thrown Out Window', 'Drowning', 'Strangulation - Include Hanging']
valid_races = ['Unknown', 'White', 'Black or African American', 'American Indian or Alaska Native', 'Asian', 'Native Hawaiian or Other Pacific Islander', 'Multiple', 'Not Specified']
valid_ethnicities= ['Hispanic or Latino', 'Not Hispanic or Latino', 'Multiple', 'Unknown', 'Not Specified']



class CrimeDataAPI:
    def __init__(self):
        '''
        Reads in and stores the data from the specified file(s) as a list of dictionaries, for use by the rest of the functions in the class.
        
        PARAMETER
            filename - the name (and path, if not in the current working directory) of the data file
        '''
        self.connection = self.connect()

    def connect(self): 
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection    
        

    # functions to check for valid inputs

    def is_valid_location(self, location):
        if location == "US" or location in states:
            return True
        else:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM national_offenses WHERE city = %s", (location,))
                result = cursor.fetchone()[0]
                return result > 0
            except Exception as e:
                print ("Something went wrong when executing the query: ", e)
                return False    
                    

    def is_valid_crime_type(self, crime_type):
        return crime_type in violent_crime_types or crime_type in property_crime_types
    
    def is_valid_weapon(self, weapon):
        return weapon in valid_weapons
    
    def is_valid_race(self, race):
        return race in valid_races
    
    def is_valid_ethnicity(self, ethnicity):
        return ethnicity in valid_ethnicities
    
    def is_valid_age_range(self,low, high):
        try: 
            low = int(low)
            high = int(high)
        except ValueError:
            return None
        low,high = int(low), int(high)
        if low < 0 or high > 200:
            return None
        elif low > high:
            return None
        return True

    # Functions to use for US
              
    # 1      
    def find_area_with_highest_crime_rate_among(self, level, upperLevel):
        """finds the <level> within <upperLevel> that has the highest number of crimes per person 
    Args:
        level (str): indicates at the city or state level 
        upperLevel (str): indicates the parent level (US or specific state)
    Returns:
        str: the name of the specific city, county, or state    
        """

        if upperLevel == "US":
            if level == "City":
                query = "SELECT city, state, total_offenses, population FROM national_offenses WHERE (total_offenses *1.0 /population) = (Select MAX(total_offenses *1.0 /population) FROM national_offenses);"
            elif level == "State":
                query = "SELECT state, AVG(total_offenses*1.0/population) AS crime_rate FROM national_offenses GROUP BY state ORDER BY crime_rate DESC LIMIT 1;"
            else:
                return "Invalid input, please only enter City or State (case senstitive)"
        elif upperLevel in states:
            if level == "City":                         
                query = "SELECT city, (total_offenses*1.0/population) as crime_rate FROM national_offenses WHERE state = %s ORDER BY crime_rate DESC LIMIT 1;" 
            else: 
                return "Invalid input, please only enter City for State Upper Level"
        else: 
            return "Invalid input, please enter US or a valid US state. \n (Keep in mind our dataset does not have data on Florida or District of Columbia)"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (upperLevel,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None        

    # 2
    def find_area_with_lowest_crime_rate_among(self, level, upperLevel):
        """finds the <level> within <upperLevel> that has the lowest number of crimes per person 
    Args:
        level (str): indicates at the city, county, or state level
        upperLevel (str): indicates the parent level (county, state, or country)
    Returns:
        str: the name of the specific city or state 
        """
        if upperLevel == "US":
            if level == "City":
                query = "SELECT city, state, total_offenses, population, (SELECT COUNT(*) FROM national_offenses WHERE (total_offenses * 1.0 / population) = (SELECT MIN(total_offenses * 1.0 / population) FROM national_offenses)) AS num_cities FROM national_offenses WHERE (total_offenses * 1.0 / population) = (SELECT MIN(total_offenses * 1.0 / population) FROM national_offenses) LIMIT 1;"
            elif level == "State":
                query = "SELECT state, AVG(total_offenses*1.0/population) AS crime_rate FROM national_offenses GROUP BY state ORDER BY crime_rate ASC LIMIT 1;"
            else:
                return "Invalid input, please only enter City or State (case senstitive)"
        elif upperLevel in states:
            if level == "City":                         
                query = "SELECT city, (total_offenses*1.0/population) as crime_rate FROM national_offenses WHERE state = %s ORDER BY crime_rate ASC LIMIT 1;" 
            else: 
                return "Invalid input, please only enter City for State Upper Level"
        else: 
            return "Invalid input, please enter US or a valid US state. \n (Keep in mind our dataset does not have data on Florida or District of Columbia)"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (upperLevel,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 


    # 3
    def find_most_common_violent_crime_in(self, location):
        """Gets and prints the type of the violent crime with the highest occurrence in the location specified
    Args:
        location (str): The specific city or state, or the US
    Returns:
        str: the type of the violent crime with the highest occurrence 
    """ 
        if not self.is_valid_location(location):
            return None
        
        if location == 'US':            # most common in the US
            query = "SELECT violent_crime_type, SUM(count) AS total_counts FROM (SELECT 'murder_and_nnm' AS violent_crime_type, SUM(murder_and_nnm) AS count FROM national_offenses UNION ALL SELECT 'rape' AS violent_crime_type, SUM(rape) AS count  FROM national_offenses UNION ALL SELECT 'robbery' AS violent_crime_type, SUM(robbery) AS count FROM national_offenses UNION ALL SELECT 'aggravated_assault' AS violent_crime_type, SUM(aggravated_assault) AS count FROM national_offenses) AS violent_crime_counts GROUP BY violent_crime_type ORDER BY total_counts DESC LIMIT 1;"
        elif location in states:      #most common in a specific state
            query = "SELECT violent_crime_type, SUM(count) AS total_counts FROM (SELECT 'murder_and_nnm' AS violent_crime_type, SUM(murder_and_nnm) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'rape' AS violent_crime_type, SUM(rape) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'robbery' AS violent_crime_type, SUM(robbery) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'aggravated_assault' AS violent_crime_type, SUM(aggravated_assault) AS count FROM national_offenses WHERE state = %s) AS violent_crime_counts GROUP BY violent_crime_type ORDER BY total_counts DESC LIMIT 1;"
        else:   #most common in a specific city
            query = "SELECT violent_crime_type, SUM(count) AS total_counts FROM (SELECT 'murder_and_nnm' AS violent_crime_type, SUM(murder_and_nnm) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'rape' AS violent_crime_type, SUM(rape) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'robbery' AS violent_crime_type, SUM(robbery) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'aggravated_assault' AS violent_crime_type, SUM(aggravated_assault) AS count FROM national_offenses WHERE city = %s) AS violent_crime_counts GROUP BY violent_crime_type ORDER BY total_counts DESC LIMIT 1;"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (location, location, location, location))
            return cursor.fetchall()
        
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 

    #4
    def find_least_common_violent_crime_in(self, location):
        """Gets and prints the type of the violent crime with the lowest occurrence
    Args:
        location (str): The city, county, or state in the dataset that shows your the crime occurred
    Returns:
        str: the type of the violent crime with the lowest occurrence 
    """
        if not self.is_valid_location(location):
            return None

        if location == 'US': # most common in US
            query = "SELECT violent_crime_type, SUM(count) AS total_counts FROM (SELECT 'murder_and_nnm' AS violent_crime_type, SUM(murder_and_nnm) AS count FROM national_offenses UNION ALL SELECT 'rape' AS violent_crime_type, SUM(rape) AS count FROM national_offenses UNION ALL SELECT 'robbery' AS violent_crime_type, SUM(robbery) AS count FROM national_offenses UNION ALL SELECT 'aggravated_assault' AS violent_crime_type, SUM(aggravated_assault) AS count FROM national_offenses) AS violent_crime_counts GROUP BY violent_crime_type ORDER BY total_counts ASC LIMIT 1;"
            
        elif location in states: #most common in a specific state
            query = "SELECT violent_crime_type, SUM(count) AS total_counts FROM (SELECT 'murder_and_nnm' AS violent_crime_type, SUM(murder_and_nnm) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'rape' AS violent_crime_type, SUM(rape) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'robbery' AS violent_crime_type, SUM(robbery) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'aggravated_assault' AS violent_crime_type, SUM(aggravated_assault) AS count FROM national_offenses WHERE state = %s) AS violent_crime_counts GROUP BY violent_crime_type ORDER BY total_counts ASC LIMIT 1;"

        else: #most common in a specific city
            query = "SELECT violent_crime_type, SUM(count) AS total_counts FROM (SELECT 'murder_and_nnm' AS violent_crime_type, SUM(murder_and_nnm) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'rape' AS violent_crime_type, SUM(rape) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'robbery' AS violent_crime_type, SUM(robbery) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'aggravated_assault' AS violent_crime_type, SUM(aggravated_assault) AS count FROM national_offenses WHERE city = %s) AS violent_crime_counts GROUP BY violent_crime_type ORDER BY total_counts ASC LIMIT 1;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(location, location, location, location))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None             
    #5
    def find_most_common_property_crime_in(self, location):
        """Gets and prints the type of the property crime with the most occurrence
    Args:
        location (str): The city, county, or state in the dataset that shows your the crime occurred
    Returns:
        str: the type of the property
 crime with the most occurrence 
    """
        if not self.is_valid_location(location):
            return None
        
        if location == 'US': # most common in US    #copied wrong
            query = "SELECT property_crime_type, SUM(count) AS total_counts FROM (SELECT 'burglary' AS property_crime_type, SUM(burglary) AS count FROM national_offenses UNION ALL SELECT 'larceny_theft' AS property_crime_type, SUM(larceny_theft) AS count FROM national_offenses UNION ALL SELECT 'motor_vehicle_theft' AS property_crime_type, SUM(motor_vehicle_theft) AS count FROM national_offenses UNION ALL SELECT 'arson' AS property_crime_type, SUM(arson) AS count FROM national_offenses) AS property_crime_counts GROUP BY property_crime_type ORDER BY total_counts DESC LIMIT 1;"

        elif location in states: #most common in a specific state   #copied wrong
            query = "SELECT property_crime_type, SUM(count) AS total_counts FROM (SELECT 'burglary' AS property_crime_type, SUM(burglary) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'larceny_theft' AS property_crime_type, SUM(larceny_theft) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'motor_vehicle_theft' AS property_crime_type, SUM(motor_vehicle_theft) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'arson' AS property_crime_type, SUM(arson) AS count FROM national_offenses WHERE state = %s) AS property_crime_counts GROUP BY property_crime_type ORDER BY total_counts DESC LIMIT 1;"
        
        else: #most common in a specific city   #copied wrong
            query = "SELECT property_crime_type, SUM(count) AS total_counts FROM (SELECT 'burglary' AS property_crime_type, SUM(burglary) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'larceny_theft' AS property_crime_type, SUM(larceny_theft) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'motor_vehicle_theft' AS property_crime_type, SUM(motor_vehicle_theft) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'arson' AS property_crime_type, SUM(arson) AS count FROM national_offenses WHERE city = %s) AS property_crime_counts GROUP BY property_crime_type ORDER BY total_counts DESC LIMIT 1;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(location, location, location, location))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 
    #6
    def find_least_common_property_crime_in(self, location):
        """Gets and prints the type of the property crime with the lowest occurrence
    Args:
        location (str): The city, county, or state in the dataset that shows your the crime occurred
    Returns:
        str: the type of the property crime with the lowest occurrence 
    """
        if not self.is_valid_location(location):
            return None

        if location == 'US': # most common in US  #copied wrong
            query = "SELECT property_crime_type, SUM(count) AS total_counts FROM (SELECT 'burglary' AS property_crime_type, SUM(burglary) AS count FROM national_offenses UNION ALL SELECT 'larceny_theft' AS property_crime_type, SUM(larceny_theft) AS count FROM national_offenses UNION ALL SELECT 'motor_vehicle_theft' AS property_crime_type, SUM(motor_vehicle_theft) AS count FROM national_offenses UNION ALL SELECT 'arson' AS property_crime_type, SUM(arson) AS count FROM national_offenses) AS property_crime_counts GROUP BY property_crime_type ORDER BY total_counts ASC LIMIT 1;"

        elif location in states: #most common in a specific state  #copied wrong
            query = "SELECT property_crime_type, SUM(count) AS total_counts FROM (SELECT 'burglary' AS property_crime_type, SUM(burglary) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'larceny_theft' AS property_crime_type, SUM(larceny_theft) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'motor_vehicle_theft' AS property_crime_type, SUM(motor_vehicle_theft) AS count FROM national_offenses WHERE state = %s UNION ALL SELECT 'arson' AS property_crime_type, SUM(arson) AS count FROM national_offenses WHERE state = %s) AS property_crime_counts GROUP BY property_crime_type ORDER BY total_counts ASC LIMIT 1;"
        
        else: #most common in a specific city  #copied wrong
            query = "SELECT property_crime_type, SUM(count) AS total_counts FROM (SELECT 'burglary' AS property_crime_type, SUM(burglary) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'larceny_theft' AS property_crime_type, SUM(larceny_theft) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'motor_vehicle_theft' AS property_crime_type, SUM(motor_vehicle_theft) AS count FROM national_offenses WHERE city = %s UNION ALL SELECT 'arson' AS property_crime_type, SUM(arson) AS count FROM national_offenses WHERE city = %s) AS property_crime_counts GROUP BY property_crime_type ORDER BY total_counts ASC LIMIT 1;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(location, location, location, location))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 

    #7
    def proportion_of_crime_type_committed(self, crime_type, location):
        """Gets and prints the proportion of total crime committed by type and location the user selected
    Args:
        crime type (str): The type of the crime from the dataset the user have choosen
            options of crime type includes: 
                violent crimes: Murder and nonnegligent manslaughter, rape, robbery, and aggravated assault
                property crimes: burglary, larceny-theft, motor vehicle theft, and arson
        location (str): The city, ccounty, or state in the dataset that shows your the crime occured
    Returns:
        int: The proportion of crime committed by the crime type and location selected by the user
    """
        if not self.is_valid_crime_type(crime_type):
            return None

        if not self.is_valid_location(location):
            return None

        # divides the total number of times a crime type was committed (in US, a state, or a city) and divides it by the total offenses in that same location
        if location == 'US': 
            query = f"SELECT ROUND(SUM({crime_type} *1.0) / SUM(Total_Offenses *1.0),2) FROM national_offenses;"
        elif location in states: 
            query = f"SELECT ROUND(SUM({crime_type} *1.0) / SUM(Total_Offenses *1.0),2) FROM national_offenses WHERE state= %s"
        else: 
            query = f"SELECT ROUND(SUM({crime_type} *1.0) / SUM(Total_Offenses *1.0),2) FROM national_offenses WHERE city= %s"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (location,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 
    #8  
    def num_of_crime_type_committed(self, crime_type, location):
        """Gets and prints the number of crime committed by type and location the user selected
    Args:
        crime type (str): The type of the crime from the dataset the user have choosen
            options of crime type includes: 
                violent crimes: Murder and nonnegligent manslaughter, rape, robbery, and aggravated assault
                property crimes: burglary, larceny-theft, motor vehicle theft, and arson
        location (str): The city, ccounty, or state in the dataset that shows your the crime occured
    Returns:
        int: The number of crime committed by the crime type and location selected by the user
    """
        if not self.is_valid_crime_type(crime_type):
            return None
        if not self.is_valid_location(location):
            return None

        if location == 'US':
            query = f"SELECT SUM({crime_type}) AS total_murder_and_nnm FROM national_offenses;"
        elif location in states: 
            query = f"SELECT SUM({crime_type}) AS mn_total_murder_and_nnm FROM national_offenses WHERE state = %s;"
        else: 
            query = f"SELECT SUM({crime_type}) AS minneapolis_total_murder_and_nnm FROM national_offenses WHERE city = %s;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(location,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 


    #Functions that are only Usable with MN Data

    #9
    def violent_crime_by_weapon_in_MN(self, weapon):
        """How many violent offenses were committed by a certain weapon in all of Minnesota
    Args:
        weapon (str): fn will look for this string in the spreadsheet.
            options for weapon: Firearm, Handgun, Rifle ,Rifle (Automatic), Shotgun, etc.
    Returns:
        int: an integer value of the number of offenses where this weapon was used.
    """
        if not self.is_valid_weapon(weapon):
            return None

        query = "SELECT COUNT(weapon) AS mn_total_weapon FROM mn_weapon WHERE weapon = %s;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(weapon,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 
    #10
    def proportion_of_crime_by_age_in_MN(self, low, high):
        """Returns the proportion of crime committed by a given age group.
    Args:
        low(int): the lower bound of our age search
        high(int): the upper bound of our age search
        location(str): city, county, etc. fn will look for this str thru our data.
    Returns:int proportion of total crime committed by the specified age group.
    """
        if not self.is_valid_age_range(low, high):
            return None
        
        query = "SELECT ROUND(COUNT(CASE WHEN age BETWEEN %s AND %s THEN 1 END) *1.0 / COUNT(*),2) AS proportion_offenders_between_low_high FROM mn_offenders;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(low,high))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 
    #11
    def proportion_of_crime_by_ethnicity_in_MN(self, ethnicity):
        """Returns the proportion of crime committed by a given ethnicity.
    Args:
        ethnicity(str): ethnicity of offender
            options for ethnicity: Hispanic or Latino, Not Hispanic or Latino, Multiple, Unknown, Not Specified
        location(str): city, county, etc. fn will look for this str thru our data.
    Returns:int proportion of total crime committed by the specified ethnicity.
        """
        if not self.is_valid_ethnicity(ethnicity):
            return None
        query = "SELECT ROUND(COUNT(CASE WHEN mn_offenders.ethnicity = %s THEN 1 END) *1.0 / COUNT(*),2) AS proportion_offenders_committed_by_Ethnicity FROM mn_offenders;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(ethnicity,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 

    #12
    def proportion_of_crime_by_race_in_MN(self, race):
        """Returns the proportion of crime commmited by a given race.
    Args:
        race(str): race of offender
            options for race: Unknown, White, Black or African American, American Indian or Alaska Native, Asian, 
            Asian or Native Hawaiian or Other Pacific Islander, Chinese, Japanese, Native Hawaiian or Other Pacific Islander, 
            Other, Multiple, Not Specified
        location(str): city, county, etc. fn will look for this str thru our data.
    Returns:int proportion of total crime committed by the specified race.
        """
        if not self.is_valid_race(race):
            return None
        
        query = "SELECT ROUND(COUNT(CASE WHEN mn_offenders.race = %s THEN 1 END) *1.0 / COUNT(*),2) AS proportion_offenders_committed_by_race FROM mn_offenders;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(race,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 

    #13
    def proportion_of_crime_by_sex_in_MN(self, sex):
        """Returns the proportion of crime commmited by a given sex.
    Args:
        gender(str): sex of offender
            options for sex: M, F, Not Specified
    Returns:int proportion of total crime committed by the specified sex.
        """
        if not sex == "M" and not sex == "F" and not sex == "X":
            return None
        query = "SELECT ROUND(COUNT(CASE WHEN mn_offenders.sex = %s THEN 1 END) *1.0 / COUNT(*),2) AS proportion_offenders_committed_by_sex FROM mn_offenders;"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query,(sex,))
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None 

if __name__ == "__main__":
    crime = CrimeDataAPI()
    print (crime.find_area_with_highest_crime_rate_among("City", "US"))
    print (crime.find_area_with_lowest_crime_rate_among("City", "US"))
    #crime.get_highest_CR_city_in_US()
    #connection.close() 
    
