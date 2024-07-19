DROP TABLE IF EXISTS national_offenses;
CREATE TABLE national_offenses (
  state text,
  city text,
  population integer,
  total_offenses integer,
  violent_crime integer,
  murder_and_nnm integer,
  rape integer,
  robbery integer,
  aggravated_assault integer,
  property_crime integer,
  burglary integer,
  larceny_theft integer,
  motor_vehicle_theft integer,
  arson integer
);

DROP TABLE IF EXISTS mn_offenders;
CREATE TABLE mn_offenders (
  offender_id integer,
  incident_id integer,
  age integer, 
  sex text,
  race text,
  ethnicity text
);


DROP TABLE IF EXISTS mn_weapon;
CREATE TABLE mn_weapon (
  weapon text,
  offense_id integer
);










