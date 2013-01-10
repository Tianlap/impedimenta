-- ************************************************************
-- LUNCHES DATABASE TABLES:
--     L_EMPLOYEES
--     L_FOODS
--     L_DEPARTMENTS
--     L_LUNCHES
--     L_LUNCH_ITEMS
--     L_SUPPLIERS
--     L_CONSTANTS
-- ************************************************************

DROP DATABASE lunches;
CREATE DATABASE lunches;
USE lunches;

CREATE TABLE L_EMPLOYEES
(
    EMPLOYEE_ID     INT(3) PRIMARY KEY AUTO_INCREMENT,
    FIRST_NAME      VARCHAR(10) NOT NULL,
    LAST_NAME       VARCHAR(20) NOT NULL,
    DEPT_CODE       VARCHAR(3),
    HIRE_DATE       DATE,
    CREDIT_LIMIT    DECIMAL(4,2),
    PHONE_NUMBER    VARCHAR(4),
    MANAGER_ID      INT(3)
) ENGINE=InnoDB;
ALTER TABLE L_EMPLOYEES AUTO_INCREMENT = 201;

INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'SUSAN', 'BROWN', 'EXE', STR_TO_DATE('01-06-1998', '%d-%m-%Y'), 30, '3484', NULL);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'JIM', 'KERN', 'SAL', STR_TO_DATE('16-08-1999', '%d-%m-%Y'), 25, '8722', 201);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'MARTHA', 'WOODS', 'SHP', STR_TO_DATE('02-02-2009', '%d-%m-%Y'), 25, '7591', 201);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'ELLEN', 'OWENS', 'SAL', STR_TO_DATE('01-07-2008', '%d-%m-%Y'), 15, '6830', 202);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'HENRY', 'PERKINS', 'SAL', STR_TO_DATE('01-03-2006', '%d-%m-%Y'), 25, '5286', 202);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'CAROL', 'ROSE', 'ACT', NULL, NULL, NULL, NULL);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'DAN', 'SMITH', 'SHP', STR_TO_DATE('01-12-2008', '%d-%m-%Y'), 25, '2259', 203);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'FRED', 'CAMPBELL', 'SHP', STR_TO_DATE('01-04-2008', '%d-%m-%Y'), 25, '1752', 203);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'PAULA', 'JACOBS', 'MKT', STR_TO_DATE('17-03-1999', '%d-%m-%Y'), 15, '3357', 201);
INSERT INTO L_EMPLOYEES VALUES
  (NULL, 'NANCY', 'HOFFMAN', 'SAL', STR_TO_DATE('16-02-2007', '%d-%m-%Y'), 25, '2974', 203);
COMMIT;

-- *************************************

CREATE TABLE L_FOODS
(
    SUPPLIER_ID     VARCHAR(3),
    PRODUCT_CODE    VARCHAR(2),
    MENU_ITEM       DECIMAL(2),
    DESCRIPTION     VARCHAR(20),
    PRICE           DECIMAL(4,2),
    PRICE_INCREASE  DECIMAL(4,2),
    PRIMARY KEY     (SUPPLIER_ID, PRODUCT_CODE)
) ENGINE=InnoDB;

INSERT INTO L_FOODS VALUES ('ASP', 'FS', 1, 'FRESH SALAD', 2, 0.25);
INSERT INTO L_FOODS VALUES ('ASP', 'SP', 2, 'SOUP OF THE DAY', 1.5, NULL);
INSERT INTO L_FOODS VALUES ('ASP', 'SW', 3, 'SANDWICH', 3.5, 0.4);
INSERT INTO L_FOODS VALUES ('CBC', 'GS', 4, 'GRILLED STEAK', 6, 0.7);
INSERT INTO L_FOODS VALUES ('CBC', 'SW', 5, 'HAMBURGER', 2.5, 0.3);
INSERT INTO L_FOODS VALUES ('FRV', 'BR', 7, 'BROCCOLI', 1, 0.05);
INSERT INTO L_FOODS VALUES ('FRV', 'FF', 7, 'FRENCH FRIES', 1.5, NULL);
INSERT INTO L_FOODS VALUES ('JBR', 'AS', 8, 'SODA', 1.25, 0.25);
INSERT INTO L_FOODS VALUES ('JBR', 'VR', 9, 'COFFEE', 0.85, 0.15);
INSERT INTO L_FOODS VALUES ('VSB', 'AS', 10, 'DESSERT', 3, 0.5);
COMMIT;

-- *************************************

CREATE TABLE L_DEPARTMENTS
(
    DEPT_CODE           VARCHAR(3) PRIMARY KEY,
    DEPARTMENT_NAME     VARCHAR(30)
) ENGINE=InnoDB;

