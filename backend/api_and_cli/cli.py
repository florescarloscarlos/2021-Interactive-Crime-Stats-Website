from api import *
crime_inputs = {"Murder and nonnegligent manslaughter": "murder_and_nnm","Rape": "rape","Robbery": "robbery","Aggravated assault": "aggravated_assault","Burglary": "burglary","Larceny theft": "larceny_theft","Motor vehicle theft": "motor_vehicle_theft","Arson": "arson"}
crime_outputs = {'murder_and_nnm': 'Murder and nonnegligent manslaughter', 'rape': 'Rape', 'robbery': 'Robbery', 'aggravated_assault': 'Aggravated assault', 'burglary': 'Burglary', 'larceny_theft': 'Larceny theft', 'motor_vehicle_theft': 'Motor vehicle theft', 'arson': 'Arson'}
def display_function_menu():
    print("Welcome to our Command Line Interface on Crime Data in the US and Minnesota")
    print("Please read the following options\n")
    print("(1) Get the city/county/state with the highest crime rate")
    print("(2) Get the city/county/state with the lowest crime rate")
    print("(3) Get the most common violent crime in a city, state, or the country")
    print("(4) Get the least common violent crime in a city, state, or the country")
    print("(5) Get the most common property crime offense in a city, state, or the country")
    print("(6) Get the least common property crime offense in a city, state, or the country")
    print("(7) Given a certain crime type, get the proportionage of total crime that it makes up in a city, state, or the US") 
    print("(8) Given a certain crime type, get the number of crimes committed in a city, state, or the US") 
    print("\nFor some more in depth data, these statistics are applicable to Minnesota only")
    print("(9) Get number of violent offenses that were committed by a certain weapon")
    print("(10) Get the proportion of crime committed by a given age group")
    print("(11) Get the proportion of crime committed by a given ethnicity")
    print("(12) Get the proportion of crime committed by a given race")
    print("(13) Get the proportion of crime committed by a given sex")

def input_location_with_scope():
    upper_level = input("Do you want to find this statistic across the US or within a specific state(enter the state if so without abbreviation)? ")
    lower_level = input("What geographical level would you like the statistic to be based on? \n(Enter only these options: City, State) ") 
    return upper_level,lower_level
    
def input_specific_location(): 
    location = input("What specific location do you want to find this statistic for? \n(Options: US, a specific state (i.e Minnesota), or a specific city (i.e. Minneapolis)) ") 
    return location

def input_crime_type(): 
    crime_type = input("What type of crime do you want to find this statistic for? \n (Options: Murder and nonnegligent manslaughter, Rape, Robbery, and Aggravated assault \n Burglary, Larceny theft, Motor vehicle theft, Arson \n Write these to match case with capitalization and underscores): ")
    return change_to_proper_name(crime_type)

def change_to_proper_name(crime_type):
    if crime_type in crime_inputs:
        crime_type = crime_inputs[crime_type]
    return crime_type


