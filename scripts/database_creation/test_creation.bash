#!/bin/bash
echo "table_creation.sql" >result_creation.txt
echo "------------------------------------------" >>result_creation.txt
cat table_creation.sql >>result_creation.txt
psql cs421< table_creation.sql  > projectsetup.log 1>>result_creation.txt
