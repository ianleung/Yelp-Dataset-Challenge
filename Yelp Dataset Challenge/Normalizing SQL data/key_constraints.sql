CREATE Database Lab2Test2;
USE Lab2Test2;
#create tables
CREATE TABLE tip (`type` VARCHAR(100), business_id VARCHAR(100), text VARCHAR(1000), user_id VARCHAR(100), date DATE, likes INT);
CREATE TABLE `user` (`type` VARCHAR(100), user_id VARCHAR(100), name VARCHAR(100), review_count INT, average_stars VARCHAR(100), yelping_since VARCHAR(100), fans INT);
CREATE TABLE EliteYears(user_id VARCHAR(100),years INT);
CREATE TABLE ComplimentsTable(user_id VARCHAR(100), profile INT, cute INT, funny INT, plain INT, list INT, writer INT, note INT, photos INT, hot INT, cool INT, more INT, useful INT);
CREATE TABLE VotesTable(user_id VARCHAR(100),funny INT, useful INT, cool INT);
CREATE TABLE FriendTable (user_id VARCHAR(100), friend_id VARCHAR(100));
CREATE TABLE checkin(`type` VARCHAR(100), business_id VARCHAR(100));
CREATE TABLE CheckinHoursTable(`business_id` VARCHAR(100), `day_hour` VARCHAR(100),`count` INT);
CREATE TABLE business (type VARCHAR(100), business_id VARCHAR(100), name VARCHAR(100), full_address VARCHAR(1000), review_count INT, city VARCHAR(1000),state VARCHAR(1000), latitude INT, longitude INT, stars FLOAT(10,2),open VARCHAR(10));
CREATE TABLE BusinessHours (business_id VARCHAR(100), day VARCHAR(100), time VARCHAR(10));
CREATE TABLE Categories (business_id VARCHAR(100),categories VARCHAR(100));
CREATE TABLE Neighbourhoods (business_id VARCHAR(100),hood_name VARCHAR(100));
CREATE TABLE Attributes (business_id VARCHAR(100), attribute_name VARCHAR(50), attribute_value VARCHAR(50));

#add primary keys
ALTER TABLE user ADD PRIMARY KEY (user_id);
ALTER TABLE business ADD PRIMARY KEY (business_id);
#insert into tables user and business
#foreign keys for tip
ALTER TABLE tip ADD FOREIGN KEY (business_id) REFERENCES business(business_id);

#foreignkeys for user
ALTER TABLE EliteYears ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE ComplimentsTable ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE VotesTable ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE FriendTable ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE FriendTable ADD FOREIGN KEY (friend_id) REFERENCES user(user_id);

#foreignkeys for checkin
ALTER TABLE checkin ADD FOREIGN KEY (business_id) references business(business_id);

#foreignkeys for business
ALTER TABLE BusinessHours ADD FOREIGN KEY (business_id) REFERENCES business(business_id);
ALTER TABLE Neighbourhoods ADD FOREIGN KEY (business_id) REFERENCES business(business_id);
ALTER TABLE Categories ADD FOREIGN KEY (business_id) REFERENCES business(business_id);
ALTER TABLE Attributes ADD PRIMARY KEY (business_id, attribute_name);
ALTER TABLE Attributes ADD FOREIGN KEY (business_id) REFERENCES business(business_id);


