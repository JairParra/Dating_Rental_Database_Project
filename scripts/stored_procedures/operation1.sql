    CREATE OR REPLACE FUNCTION CancelOrders() RETURNs void
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
            FOR SELECT * FROM orderTable WHERE startDate > '2020-03-20';
        BEGIN

        OPEN OrderCursor(1);
        
        LOOP
                -- PRINT 'Processing OrderID:' +Cast(@oid as VARCHAR);

                FETCH OrderCursor INTO order_row;
                EXIT WHEN NOT FOUND;
                    
                UPDATE orderTable
                SET ordStatus = 'complete'
                WHERE CURRENT OF OrderCursor;

                SELECT INTO invoice_row * FROM invoice WHERE oid = order_row.oid ;
                IF invoice_row.status = 'paid' THEN
                -- DECLARE InvoiceCursor CURSOR(h INTEGER) FOR SELECT * FROM invoice WHERE oid = order_row.oid AND status = 'paid';

                -- OPEN InvoiceCursor(1);
                -- LOOP 

                --     FETCH InvoiceCursor INTO invoice_row;
                --     EXIT WHEN NOT FOUND;
                    INSERT INTO invoice(oid, description,duedate, amount, custName, method, status) 
                    VALUES (order_row.oid, description, duedate, invoice_row.amount, invoice_row.custName, invoice_row.method, status);
                
                END IF;
                
        END LOOP;
        CLOSE OrderCursor;
        END
    $$
    ;


            


