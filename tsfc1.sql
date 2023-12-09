PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE amount_types (
	id INTEGER NOT NULL, 
	type VARCHAR, 
	ingredient_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id)
);
CREATE TABLE dishes (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO dishes VALUES(1,'Taco Beef');
INSERT INTO dishes VALUES(2,'Frietje Rendang');
INSERT INTO dishes VALUES(3,'Taco Shrimp');
INSERT INTO dishes VALUES(4,'Popcorn Shrimp');
CREATE TABLE ingredients (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	amount_type VARCHAR, 
	storage_type VARCHAR, 
	waste_type VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO ingredients VALUES(1,'Birria','grams','Vaccum bags','Meat');
INSERT INTO ingredients VALUES(2,'Avo Smash','grams','Hoedje','Base');
INSERT INTO ingredients VALUES(3,'Onion Coriander','grams','Hoedje','Topping');
INSERT INTO ingredients VALUES(4,'Mojo Rojo','grams','Bottle','Sauce');
INSERT INTO ingredients VALUES(5,'Rendang','grams','Vaccum bags','Meat');
INSERT INTO ingredients VALUES(6,'Fries','grams','Fries Packaging','Side');
INSERT INTO ingredients VALUES(7,'Danish Cheese','grams','Cheese Packaging','Topping');
INSERT INTO ingredients VALUES(8,'SS Cucumber','grams','Hoedje','Topping');
INSERT INTO ingredients VALUES(9,'Shrimp','pieces','Shrimp Packaging','Fish');
INSERT INTO ingredients VALUES(10,'Salsa Verde','grams','Bottle','Sauce');
INSERT INTO ingredients VALUES(11,'Pico de Gallo','grams','Hoedje','Topping');
INSERT INTO ingredients VALUES(12,'Iceberg Lettuce','grams','Hoedje','Vegetables');
INSERT INTO ingredients VALUES(13,'Tempura Batter','grams','Tempura Packaging','Other');
INSERT INTO ingredients VALUES(14,'Yuzu Mayonaise','grams','Bottle','Sauce');
CREATE TABLE dish_ingredients (
	id INTEGER NOT NULL, 
	dish_id INTEGER, 
	ingredient_id INTEGER, 
	amount INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(dish_id) REFERENCES dishes (id), 
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id)
);
INSERT INTO dish_ingredients VALUES(1,1,1,85);
INSERT INTO dish_ingredients VALUES(2,1,2,25);
INSERT INTO dish_ingredients VALUES(3,1,3,25);
INSERT INTO dish_ingredients VALUES(4,1,4,15);
INSERT INTO dish_ingredients VALUES(5,2,5,120);
INSERT INTO dish_ingredients VALUES(6,2,6,80);
INSERT INTO dish_ingredients VALUES(7,2,7,50);
INSERT INTO dish_ingredients VALUES(8,2,8,25);
INSERT INTO dish_ingredients VALUES(9,3,9,2);
INSERT INTO dish_ingredients VALUES(10,3,10,30);
INSERT INTO dish_ingredients VALUES(11,3,11,40);
INSERT INTO dish_ingredients VALUES(12,3,12,25);
INSERT INTO dish_ingredients VALUES(13,3,13,24);
INSERT INTO dish_ingredients VALUES(14,4,9,5);
INSERT INTO dish_ingredients VALUES(15,4,14,60);
INSERT INTO dish_ingredients VALUES(16,4,13,60);
CREATE TABLE waste (
	id INTEGER NOT NULL, 
	dish_id INTEGER, 
	ingredient_id INTEGER, 
	dish_name VARCHAR, 
	ingredient_name VARCHAR, 
	amount FLOAT NOT NULL, 
	waste_type VARCHAR, 
	date DATE, 
	entry_time TIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(dish_id) REFERENCES dishes (id), 
	FOREIGN KEY(ingredient_id) REFERENCES ingredients (id)
);
INSERT INTO waste VALUES(1,1,1,'Taco Beef','Birria',1800.0,'Meat','2023-11-04','11:24:21.989962');
INSERT INTO waste VALUES(2,2,5,'Frietje Rendang','Rendang',2300.0,'Meat','2023-11-04','11:24:21.995012');
INSERT INTO waste VALUES(3,1,1,'Taco Beef','Birria',1500.0,'Meat','2023-11-05','11:24:22.000692');
INSERT INTO waste VALUES(4,2,5,'Frietje Rendang','Rendang',2000.0,'Meat','2023-11-05','11:24:22.004843');
INSERT INTO waste VALUES(5,1,1,'Taco Beef','Birria',1000.0,'Meat','2023-11-06','11:24:22.009986');
INSERT INTO waste VALUES(6,2,5,'Frietje Rendang','Rendang',3500.0,'Meat','2023-11-07','11:24:22.015090');
INSERT INTO waste VALUES(7,1,1,'Taco Beef','Birria',2200.0,'Meat','2023-11-07','11:24:22.021760');
INSERT INTO waste VALUES(8,2,5,'Frietje Rendang','Rendang',3500.0,'Meat','2023-11-08','11:24:22.026362');
INSERT INTO waste VALUES(9,1,1,'Taco Beef','Birria',1500.0,'Meat','2023-11-08','11:24:22.032103');
INSERT INTO waste VALUES(10,1,1,'Taco Beef','Birria',800.0,'Meat','2023-11-09','11:24:22.037895');
INSERT INTO waste VALUES(11,1,1,'Taco Beef','Birria',600.0,'Meat','2023-11-10','11:24:22.042431');
COMMIT;
