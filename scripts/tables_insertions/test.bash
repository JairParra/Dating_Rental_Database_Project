#!/bin/bash

echo "1_usertable_insertions.sql" > resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 1_usertable_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 1_usertable_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "2_mate_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 2_mate_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
psql cs421< 2_mate_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "3_customer_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 3_customer_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 3_customer_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "4_manager_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 4_manager_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 4_manager_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "5_application_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 5_application_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 5_application_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "6_request_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 6_request_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 6_request_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "7_order_insertions.sql " >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 7_order_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 7_order_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "8_invoice_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 8_invoice_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 8_invoice_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "9_startTable_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 9_startTable_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 9_startTable_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "10_activity_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 10_activity_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 10_activity_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "11_modify_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 11_modify_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 11_modify_insertions.sql > projectsetup.log 1>>resultInsertion.txt

echo "12_generate_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 12_generate_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 12_generate_insertions.sql  > projectsetup.log 1>>resultInsertion.txt

echo "13_schedule_insertions.sql" >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt
head 13_schedule_insertions.sql -n 5 >>resultInsertion.txt
echo "----------------------------------------------------------" >> resultInsertion.txt

psql cs421< 13_schedule_insertions.sql  > projectsetup.log 1>>resultInsertion.txt
