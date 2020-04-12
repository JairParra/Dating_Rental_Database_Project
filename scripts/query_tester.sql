-- Obtain the record for a specific user  
SELECT * FROM usertable WHERE username IN ('bmccartand','gfilinkov1d') OR email='jspurling0@cnet.com'; 

SELECT * FROM usertable; 

SELECT * FROM manager; 
SELECT * FROM customer; 
SELECT * FROM mate; 


SELECT 
 * 
FROM usertable 
WHERE username IN 
    (
        SELECT username
        FROM customer
        WHERE username = 'bmccartand'
    )
; 


SELECT * FROM 
    (   
    SELECT 
        m.nickname,
        u.sex, 
        DATE_PART('year', CURRENT_DATE) - DATE_PART('year', u.dateofbirth) as age, 
        m.language, 
        m.height, 
        m.weight,  
        m.hourlyrate, 
        m.description 
    FROM mate m
    JOIN usertable u 
        ON m.username = u.username 
    WHERE sex='Male' AND (height BETWEEN 1.50 AND 1.75)
    ORDER BY age
    ) T 
WHERE (T.age BETWEEN 20 AND 25)
; 

DELETE FROM usertable WHERE username='newusername'; 

INSERT INTO usertable (username, password, email , firstname, lastname, sex, city , phoneNum, dateOfBirth) VALUES ('username1', 'Asderx890', 'username@mail.com', 'Name', 'Last', 'Female', 'Bogota', 4342890890, '1995-04-04') ;
SELECT * FROM usertable WHERE username='username1';

SELECT * FROM usertable WHERE username='newusername'; 

INSERT INTO customer (username, preferences) VALUES ('newusername','preference12321') ; 
DELETE FROM customer WHERE username='newusername'; 


SELECT * FROM customer; 



SELECT * 
FROM usertable u
JOIN manager m
    ON u.username = m.username 
; 


INSERT INTO invoice( oid, description,duedate, amount, custName, method, status) VALUES(1, '123', '2020-1-10', 1, 'agiven2o', 'bank', 'complete');


SELECT * FROM mate; 



--------------------------------------------------------------------------------

SELECT VERSION(); 


CREATE OR REPLACE PROCEDURE CancelOrders()

    LANGUAGE PLPGSQL
    AS $$
        DECLARE 
        ordStatus VARCHAR(20) := 'complete';
        oid INTEGER;
        amount DECIMAL(100,2);
        description VARCHAR(100) :='Automatic refund';
        duedate DATE := '2020-03-20';
        custName VARCHAR(50);
        method VARCHAR(20) ;
        status VARCHAR(20) := 'paid';
        order_row RECORD;
        invoice_row RECORD;

        OrderCursor CURSOR(p INTEGER   )
            FOR SELECT * FROM orderTable WHERE startDate > '2019-12-08';
        BEGIN

        OPEN OrderCursor(1);
        
        LOOP
                -- PRINT 'Processing OrderID:' +Cast(@oid as VARCHAR);

                FETCH OrderCursor INTO order_row;
                EXIT WHEN NOT FOUND;
                    
                UPDATE orderTable
                SET ordStatus = 'complete'
                WHERE CURRENT OF OrderCursor;

                SELECT INTO invoice_row * FROM invoice WHERE invoice.oid = order_row.oid ;
                IF invoice_row.status = 'paid' THEN
                    INSERT INTO invoice(oid, description,duedate, amount, custName, method, status) 
                    VALUES (order_row.oid, description, duedate, invoice_row.amount, invoice_row.custName, invoice_row.method, status);
                
                END IF;
                
        END LOOP;
        CLOSE OrderCursor;
        END
    $$
    ;

    CALL CancelOrders();

