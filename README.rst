.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://github.com/aptivate/ckanext-mapactiontheme/workflows/CI/badge.svg
    :target: https://github.com/aptivate/ckanext-mapactiontheme/actions

.. image:: https://coveralls.io/repos/github/aptivate/ckanext-mapactiontheme/badge.svg
    :target: https://coveralls.io/github/aptivate/ckanext-mapactiontheme

=============
ckanext-mapactiontheme
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


------------
Requirements
------------

For example, you might want to mention here which versions of CKAN this
extension works with.


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-mapactiontheme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-mapactiontheme Python package into your virtual environment::

     pip install ckanext-mapactiontheme

3. Add ``mapactiontheme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

::

    # Allow renaming of 'Group'
    # (optional, default: Group)
    ckan.mapactiontheme.group_name = MyGroupName

    # Allow renaming of 'Group' in plural form
    # (optional, default: the above suffixed with 's')
    ckan.mapactiontheme.plural_group_name = MyGroupNames

    # Show the section to follow datasets
    # (optional, default: True)
    ckan.mapactiontheme.show_follows = False

    # Show the license section
    # (optional, default: True)
    ckan.mapactiontheme.show_license = False

    # Show the entire concept of organizations
    # (optional, default: True)
    ckan.mapactiontheme.show_organization = False

    # Show the social links section
    # (optional, default: True)
    ckan.mapactiontheme.show_social = False

    # Show the groups tab eg in package_read template
    # (optional, default: True)
    ckan.mapactiontheme.show_groups_tab = False

    # Show the activity tab eg in package_read template
    # (optional, default: True)
    ckan.mapactiontheme.show_activity_tab = False

    # The name of the CKAN home page
    # (optional, default: Home)
    ckan.mapactiontheme.ckan_home_page_name = Maps and Data

    # The link for the home page if CKAN is deployed as part of another site
    # (mandatory)
    ckan.mapactiontheme.home_page_link = http://mapaction.org

    # The navigation menu ID of the CKAN site
    # (mandatory)
    ckan.mapactiontheme.nav_menu_this_id = 12

    # Connect timeout when retrieving content from WordPress API
    # (optional, default: 3.05)
    ckan.mapactiontheme.api_connect_timeout = 1

    # Read timeout when retrieving content from WordPress API
    # (optional, default: 3)
    ckan.mapactiontheme.read_timeout = 27

    # URL for current emergencies content
    # (mandatory)
    ckan.mapactiontheme.current_emergencies_api = http://www.example.com/api/

    # URL for navigation menu content
    # (mandatory)
    ckan.mapactiontheme.nav_menu_api = http://www.example.com/api/

    # URL for footer widget content
    # (mandatory)
    ckan.mapactiontheme.footer_widget_api = http://www.example.com/api/

------------------------
Development Installation
------------------------

To install ckanext-mapactiontheme for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/aptivate/ckanext-mapactiontheme.git
    cd ckanext-mapactiontheme
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.mapactiontheme --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-mapactiontheme on PyPI
---------------------------------

ckanext-mapactiontheme should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-mapactiontheme. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-mapactiontheme
----------------------------------------

ckanext-mapactiontheme is availabe on PyPI as https://pypi.python.org/pypi/ckanext-mapactiontheme.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags

-----
About
-----
Copyright (c) 2016 `MapAction <http://mapaction.org>`_. Developed by `Aptivate <http://aptivate.org>`_.

Development of v1 of this plugin was funded by `ECHO <http://ec.europa.eu/echo>`_.

.. image:: http://www.echo-visibility.eu/wp-content/uploads/2014/02/EU_Flag_HA_2016_EN-300x272.png
   :alt: "Funded by European Union Humanitarian Aid"
