import unittest
from decimal import Decimal
from api import *

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.api = CrimeDataAPI()


    # test for valid input checks

    def test_is_valid_location(self):
        location = "Minneapolis"
        self.assertTrue(self.api.is_valid_location(location))
    
    def test_is_not_valid_location(self):
        location = "asdfasdfa"
        self.assertFalse(self.api.is_valid_location(location))

    # tests for function 1
    def test_highest_CR_city_in_US(self):
        level = "City"
        upperLevel = "US"
        expectedResult = [('Lakeside', 'Colorado', 157, 8)]
        self.assertEqual(self.api.find_area_with_highest_crime_rate_among(level, upperLevel), expectedResult)
    
    def test_highest_CR_state_in_US(self):
        level = "State"
        upperLevel = "US"
        expectedResult = [('Colorado', Decimal('0.19478926456975261225'))]
        self.assertEqual(self.api.find_area_with_highest_crime_rate_among(level, upperLevel), expectedResult)

    def test_highest_CR_city_in_state(self):
        level = "City"
        upperLevel = "Minnesota"
        expectedResult = [('Waite Park', Decimal('0.09975762214568184717'))]
        self.assertEqual(self.api.find_area_with_highest_crime_rate_among(level, upperLevel), expectedResult)

    # tests for function 2
    def test_lowest_CR_city_in_US(self):
        level = "City"
        upperLevel = "US"
        expectedResult =[('Skagway', 'Alaska', 0, 1202, 102)]
        self.assertEqual(self.api.find_area_with_lowest_crime_rate_among(level, upperLevel), expectedResult)
    
    def test_lowest_CR_state_in_US(self):
        level = "State"
        upperLevel = "US"
        expectedResult = [('Pennsylvania', Decimal('0.00814513769513013573'))]
        self.assertEqual(self.api.find_area_with_lowest_crime_rate_among(level, upperLevel), expectedResult)

    def test_lowest_CR_city_in_state(self):
        level = "City"
        upperLevel = "Minnesota"
        expectedResult = [('Caledonia', Decimal('0E-20'))]
        self.assertEqual(self.api.find_area_with_lowest_crime_rate_among(level, upperLevel), expectedResult)
    

     # tests for function 3
    def test_most_common_violent_crime_in_US(self):
        location = "US"
        expectedResult = [('aggravated_assault', Decimal('423666'))]
        self.assertEqual(self.api.find_most_common_violent_crime_in(location), expectedResult)

    def test_most_common_violent_crime_in_state(self):
        location = "Minnesota"
        expectedResult = [('aggravated_assault', Decimal('9188'))]
        self.assertEqual(self.api.find_most_common_violent_crime_in(location), expectedResult)

    def test_most_common_violent_crime_in_city(self):
        location = "Minneapolis"
        expectedResult = [('aggravated_assault', Decimal('2962'))]
        self.assertEqual(self.api.find_most_common_violent_crime_in(location), expectedResult)
        

    # tests for function 4
    def test_least_common_violent_crime_in_US(self):
        location = "US"
        expectedResult = [('murder_and_nnm', Decimal('9981'))]
        self.assertEqual(self.api.find_least_common_violent_crime_in(location), expectedResult)

    def test_least_common_violent_crime_in_state(self):
        location = "Minnesota"
        expectedResult = [('murder_and_nnm', Decimal('188'))]
        self.assertEqual(self.api.find_least_common_violent_crime_in(location), expectedResult)

    def test_least_common_violent_crime_in_city(self):
        location = "Minneapolis"
        expectedResult = [('murder_and_nnm', Decimal('94'))]
        self.assertEqual(self.api.find_least_common_violent_crime_in(location), expectedResult)

    # tests for function 5
    def test_most_common_property_crime_in_US(self):
        location = "US"
        expectedResult = [('larceny_theft', Decimal('2152368'))]
        self.assertEqual(self.api.find_most_common_property_crime_in(location), expectedResult)

    def test_most_common_property_crime_in_state(self):
        location = "Minnesota"
        expectedResult = [('larceny_theft', Decimal('76471'))]
        self.assertEqual(self.api.find_most_common_property_crime_in(location), expectedResult)
    def test_most_common_property_crime_in_city(self):
        location = "Minneapolis"
        expectedResult = [('larceny_theft', Decimal('11648'))]
        self.assertEqual(self.api.find_most_common_property_crime_in(location), expectedResult)
        
    # tests for function 6
    def test_least_common_property_crime_in_US(self):
        location = "US"
        expectedResult = [('arson', Decimal('17801'))]
        self.assertEqual(self.api.find_least_common_property_crime_in(location), expectedResult)

    def test_least_common_property_crime_in_state(self):
        location = "Minnesota"
        expectedResult = [('arson', Decimal('618'))]
        self.assertEqual(self.api.find_least_common_property_crime_in(location), expectedResult)

    def test_least_common_property_crime_in_city(self):
        location = "Minneapolis"
        expectedResult = [('arson', Decimal('116'))]
        self.assertEqual(self.api.find_least_common_property_crime_in(location), expectedResult)

    # tests for function 7
        # city and violent crime

    def test_percent_of_a_violent_crime_out_of_total_offenses_committed_in_city(self):
        location = "Minneapolis"
        crimeType = "robbery"
        expectedResult = [(Decimal('0.09'),)]
        self.assertEqual(self.api.percent_of_crime_type_committed(crimeType, location), expectedResult)

        # city and property crime
    def test_percent_of_a_property_crime_out_of_total_offenses_committed_in_city(self):
        location = "Minneapolis"
        crimeType = "burglary"
        expectedResult = [(Decimal('0.11'),)] # actually 0.12? 
        self.assertEqual(self.api.percent_of_crime_type_committed(crimeType, location), expectedResult)

        # state and violent crime
    def test_percent_of_a_violent_crime_out_of_total_offenses_committed_in_state(self):
        location = "Minnesota"
        crimeType = "robbery"
        expectedResult = [(Decimal('0.03'),)]
        self.assertEqual(self.api.percent_of_crime_type_committed(crimeType, location), expectedResult)

        # state and property crime
    def test_percent_of_a_property_crime_out_of_total_offenses_committed_in_state(self):
        location = "Minnesota"
        crimeType = "burglary"
        expectedResult = [(Decimal('0.10'),)]
        self.assertEqual(self.api.percent_of_crime_type_committed(crimeType, location), expectedResult)

        # US and violent crime
    def test_percent_of_a_violent_crime_out_of_total_offenses_committed_in_US(self):
        location = "US"
        crimeType = "robbery"
        expectedResult = [(Decimal('0.03'),)]
        self.assertEqual(self.api.percent_of_crime_type_committed(crimeType, location), expectedResult)

        # US and property crime
    def test_percent_of_a_property_crime_out_of_total_offenses_committed_in_US(self):
        location = "US"
        crimeType = "burglary"
        expectedResult = [(Decimal('0.12'),)]
        self.assertEqual(self.api.percent_of_crime_type_committed(crimeType, location), expectedResult)

    
    # tests for function 8
        # city and violent crime
    def test_num_of_violent_crime_committed_in_city(self):
        location = "Minneapolis"
        crimeType = "robbery"
        expectedResult = [(2215,)]
        self.assertEqual(self.api.num_of_crime_type_committed(crimeType, location), expectedResult)

        # city and property crime
    def test_num_of_property_crime_committed_in_city(self):
        location = "Minneapolis"
        crimeType = "burglary"
        expectedResult = [(2531,)]
        self.assertEqual(self.api.num_of_crime_type_committed(crimeType, location), expectedResult)

        # state and violent crime
    def test_num_of_violent_crime_committed_in_state(self):
        location = "Minnesota"
        crimeType = "robbery"
        expectedResult = [(3768,)]
        self.assertEqual(self.api.num_of_crime_type_committed(crimeType, location), expectedResult)

        # state and property crime
    def test_num_of_property_crime_committed_in_state(self):
        location = "Minnesota"
        crimeType = "burglary"
        expectedResult = [(12037,)]
        self.assertEqual(self.api.num_of_crime_type_committed(crimeType, location), expectedResult)

        # US and violent crime
    def test_num_of_violent_crime_committed_in_US(self):
        location = "US"
        crimeType = "robbery"
        expectedResult = [(94235,)]
        self.assertEqual(self.api.num_of_crime_type_committed(crimeType, location), expectedResult)

        # US and property crime
    def test_num_of_property_crime_committed_in_US(self):
        location = "US"
        crimeType = "burglary"
        expectedResult = [(430015,)]
        self.assertEqual(self.api.num_of_crime_type_committed(crimeType, location), expectedResult)
    
    # tests for function 9
    def test_violent_crime_by_weapon_MN(self):
        weapon = "Handgun"
        expectedResult = [(5346,)]
        self.assertEqual(self.api.violent_crime_by_weapon_in_MN(weapon), expectedResult)
    

    # tests for function 10
    def test_percent_of_crime_by_age_MN_100to50(self):
        upper = 50
        lower = 100
        expectedResult = None
        self.assertEqual(self.api.percent_of_crime_by_age_in_MN(lower,upper), expectedResult)

    def test_percent_of_crime_by_age_MN_200to500(self):
        lower = 200
        upper = 500
        expectedResult = None
        self.assertEqual(self.api.percent_of_crime_by_age_in_MN(lower,upper), expectedResult)

    #upper>=lower ||  #upper>=lower ||  #upper>=lower ||  #upper>=lower
    def test_percent_of_crime_by_age_MN_50to100(self):
        upper = 100
        lower = 50
        expectedResult = [(Decimal('0.05'),)]
        self.assertEqual(self.api.percent_of_crime_by_age_in_MN(lower,upper), expectedResult)
    
    
    #check when upper==lower || #check when upper==lower || #check when upper==lower || #check when upper==lower
    def test_percent_of_crime_by_age_MN_50to50(self):
        upper = 50
        lower = 50
        expectedResult = [(Decimal('0.01'),)]
        self.assertEqual(self.api.percent_of_crime_by_age_in_MN(lower,upper), expectedResult)

    
    #check when upper>max age(120) ||  #check when upper>max age(120)  ||   #check when upper>max age(120)
    #THIS SHOULD NOT BE AN ISSUE OR THROW AN ERROR
    def test_percent_of_crime_by_age_MN_50to200(self):
        upper = 200
        lower = 50
        expectedResult = [(Decimal('0.05'),)]
        self.assertEqual(self.api.percent_of_crime_by_age_in_MN(lower,upper), expectedResult)

    # tests for function 11
    def test_percent_of_crime_by_ethnicity_MN(self):
        ethnicity = "Hispanic or Latino"
        expectedResult = [(Decimal('0.02'),)]
        self.assertEqual(self.api.percent_of_crime_by_ethnicity_in_MN(ethnicity), expectedResult)
    
    #test for invalid input 

    # tests for function 12
    def test_percent_of_crime_by_race_MN(self):
        race = "White"
        expectedResult = [(Decimal('0.23'),)]
        self.assertEqual(self.api.percent_of_crime_by_race_in_MN(race), expectedResult)
    
    #test for invalid input 

    # tests for function 13
    def test_percent_of_crime_by_sex_MN(self):
        sex = "M"
        expectedResult = [(Decimal('0.38'),)]
        self.assertEqual(self.api.percent_of_crime_by_sex_in_MN(sex), expectedResult)

    def test_percent_of_crime_by_invalid_sex_MN(self):
        sex = "Male"
        expectedResult = None
        self.assertEqual(self.api.percent_of_crime_by_sex_in_MN(sex), expectedResult)
    

    #test for invalid input 
        


if __name__ == "__main__":
    unittest.main()
    