--
CREATE VIEW timeRequest(custName, mateName) AS
SELECT rid FROM orderTable WHERE DATEDIFF(day, '2018/03/05', endDate) <= 100
;
SELECT custName, mateName FROM timeRequest as temp, request WHERE temp.rid=request.rid