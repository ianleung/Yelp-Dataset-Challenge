
ALTER TABLE business ADD PRIMARY KEY (business_id);

ALTER TABLE BusinessHours ADD FOREIGN KEY (business_id) REFERENCES business(business_id);

ALTER TABLE Neighbourhoods ADD FOREIGN KEY (business_id) REFERENCES business(business_id);

ALTER TABLE Categories ADD FOREIGN KEY (business_id) REFERENCES business(business_id);

ALTER TABLE Attributes ADD PRIMARY KEY (business_id, attribute_name);

ALTER TABLE Attributes ADD FOREIGN KEY (business_id) REFERENCES business(business_id);