def run_function(num):
    if num == 1:
        # Do you want to find the highest CR across the US or within a specific state? 
        # At what level of location are you interested in finding the highest crime rate (city, county or state)? 
        while True:
            upper_level,lower_level = input_location_with_scope()
            result = api.find_area_with_highest_crime_rate_among(lower_level, upper_level) 
            if "Invalid input," not in result:
                break
            print (result)
        if upper_level == "US" and lower_level == "City":
            result = result[0][0] +","+result[0][1]
        else:
            result = result[0][0]
        print(result + " has the highest crime rate for a " + lower_level + " in " + upper_level +".\n")
        return
    elif num == 2:
        while True:
            upper_level,lower_level = input_location_with_scope()
            result = api.find_area_with_lowest_crime_rate_among(lower_level, upper_level)
            if "Invalid input," not in result:
                break 
            print(result)
        if upper_level == "US" and lower_level == "City":
            result_city = result[0][0] +","+result[0][1]
            print(result_city + " is one of the "+ str(result[0][4]) +" cities with the lowest crime rate for a " + lower_level + " in " + upper_level +".\n")        
        else:
            result = result[0][0]
            print(result + " is the lowest crime rate for a " + lower_level + " in " + upper_level +".\n")        
        return 
    elif num == 3: 
        #remember to think abt states w/ same name as cities in the future
        while True:
            location = input_specific_location()
            result = api.find_most_common_violent_crime_in(location)
            if result is not None:
                break   
            print ("Invalid input, no data for the location you specified.")  
        print("The most common violent crime offense in", location, "was", crime_outputs.get(result[0][0]) +".\n")        
        return
    elif num == 4:
        while True:
            location = input_specific_location()
            result = api.find_least_common_violent_crime_in(location)
            if result is not None:
                break
            print("Invalid input, no data for the location you specified.")
        print("The least common violent crime offense in", location, "was", crime_outputs.get(result[0][0])+".\n")     
        return
    elif num == 5:
        while True:
            location = input_specific_location()
            result = api.find_most_common_property_crime_in(location)
            if result is not None:
                break
            print ("Invalid input, no data for the location you specified.")
        print("The most common property crime offense in", location, "was", crime_outputs.get(result[0][0]))+".\n"
        return

    elif num == 6: 
        while True: 
            location = input_specific_location()
            result = api.find_least_common_property_crime_in(location)
            if result is not None:
                break
            print("Invalid input, no data for the location you specified.")
        print("The least common property crime offense in", location, "was"+ crime_outputs.get(result[0][0])+".\n")
        return
    elif num == 7:
        while True: 
            crime_type = input_crime_type()
            location = input_specific_location()
            result = api.proportion_of_crime_type_committed(crime_type, location)
            if result is not None:
                break
            print("Invalid input. Make sure the Crime Type and Location you entered are valid inputs.")
        print ("The proportion of all crime", crime_outputs.get(crime_type), "makes up in", location, "was", str(result[0][0])+".\n")
        return
    elif num == 8:
        while True:
            crime_type = input_crime_type()
            location = input_specific_location()
            result = api.num_of_crime_type_committed(crime_type, location)
            if result is not None:
                break
            print("Invalid input. Make sure the Crime Type and Location you entered are valid inputs.")
        print ("The number of", crime_outputs.get(crime_type),"committed in", location, "was", str(result[0][0])+".\n")
        return
    elif num == 9: 
        while True:
            weapon_type = input("What weapon type do you want to find this statistic for? \n (Options: Firearm, Firearm (Automatic), Handgun, Handgun (Automatic), Rifle (Automatic), \n Shotgun, Shotgun (Automatic), Other Firearm, Other Firearm (Automatic), Knife/Cutting Instrument, Blunt Object, \n Motor Vehicle/Vessel, Poison, Explosives, Fire/Incendiary Device, Drugs/Narcotics/Sleeping Pills, \nAsphyxiation, Other, Unknown, Personal Weapons, None, Unarmed, Lethal Cutting Instrument, \n Club/Blackjack/Brass Knuckles, Pushed or Thrown Out Window, Drowning, Strangulation - Include Hanging) \n")
            result = api.violent_crime_by_weapon_in_MN(weapon_type)
            if result is not None:
                break
            print("Invalid input. Please make sure the Weapon Type you entered are valid inputs.")
        print("The number of violent offenses committed by", weapon_type, "in Minnesota was", str(result[0][0])+".\n")
        return
    elif num == 10:
        while True: 
            age_low = (input("What's the lower bound of your age range?"))
            age_high = (input("What's the upper bound of your age range?"))
            result = api.proportion_of_crime_by_age_in_MN(age_low, age_high)
            if result is not None:
                break
            print("Invalid input. Please make sure the low and high values of your age range are valid inputs.")
        print ("The proportion of total crime committed by the age range "+age_low+"-"+age_high+ " in Minnesota was", str(result[0][0])+".\n")
        return        
    elif num == 11:
        while True:
            ethnicity = input("What specific ethnicity do you want to find this statisticfor? \n Options: Hispanic or Latino, Not Hispanic or Latino, Multiple, Unknown, Not Specified): ")
            result = api.proportion_of_crime_by_ethnicity_in_MN(ethnicity)
            if result is not None:
                break
            print("Invalid input. Please make sure the Ethnicity you entered are valid inputs.")
        print("The proportion of total crime committed by the specified ethnicity ("+ ethnicity+ ") in Minnesota was", str(result[0][0])+".\n")
    elif num == 12: 
        while True:
            race = input("What specific race do you want to find this statistic for? \n Options: 'Unknown', 'White', 'Black or African American', 'American Indian or Alaska Native', 'Asian', 'Native Hawaiian or Other Pacific Islander', 'Multiple', 'Not Specified': ")
            result = api.proportion_of_crime_by_race_in_MN(race)
            if result is not None:
                break
            print("Invalid input. Please make sure the race you entered are valid inputs.")
        print("The proportion of total crime committed by the specified race ("+ race+ ") in Minnesota was", str(result[0][0])+".\n")
        return
    elif num == 13:
        while True:
            sex = input("What specific sex do you want to find this statistic for? \n(Options: M, F, X) Only enter X if you wan't data for crimes where the Sex of the offender is unknown: ")
            result = api.proportion_of_crime_by_sex_in_MN(sex)
            if result is not None:
                break
            print("Invalid input. Please make sure the sex you entered are valid inputs.")
        print("The proportion of total crime committed by the specified sex ("+ sex+ ") in Minnesota was", str(result[0][0])+".\n")
        return

def CLI():
    display_function_menu()
    while True:
        selection = (input("Enter the number of the statistic you want to learn more about: "))
        if selection.isdigit():
            selection = int(selection)
            run_function(selection)
            break
        print("Invalid input. Please enter an integer.")    

def main():
    continue_prompt = ""
    while continue_prompt.lower() != "quit":
        CLI()
        continue_prompt = (input("Type 'quit' to end your session or press the ENTER key to explore more statistics. "))
        

if __name__ == "__main__":
    api = CrimeDataAPI()

    main()

    
    
    

    




        



        