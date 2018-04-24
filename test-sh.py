import pexpect
child = pexpect.run('/usr/lib/ckan/bin/paster --plugin=ckan search-index check --config=/project/development.ini')
print child