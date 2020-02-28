--

CREATE VIEW timeRequest (oid,rid) AS
SELECT oid,rid FROM orderTable WHERE ((DATE_PART('year', '2018-02-02'::date) - DATE_PART('year',enddate::date)) * 12 + (DATE_PART('month', '2018-02-02'::date) - DATE_PART('month', enddate::date))) <= 100
;

SELECT custname,matename,mngname FROM timeRequest as temp, request,modification WHERE temp.rid=request.rid AND temp.oid=modification.oid