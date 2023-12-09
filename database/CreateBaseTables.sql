BEGIN TRANSACTION;

CREATE TABLE dishes (
    id INT NOT NULL PRIMARY KEY IDENTITY, 
    name VARCHAR(255) UNIQUE
);


CREATE TABLE ingredients (
    id INT NOT NULL PRIMARY KEY IDENTITY, 
    name VARCHAR(255) UNIQUE, 
    amount_type VARCHAR(50), 
    storage_type VARCHAR(50), 
    waste_type VARCHAR(50)
);

CREATE TABLE dish_ingredients (
    id INT NOT NULL PRIMARY KEY IDENTITY, 
    dish_id INT, 
    ingredient_id INT, 
    amount INT, 
    FOREIGN KEY(dish_id) REFERENCES dishes (id), 
    FOREIGN KEY(ingredient_id) REFERENCES ingredients (id)
);

CREATE TABLE waste (
    id INT NOT NULL PRIMARY KEY IDENTITY, 
    dish_id INT, 
    ingredient_id INT, 
    dish_name VARCHAR(255), 
    ingredient_name VARCHAR(255), 
    amount FLOAT NOT NULL, 
    waste_type VARCHAR(50), 
    date DATE, 
    entry_time TIME, 
    FOREIGN KEY(dish_id) REFERENCES dishes (id), 
    FOREIGN KEY(ingredient_id) REFERENCES ingredients (id)
);

INSERT INTO dishes (name) VALUES('Taco Beef');
INSERT INTO dishes (name) VALUES('Frietje Rendang');
INSERT INTO dishes (name) VALUES('Taco Shrimp');
INSERT INTO dishes (name) VALUES('Popcorn Shrimp');

INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Birria','grams','Vaccum bags','Meat');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Avo Smash','grams','Hoedje','Base');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Onion Coriander','grams','Hoedje','Topping');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Mojo Rojo','grams','Bottle','Sauce');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Rendang','grams','Vaccum bags','Meat');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Fries','grams','Fries Packaging','Side');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Danish Cheese','grams','Cheese Packaging','Topping');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('SS Cucumber','grams','Hoedje','Topping');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Shrimp','pieces','Shrimp Packaging','Fish');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Salsa Verde','grams','Bottle','Sauce');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Pico de Gallo','grams','Hoedje','Topping');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Iceberg Lettuce','grams','Hoedje','Vegetables');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Tempura Batter','grams','Tempura Packaging','Other');
INSERT INTO ingredients (name, amount_type, storage_type, waste_type) VALUES('Yuzu Mayonaise','grams','Bottle','Sauce');

INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(1,1,85);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(1,2,25);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(1,3,25);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(1,4,15);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(2,5,120);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(2,6,80);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(2,7,50);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(2,8,25);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(3,9,2);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(3,10,30);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(3,11,40);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(3,12,25);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(3,13,24);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(4,9,5);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(4,14,60);
INSERT INTO dish_ingredients (dish_id, ingredient_id, amount) VALUES(4,13,60);

INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,1800.0,'Meat','2023-11-04','11:24:21.989962');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(2,5,2300.0,'Meat','2023-11-04','11:24:21.995012');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,1500.0,'Meat','2023-11-05','11:24:22.000692');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(2,5,2000.0,'Meat','2023-11-05','11:24:22.004843');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,1000.0,'Meat','2023-11-06','11:24:22.009986');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(2,5,3500.0,'Meat','2023-11-07','11:24:22.015090');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,2200.0,'Meat','2023-11-07','11:24:22.021760');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(2,5,3500.0,'Meat','2023-11-08','11:24:22.026362');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,1500.0,'Meat','2023-11-08','11:24:22.032103');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,800.0,'Meat','2023-11-09','11:24:22.037895');
INSERT INTO waste (dish_id, ingredient_id, amount, waste_type, date, entry_time) VALUES(1,1,600.0,'Meat','2023-11-10','11:24:22.042431');

COMMIT;