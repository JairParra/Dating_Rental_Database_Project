#!/bin/bash

echo "1_usertable_insertions.sql" >>result.txt

psql cs421< 1_usertable_insertions.sql  > projectsetup.log 1>>result.txt

echo "2_mate_insertions.sql" >>result.txt

psql cs421< 2_mate_insertions.sql  > projectsetup.log 1>>result.txt

echo "3_customer_insertions.sql" >>result.txt

psql cs421< 3_customer_insertions.sql  > projectsetup.log 1>>result.txt

echo "4_manager_insertions.sql" >>result.txt

psql cs421< 4_manager_insertions.sql  > projectsetup.log 1>>result.txt

echo "5_application_insertions.sql" >>result.txt

psql cs421< 5_application_insertions.sql  > projectsetup.log 1>>result.txt

echo "6_request_insertions.sql" >>result.txt

psql cs421< 6_request_insertions.sql  > projectsetup.log 1>>result.txt

echo "7_order_insertions.sql " >>result.txt

psql cs421< 7_order_insertions.sql  > projectsetup.log 1>>result.txt

echo "8_invoice_insertions.sql" >>result.txt

psql cs421< 8_invoice_insertions.sql  > projectsetup.log 1>>result.txt

echo "9_startTable_insertions.sql" >>result.txt

psql cs421< 9_startTable_insertions.sql  > projectsetup.log 1>>result.txt

echo "10_activity_insertions.sql" >>result.txt

psql cs421< 10_activity_insertions.sql  > projectsetup.log 1>>result.txt

echo "11_modify_insertions.sql" >>result.txt

psql cs421< 11_modify_insertions.sql > projectsetup.log 1>>result.txt

echo "12_generate_insertions.sql" >>result.txt

psql cs421< 12_generate_insertions.sql  > projectsetup.log 1>>result.txt

echo "13_schedule_insertions.sql" >>result.txt

psql cs421< 13_schedule_insertions.sql  > projectsetup.log 1>>result.txt