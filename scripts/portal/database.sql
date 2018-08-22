use onion_analysis;
drop table anomalies_bangalore,anomalies_mumbai,anomalies_delhi,anomalies_lucknow;
drop table mandiarrival_bangalore,mandiarrival_mumbai,mandiarrival_delhi,mandiarrival_lucknow;
drop table mandiprice_bangalore,mandiprice_mumbai,mandiprice_delhi,mandiprice_lucknow;
drop table retail_bangalore,retail_mumbai,retail_delhi,retail_lucknow;
drop table semi_labels_bangalore,semi_labels_mumbai,semi_labels_delhi,semi_labels_lucknow;

create table anomalies_bangalore ( id int PRIMARY KEY, start_date DATE, end_date DATE, category int);
create table anomalies_mumbai ( id int PRIMARY KEY, start_date DATE, end_date DATE, category int);
create table anomalies_lucknow ( id int PRIMARY KEY, start_date DATE, end_date DATE, category int);
create table anomalies_delhi ( id int PRIMARY KEY, start_date DATE, end_date DATE, category int);
create table mandiarrival_bangalore (date DATE, arrival DOUBLE); 
create table mandiarrival_mumbai (date DATE, arrival DOUBLE); 
create table mandiarrival_delhi (date DATE, arrival DOUBLE); 
create table mandiarrival_lucknow (date DATE, arrival DOUBLE); 

create table mandiprice_mumbai (date DATE, price DOUBLE); 
create table mandiprice_delhi (date DATE, price DOUBLE); 
create table mandiprice_lucknow (date DATE, price DOUBLE); 
create table mandiprice_bangalore (date DATE, price DOUBLE); 

create table retail_bangalore (date DATE, price DOUBLE); 
create table retail_mumbai (date DATE, price DOUBLE); 
create table retail_delhi (date DATE, price DOUBLE); 
create table retail_lucknow (date DATE, price DOUBLE); 

create table semi_labels_bangalore (label int); 
create table semi_labels_mumbai (label int); 
create table semi_labels_delhi (label int); 
create table semi_labels_lucknow (label int); 

load data local infile 'semi_labels_lucknow.csv' into table semi_labels_lucknow fields terminated by ',' lines terminated by '\n';
load data local infile 'semi_labels_delhi.csv' into table semi_labels_delhi fields terminated by ',' lines terminated by '\n';
load data local infile 'semi_labels_mumbai.csv' into table semi_labels_mumbai fields terminated by ',' lines terminated by '\n';
load data local infile 'semi_labels_bangalore.csv' into table semi_labels_bangalore fields terminated by ',' lines terminated by '\n';

load data local infile '../portal2/mandiarrival_lucknow.csv' into table mandiarrival_lucknow fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/mandiarrival_delhi.csv' into table mandiarrival_delhi fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/mandiarrival_mumbai.csv' into table mandiarrival_mumbai fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/mandiarrival_bangalore.csv' into table mandiarrival_bangalore fields terminated by ',' lines terminated by '\n';


load data local infile '../portal2/mandiprice_lucknow.csv' into table mandiprice_lucknow fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/mandiprice_delhi.csv' into table mandiprice_delhi fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/mandiprice_mumbai.csv' into table mandiprice_mumbai fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/mandiprice_bangalore.csv' into table mandiprice_bangalore fields terminated by ',' lines terminated by '\n';


load data local infile '../portal2/retail_lucknow.csv' into table retail_lucknow fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/retail_delhi.csv' into table retail_delhi fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/retail_mumbai.csv' into table retail_mumbai fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/retail_bangalore.csv' into table retail_bangalore fields terminated by ',' lines terminated by '\n';


load data local infile '../portal2/anomalies_lucknow.csv' into table anomalies_lucknow fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/anomalies_delhi.csv' into table anomalies_delhi fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/anomalies_mumbai.csv' into table anomalies_mumbai fields terminated by ',' lines terminated by '\n';
load data local infile '../portal2/anomalies_bangalore.csv' into table anomalies_bangalore fields terminated by ',' lines terminated by '\n';






