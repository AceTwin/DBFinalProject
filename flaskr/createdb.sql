DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Professors;
DROP TABLE IF EXISTS Classes;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Headmaster;
DROP TABLE IF EXISTS Grades;
DROP TABLE IF EXISTS Wand;
DROP TABLE IF EXISTS House;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS ExtraCurricular;

CREATE TABLE Student (
stuId NUMERIC(5) PRIMARY KEY,
lastName VARCHAR2(20),
firstName VARCHAR2(20),
GPA DECIMAL(3,2),
House VARCHAR2(20),
Schedule VARCHAR2(3),
FOREIGN KEY(House) REFERENCES House(HouseName),
FOREIGN KEY(GPA) REFERENCES Grades(GPA));
 
CREATE TABLE Professors (
ProfID VARCHAR2(5) PRIMARY KEY,
name VARCHAR2(20),
subject VARCHAR2(20));
 
CREATE TABLE Classes (
classTitle VARCHAR2(25) PRIMARY KEY,
ProfID VARCHAR2(5) NOT NULL,
NumStud NUMBER(6),
FOREIGN KEY(ProfID) REFERENCES Professors(ProfID));
 
CREATE TABLE Room (
RoomId VARCHAR2(5) PRIMARY KEY,
classTaught VARCHAR2(25) NOT NULL,
Condition VARCHAR2(25),
FOREIGN KEY(classTaught) REFERENCES Classes(classTitle));

CREATE TABLE Headmaster (
Name VARCHAR2(25) PRIMARY KEY,
start_date DATE,
end_Date DATE,
NumYears NUMBER(3));

CREATE TABLE Grades (
Semester VARCHAR2(20),
GPA DECIMAL(3,2),
stuId NUMERIC(5),
PRIMARY KEY (Semester, GPA),
FOREIGN KEY(stuId) REFERENCES Students(stuId));

CREATE TABLE Wand (
WandId VARCHAR2(5) PRIMARY KEY,
WCondition VARCHAR2(25),
Core VARCHAR2(25),
StudFName VARCHAR2(20),
StudLName VARCHAR2(20),
FOREIGN KEY(StudFName) REFERENCES Students(firstName),
FOREIGN KEY(StudLName) REFERENCES Students(lastName));

CREATE TABLE House (
HouseName VARCHAR2(5) PRIMARY KEY,
Mascot VARCHAR2(7),
Location VARCHAR2(7));

CREATE TABLE Books (
bID VARCHAR2(5) PRIMARY KEY,
classRequired VARCHAR2(25),
NumPages NUMBER2(7),
FOREIGN KEY(classRequired) REFERENCES Classes(classTitle));

CREATE TABLE ExtraCurricular (
Clubs VARCHAR2(25) PRIMARY KEY,
Season VARCHAR2(7));

INSERT INTO Student VALUES (9876, "Potter", "Harry", 3.7, "Gryffindor", "MWF");
INSERT INTO Student VALUES (7643, "Lovegood", "Luna", 3.87, "Ravenclaw", "MWTH");
INSERT INTO Student VALUES (4536, "Cornel", "Cara", 3.9, "Gryffindor", "TWF");
INSERT INTO Student VALUES (4785, "Granger", "Hermione", 4.0, "Gryffindor", "MWF");
INSERT INTO Student VALUES (5252, "Weasley", "Ron", 3.2, "Gryffindor", "MW");
INSERT INTO Student VALUES (9222, "Weasley", "George", 3.5, "Gryffindor", "MTW");
INSERT INTO Professors VALUES ("P903232", "Larson", "Dark Magic");
INSERT INTO Professors VALUES ("P905555", "Alsop", "Transfiguration");
INSERT INTO Professors VALUES ("P905567", "Harrison", "Potions");
INSERT INTO Headmaster VALUES ("Snape", "12-01-1992", "12-01-2050", 3);
INSERT INTO Classes VALUES ("Potions", "P905567", 5);
INSERT INTO Classes VALUES ("Transfiguration", "P905555", 3);
INSERT INTO Classes VALUES ("Dark Magic", "P903232", 4);
INSERT INTO Room VALUES ("R3465", "Potions", "Good");
INSERT INTO Room VALUES ("R5632", "Dark Magic", "Disrepair");
INSERT INTO Room VALUES ("R3334", "Transfiguration", "Meh");
INSERT INTO Grades VALUES ("Fall", 3.7, 9876);
INSERT INTO Grades VALUES ("Winter", 3.87, 7643);
INSERT INTO Grades VALUES ("Spring", 3.9, 4536);
INSERT INTO Grades VALUES ("Fall",4.0, 4785);
INSERT INTO Grades VALUES ("Winter", 3.2, 5252);
INSERT INTO Grades VALUES ("Fall", 3.5, 9222);
INSERT INTO Wand VALUES ("W5235", "Poor", "Wood", "Harry", "Potter");
INSERT INTO Wand VALUES ("W5236", "Good", "Pine", "Luna", "Lovegood");
INSERT INTO Wand VALUES ("W5237", "Meh", "Stone", "Cara", "Cornel");
INSERT INTO Wand VALUES ("W5238", "Poor", "Wood", "Hermione", "Granger");
INSERT INTO Wand VALUES ("W5239", "Destroyed", "Pine", "Ron", "Weasley");
INSERT INTO Wand VALUES ("W5240", "Ok", "Stone", "George", "Weasley");
INSERT INTO House VALUES ("GRIFF", "Lion", "WestTower");
INSERT INTO House VALUES ("RAVEN", "Raven", "DownHall");
INSERT INTO House VALUES ("SLYTH", "Snake", "Underground");
INSERT INTO House VALUES ("HUFFLE", "Badger", "SomewhereElse");
INSERT INTO ExtraCurricular VALUES ("Quiddich", "Fall");
INSERT INTO ExtraCurricular VALUES ("Chess", "Winter");
INSERT INTO Books VALUES ("Trannys", "Transfiguration", 200);
INSERT INTO Books VALUES ("Blow shiz up", "Dark Magic", 200);
INSERT INTO Books VALUES ("Drink me", "Potions", 200);
