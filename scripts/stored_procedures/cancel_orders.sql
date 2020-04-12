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
                    VALUES (order_row.oid, description, duedate, -1 * invoice_row.amount, invoice_row.custName, invoice_row.method, status);
                
                END IF;
                
        END LOOP;
        CLOSE OrderCursor;
        END
    $$
    ;


    CALL CancelOrders();
            