INSERT INTO L_DEPARTMENTS VALUES ('ACT', 'ACCOUNTING');
INSERT INTO L_DEPARTMENTS VALUES ('EXE', 'EXECUTIVE');
INSERT INTO L_DEPARTMENTS VALUES ('MKT', 'MARKETING');
INSERT INTO L_DEPARTMENTS VALUES ('PER', 'PERSONNEL');
INSERT INTO L_DEPARTMENTS VALUES ('SAL', 'SALES');
INSERT INTO L_DEPARTMENTS VALUES ('SHP', 'SHIPPING');
COMMIT;

-- *************************************

CREATE TABLE L_LUNCHES
(
    LUNCH_ID      DECIMAL(3) PRIMARY KEY,
    LUNCH_DATE    DATE,
    EMPLOYEE_ID   INT(3),
    DATE_ENTERED  DATETIME
) ENGINE=InnoDB;

INSERT INTO L_LUNCHES VALUES (1, STR_TO_DATE('16-11-2011', '%d-%m-%Y'), 201, STR_TO_DATE('13-10-2011 10:35:24', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (2, STR_TO_DATE('16-11-2011', '%d-%m-%Y'), 207, STR_TO_DATE('13-10-2011 10:35:39', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (3, STR_TO_DATE('16-11-2011', '%d-%m-%Y'), 203, STR_TO_DATE('13-10-2011 10:35:45', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (4, STR_TO_DATE('16-11-2011', '%d-%m-%Y'), 204, STR_TO_DATE('13-10-2011 10:35:58', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (6, STR_TO_DATE('16-11-2011', '%d-%m-%Y'), 202, STR_TO_DATE('13-10-2011 10:36:41', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (7, STR_TO_DATE('16-11-2011', '%d-%m-%Y'), 210, STR_TO_DATE('13-10-2011 10:38:52', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (8, STR_TO_DATE('25-11-2011', '%d-%m-%Y'), 201, STR_TO_DATE('14-10-2011 11:15:37', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (9, STR_TO_DATE('25-11-2011', '%d-%m-%Y'), 208, STR_TO_DATE('14-10-2011 14:23:36', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (12, STR_TO_DATE('25-11-2011', '%d-%m-%Y'), 204, STR_TO_DATE('14-10-2011 15:02:53', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (13, STR_TO_DATE('25-11-2011', '%d-%m-%Y'), 207, STR_TO_DATE('18-10-2011 08:42:11', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (15, STR_TO_DATE('25-11-2011', '%d-%m-%Y'), 205, STR_TO_DATE('21-10-2011 16:23:50', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (16, STR_TO_DATE('05-12-2011', '%d-%m-%Y'), 201, STR_TO_DATE('21-10-2011 16:23:59', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (17, STR_TO_DATE('05-12-2011', '%d-%m-%Y'), 210, STR_TO_DATE('21-10-2011 16:35:26', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (20, STR_TO_DATE('05-12-2011', '%d-%m-%Y'), 205, STR_TO_DATE('24-10-2011 09:55:27', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (21, STR_TO_DATE('05-12-2011', '%d-%m-%Y'), 203, STR_TO_DATE('24-10-2011 11:43:13', '%d-%m-%Y %H:%i:%s'));
INSERT INTO L_LUNCHES VALUES (22, STR_TO_DATE('05-12-2011', '%d-%m-%Y'), 208, STR_TO_DATE('24-10-2011 14:37:32', '%d-%m-%Y %H:%i:%s'));
COMMIT;

-- *************************************

CREATE TABLE L_LUNCH_ITEMS
(
    LUNCH_ID        DECIMAL(3),
    ITEM_NUMBER     DECIMAL(2),
    SUPPLIER_ID     VARCHAR(3),
    PRODUCT_CODE    VARCHAR(2),
    QUANTITY        DECIMAL(1),
    PRIMARY KEY     (LUNCH_ID, ITEM_NUMBER)
) ENGINE=InnoDB;

INSERT INTO L_LUNCH_ITEMS VALUES (1, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (1, 2, 'ASP', 'SW', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (1, 3, 'JBR', 'VR', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (2, 1, 'ASP', 'SW', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (2, 2, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (2, 3, 'JBR', 'VR', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (2, 4, 'VSB', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (3, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (3, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (3, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (3, 4, 'JBR', 'VR', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (3, 5, 'JBR', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (4, 1, 'ASP', 'SP', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (4, 2, 'CBC', 'SW', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (4, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (4, 4, 'JBR', 'AS', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (6, 1, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (6, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (6, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (6, 4, 'JBR', 'VR', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (6, 5, 'VSB', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (7, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (7, 2, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (7, 3, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (7, 4, 'JBR', 'VR', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (7, 5, 'VSB', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (8, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (8, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (8, 3, 'JBR', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (9, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (9, 2, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (9, 3, 'CBC', 'SW', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (9, 4, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (9, 5, 'JBR', 'VR', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (9, 6, 'JBR', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (12, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (12, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (12, 3, 'JBR', 'VR', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (12, 4, 'VSB', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (13, 1, 'ASP', 'SP', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (13, 2, 'ASP', 'SW', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (13, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (13, 4, 'JBR', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (15, 1, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (15, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (15, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (15, 4, 'JBR', 'AS', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (16, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (16, 2, 'ASP', 'SW', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (16, 3, 'CBC', 'SW', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (16, 4, 'JBR', 'VR', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (16, 5, 'JBR', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (17, 1, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (17, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (17, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (17, 4, 'JBR', 'VR', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (17, 5, 'VSB', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (20, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (20, 2, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (20, 3, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (20, 4, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (20, 5, 'JBR', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (21, 1, 'ASP', 'SP', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (21, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (21, 3, 'JBR', 'VR', 2);
INSERT INTO L_LUNCH_ITEMS VALUES (21, 4, 'VSB', 'AS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (22, 1, 'ASP', 'FS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (22, 2, 'CBC', 'GS', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (22, 3, 'FRV', 'FF', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (22, 4, 'JBR', 'VR', 1);
INSERT INTO L_LUNCH_ITEMS VALUES (22, 5, 'JBR', 'AS', 1);
COMMIT;

-- *************************************

CREATE TABLE L_SUPPLIERS
(
    SUPPLIER_ID      VARCHAR(3) PRIMARY KEY,
    SUPPLIER_NAME    VARCHAR(30)
) ENGINE=InnoDB;

INSERT INTO L_SUPPLIERS VALUES ('ARR', 'ALICE & RAY''S RESTAURANT');
INSERT INTO L_SUPPLIERS VALUES ('ASP', 'A SOUP PLACE');
INSERT INTO L_SUPPLIERS VALUES ('CBC', 'CERTIFIED BEEF COMPANY');
INSERT INTO L_SUPPLIERS VALUES ('FRV', 'FRANK REED''S VEGETABLES');
INSERT INTO L_SUPPLIERS VALUES ('FSN', 'FRANK & SONS');
INSERT INTO L_SUPPLIERS VALUES ('JBR', 'JUST BEVERAGES');
INSERT INTO L_SUPPLIERS VALUES ('JPS', 'JIM PARKER''S SHOP');
INSERT INTO L_SUPPLIERS VALUES ('VSB', 'VIRGINIA STREET BAKERY');
COMMIT;

-- *************************************

CREATE TABLE L_CONSTANTS
(
    BUSINESS_NAME          VARCHAR(30),
    BUSINESS_START_DATE    DATE,
    LUNCH_BUDGET           DECIMAL(5,2),
    OWNER_NAME             VARCHAR(30)
) ENGINE=InnoDB;

INSERT INTO L_CONSTANTS VALUES
    ('CITYWIDE UNIFORMS', STR_TO_DATE('01-06-1998', '%d-%m-%Y'), 200, 'SUSAN BROWN');

COMMIT;

-- *************************************

-- Create Referential Integrity Constraints for the Lunches Database
ALTER TABLE L_EMPLOYEES
    ADD CONSTRAINT FK_L_EMPLOYEES_DEPT_CODE
    FOREIGN KEY (DEPT_CODE)
    REFERENCES L_DEPARTMENTS (DEPT_CODE);

ALTER TABLE L_EMPLOYEES
    ADD CONSTRAINT FK_L_EMPLOYEES_MANAGER_ID
    FOREIGN KEY (MANAGER_ID)
    REFERENCES L_EMPLOYEES (EMPLOYEE_ID);

ALTER TABLE L_LUNCHES
    ADD CONSTRAINT FK_L_LUNCHES_EMPLOYEES
    FOREIGN KEY (EMPLOYEE_ID)
    REFERENCES L_EMPLOYEES (EMPLOYEE_ID);

ALTER TABLE L_LUNCH_ITEMS
    ADD CONSTRAINT FK_L_LUNCH_ITEMS_LUNCHES
    FOREIGN KEY (LUNCH_ID)
    REFERENCES L_LUNCHES (LUNCH_ID);

ALTER TABLE L_LUNCH_ITEMS
    ADD CONSTRAINT FK_L_LUNCH_ITEMS_FOODS
    FOREIGN KEY (SUPPLIER_ID, PRODUCT_CODE)
    REFERENCES L_FOODS (SUPPLIER_ID, PRODUCT_CODE);

ALTER TABLE L_FOODS
ADD CONSTRAINT FK_L_FOODS_SUPPLIERS
    FOREIGN KEY (SUPPLIER_ID)
    REFERENCES L_SUPPLIERS (SUPPLIER_ID)
    ON DELETE CASCADE;

-- Create UNIQUENESS constraints
ALTER TABLE L_EMPLOYEES
ADD CONSTRAINT UNIQUE_L_EMPLOYEES_FULL_NAME
   UNIQUE (FIRST_NAME, LAST_NAME);

ALTER TABLE L_EMPLOYEES
ADD CONSTRAINT UNIQUE_L_EMPPLOYEES_PHONE_NUM
   UNIQUE (PHONE_NUMBER);

-- Create CHECK constraints
ALTER TABLE L_FOODS
    ADD CONSTRAINT CHECK_L_FOODS_PRICE_MAX_PRICE
    CHECK (PRICE < 10.00);