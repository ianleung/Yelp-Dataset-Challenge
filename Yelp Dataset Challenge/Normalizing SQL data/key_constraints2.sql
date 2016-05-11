CREATE DATABASE Lab5Test;
USE Lab5Test;

#create tables
CREATE TABLE Tip (`type` VARCHAR(100), business_id VARCHAR(100), text VARCHAR(1000), user_id VARCHAR(100), date DATE, likes INT);

CREATE TABLE `User` (`type` VARCHAR(100), user_id VARCHAR(100), name VARCHAR(100), review_count INT, average_stars VARCHAR(100), yelping_since DATE, fans INT);
CREATE TABLE UserEliteYears(user_id VARCHAR(100),years INT);
CREATE TABLE UserCompliments(user_id VARCHAR(100), profile INT, cute INT, funny INT, plain INT, list INT, writer INT, note INT, photos INT, hot INT, cool INT, more INT, useful INT);
CREATE TABLE UserVotes(user_id VARCHAR(100),funny INT, useful INT, cool INT);
CREATE TABLE UserFriends (user_id VARCHAR(100), friend_id VARCHAR(100));

CREATE TABLE Checkin(`type` VARCHAR(100), business_id VARCHAR(100));
CREATE TABLE CheckinHours(`business_id` VARCHAR(100), `day_hour` VARCHAR(100),`count` INT);

CREATE TABLE Business (type VARCHAR(100), business_id VARCHAR(100), name VARCHAR(100), full_address VARCHAR(1000), review_count INT, city VARCHAR(1000),state VARCHAR(1000), latitude INT, longitude INT, stars FLOAT(10,2),open VARCHAR(10));
CREATE TABLE BusinessHours (business_id VARCHAR(100), day VARCHAR(100), time VARCHAR(10));
CREATE TABLE BusinessCategories (business_id VARCHAR(100),categories VARCHAR(100));
CREATE TABLE BusinessNeighbourhoods (business_id VARCHAR(100),hood_name VARCHAR(100));
CREATE TABLE BusinessAttributes (business_id VARCHAR(100), attribute_name VARCHAR(50), attribute_value VARCHAR(50));

CREATE TABLE Review(user_id VARCHAR(100), review_id VARCHAR(100), business_id VARCHAR(100));
CREATE TABLE ReviewInfo(review_id VARCHAR(100), review_text VARCHAR(10000),review_date DATE, type VARCHAR(10));
CREATE TABLE ReviewVotes(review_id VARCHAR(100), votes__useful INT, votes__funny INT, votes__cool INT);


#add primary keys
ALTER TABLE User ADD PRIMARY KEY (user_id);
ALTER TABLE Business ADD PRIMARY KEY (business_id);
ALTER TABLE Review ADD PRIMARY KEY (review_id);
#insert into tables user and business
#foreign keys for tip
ALTER TABLE Tip ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE Checkin ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE Review ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE Review ADD FOREIGN KEY (user_id) REFERENCES User(user_id);

#foreignkeys for user
ALTER TABLE UserEliteYears ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE UserCompliments ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE UserVotes ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE UserFriends ADD FOREIGN KEY (user_id) REFERENCES user(user_id);
ALTER TABLE UserFriends ADD FOREIGN KEY (friend_id) REFERENCES user(user_id);

#foreignkeys for checkin
ALTER TABLE Checkin ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE CheckinHours ADD FOREIGN KEY(business_id) REFERENCES Business(business_id);

#foreignkeys for business
ALTER TABLE BusinessHours ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE BusinessNeighbourhoods ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE BusinessCategories ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);
ALTER TABLE BusinessAttributes ADD PRIMARY KEY (business_id, attribute_name);
ALTER TABLE BusinessAttributes ADD FOREIGN KEY (business_id) REFERENCES Business(business_id);

#foreignkeys for review
ALTER TABLE ReviewInfo ADD FOREIGN KEY (review_id) REFERENCES Review(review_id);
ALTER TABLE ReviewVotes ADD FOREIGN KEY (review_id) REFERENCES Review(review_id);
