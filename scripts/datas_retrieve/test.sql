SELECT 
    custname, 
    matename,
    mngname
FROM timeRequest temp
INNER JOIN request r
    ON temp.rid = r.rid 
JOIN modification mod 
    ON mod.oid = temp.oid 
; 