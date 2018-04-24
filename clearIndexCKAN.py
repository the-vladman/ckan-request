import pexpect

file = open("idFiles.txt", "r") 
for line in file: 
    child = pexpect.run('/usr/lib/ckan/bin/paster --plugin=ckan search-index clear ' + line + ' --config=/project/development.ini')