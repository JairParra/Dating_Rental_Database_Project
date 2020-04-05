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

DELETE FROM usertable WHERE username='username1'; 

INSERT INTO usertable (username, password, email , firstname, lastname, sex, city , phoneNum, dateOfBirth) VALUES ('username1', 'Asderx890', 'username@mail.com', 'Name', 'Last', 'Female', 'Bogota', 4342890890, '1995-04-04') ;
SELECT * FROM usertable WHERE username='username1';

SELECT * FROM usertable; 


