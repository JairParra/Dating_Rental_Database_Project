# stored_procedures
- Postgresql stored_procedures scripts

## <calcel_orders> 
- Description: 
Due to Covid-19 crisis, our company has decided to cancel all dates which starts after March 15th. All orders with startdate after '2020-03-15' will automaticly be cancelled (ordStatus becomes 'complete'). For customers who have already paid their orders but not had the date yet, they will receive a full amount refund. Which means that a new invoice will be automativally generated with the amount be the negative of paid amount. 

For the result of this query, please see doc Q1_procedure_result.txt
