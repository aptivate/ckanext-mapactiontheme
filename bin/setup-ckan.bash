#!/bin/bash
set -e

echo "This is setup-ckan.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install xmlsec1 libxmlsec1-dev

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/ckan/ckan
cd ckan
if [ $CKANVERSION == 'master' ]
then
    echo "CKAN version: master"
else
    CKAN_TAG=$(git tag | grep ^ckan-$CKANVERSION | sort --version-sort | tail -n 1)
    git checkout $CKAN_TAG
    echo "CKAN version: ${CKAN_TAG#ckan-}"
fi

# install the recommended version of setuptools
if [ -f requirement-setuptools.txt ]
then
    echo "Updating setuptools..."
    pip install -r requirement-setuptools.txt
fi

if [ $CKANVERSION == '2.7' ]
then
    echo "Installing setuptools"
    pip install setuptools==39.0.1
fi

python setup.py develop
pip install -r requirements.txt
pip install -r dev-requirements.txt
cd -

echo "Creating the PostgreSQL user and database..."
psql -h localhost -U postgres -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
psql -h localhost -U postgres -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'

echo "Initialising the database..."
cd ckan
paster db init -c test-core.ini
cd -

echo "Installing ckanext-mapactiontheme dependencies..."
echo "Installing ckanext-scheming"
pip install -e git+https://github.com/ckan/ckanext-scheming.git@release-1.2.0#egg=ckanext-scheming

echo "Installing ckanext-locationgroup"
pip install -e git+https://github.com/aptivate/ckanext-locationgroup.git@staging#egg=ckanext-locationgroup

echo "Installing ckanext-mapactionevent"
pip install -e git+https://github.com/aptivate/ckanext-mapactionevent.git@staging#egg=ckanext-mapactionevent

echo "Installing ckanext-syndicate"
pip install -e git+https://github.com/aptivate/ckanext-syndicate.git@v1.1.0#egg=ckanext-syndicate

echo "Installing ckanext-mapactionschemas"
pip install -e git+https://github.com/mapaction/ckanext-mapactionschemas.git@staging#egg=ckanext-mapactionschemas

echo "Installing ckanext-mapactiontheme and its requirements..."
python setup.py develop
pip install -r dev-requirements.txt

echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir

echo "setup-ckan.bash is done."