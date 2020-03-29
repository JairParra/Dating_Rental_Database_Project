#!/bin/bash
echo "insteresting_queries.sql" >resultRetrieve.txt
cat insteresting_queries.sql >>resultRetrieve.txt
psql cs421< insteresting_queries.sql  > projectsetup.log 1>>resultRetrieve.txt

echo "------------------------------------" >>resultRetrieve.txt
echo "update_queries.sql" >>resultRetrieve.txt
cat update_queries.sql >>resultRetrieve.txt
psql cs421< update_queries.sql  > projectsetup.log 1>>resultRetrieve.txt
echo "------------------------------------" >>resultRetrieve.txt
echo "View1.sql" >>resultRetrieve.txt
cat view1.sql >>resultRetrieve.txt
psql cs421< view1.sql  > projectsetup.log 1>>resultRetrieve.txt

echo "------------------------------------" >>resultRetrieve.txt
echo "View2.sql" >>resultRetrieve.txt
cat view2.sql >>resultRetrieve.txt
psql cs421< view2.sql  > projectsetup.log 1>>resultRetrieve.txt

