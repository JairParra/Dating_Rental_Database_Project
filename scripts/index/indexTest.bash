#!/bin/bash
echo "Without Index" > indexTest.log
echo "indexTest1_noIndex.sql" >> indexTest.log
echo "------------------------------------------" >>indexTest.log
cat indexTest1_noIndex.sql >>result_creation.txt
psql cs421< indexTest1_noIndex.sql  >>indexTest.log

echo "With Index" >> indexTest.log
echo "indexTest1_index.sql" >> indexTest.log
echo "------------------------------------------" >>indexTest.log
cat indexTest1_index.sql >> result_creation.txt
psql cs421< indexTest1_index.sql >> indexTest.log

echo "Without Index" >> indexTest.log
echo "indexTest2_noIndex.sql" >> indexTest.log
echo "------------------------------------------" >>indexTest.log
cat indexTest2_noIndex.sql >>result_creation.txt
psql cs421< indexTest2_noIndex.sql  >>indexTest.log

echo "With Index" >> indexTest.log
echo "indexTest2_index.sql" >> indexTest.log
echo "------------------------------------------" >>indexTest.log
cat indexTest2_index.sql >> result_creation.txt
psql cs421< indexTest2_index.sql >> indexTest.log

