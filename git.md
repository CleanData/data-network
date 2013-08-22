##git commands
List of github commands you might need for this project. These are the commands after you have pulled from the __cleandata__ repository online to your local branch.

####Switching between branches
This is when you want to checkout the __master__ branch
    
    git checkout master

###Merging a branch
To merge the __develop__ branch into the ___master___

    git merge develop    

###Finding log # for the commits made
Whenever you want to see the list of logs with the commit message and the commit number

    git log --oneline    

###Finding the difference between two commits
This is good when you want to upload code between two commits. You will need to refer to the __git log --oneline__ here.

    git archive --output=upload.zip HEAD $(git diff --name-only 75b2e27 fe0e041|sed -e "s/ /\\\/g")     

The above command will archive the files into an output in the same git directory with the name __upload.zip__ 
    