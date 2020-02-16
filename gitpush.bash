#!/bin/bash 

{
    # read commit message from user 
    read -p "Commit message: "  desc; 
    echo "$desc";  
}
git pull origin master && \  # fetch remote changes 
git add . && \  # update all changes 
git add -u && \ # remove files that have been deleted 
git commit -m "$desc" && \  # message 
git push -u origin master  # push 



