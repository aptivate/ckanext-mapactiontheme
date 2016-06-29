from datetime import datetime

import pycountry

import pylons.config as config

from ckan.lib.helpers import get_pkg_dict_extra

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def group_name():
    '''Allows renaming of "Group"

    To change this setting add to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.group_name = MyGroupName

    Returns ``Group`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.group_name', 'Group')
    return value


def plural_group_name():
    '''Allows renaming of "Groups", the plural form.

    To change this setting add to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.plural_group_name = MyGroupNames

    Returns ``Group`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.plural_group_name', group_name() + 's')
    return value


def show_follows():
    '''Shows the follows section that would allow users to follow datasets

    To enable hiding this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_follows = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_follows', True)
    value = toolkit.asbool(value)
    return value


def show_license():
    '''Shows the license section

    To enable hiding this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_license = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_license', True)
    value = toolkit.asbool(value)
    return value


def show_organization():
    '''Show or hide the entire concept of organizations (this affects several templates)

    To hide organizations add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_organization = False

    Returns ``True`` by default, if the setting is not in the config file.

    Templates this setting affects:
    * package/read_base.html
    * package/base.html


    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_organization', True)
    value = toolkit.asbool(value)
    return value


def show_social():
    '''Shows the social links section

    To hide this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_social = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_social', True)
    value = toolkit.asbool(value)
    return value


def show_groups_tab():
    '''Shows the groups tab in places like the package_read template.

    To hide this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_groups_tab = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_groups_tab', True)
    value = toolkit.asbool(value)
    return value


def show_activity_tab():
    '''Shows the Activity Stream tab in places like the package_read template.

    To hide this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_activity_tab = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_activity_tab', True)
    value = toolkit.asbool(value)
    return value


def ckan_home_page_name():
    '''Get the name of the CKAN home page

    To set add this under the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.ckan_home_page_name = Maps and Data

    :rtype: string
    '''
    value = config.get('ckan.mapactiontheme.ckan_home_page_name', 'Home')
    return value


def home_page_link():
    '''Get the link for the home page if ckan is deployed as part of a site.

    To set add this under the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.home_page_link = http://mapaction.org

    :rtype: string
    '''
    value = config.get('ckan.mapactiontheme.home_page_link')
    return value


def unauthorized(context, data_dict=None):
    return {'success': False, 'msg': 'Organizations are not available.'}


def authorized(context, data_dict=None):
    return {'success': True}


def update_dataset_for_syndication(context, data_dict):
    dataset_dict = data_dict['dataset_dict']

    created = get_pkg_dict_extra(dataset_dict, 'createdate')

    if created is not None:
        created_date = datetime.strptime(created,
                                         '%Y-%m-%d %H:%M:%S')

        dataset_dict['dataset_date'] = created_date.strftime('%m/%d/%y')

    dataset_dict['methodology'] = 'Other'
    methodology = get_pkg_dict_extra(dataset_dict, 'methodology')
    if methodology is None:
        dataset_dict['methodology_other'] = 'Not specified'
    else:
        dataset_dict['methodology_other'] = methodology

    dataset_dict['dataset_source'] = get_pkg_dict_extra(
        dataset_dict, 'datasource')

    countries = get_pkg_dict_extra(dataset_dict, 'countries')

    dataset_dict['groups'] = []
    if countries is not None:
        for country_name in countries.split(','):
            cleaned_name = country_name.strip().title()
            country = None

            try:
                country = pycountry.countries.get(
                    name=cleaned_name)
            except KeyError:
                try:
                    country = pycountry.countries.get(
                        common_name=cleaned_name)
                except KeyError:
                    pass

            if country is not None:
                dataset_dict['groups'].append(
                    {'id': country.alpha3.lower()})

    dataset_dict['data_update_frequency'] = '0'

    return dataset_dict


class MapactionthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IFacets, inherit=True)

    # IActions
    def get_actions(self):
        return {
            'update_dataset_for_syndication':
            update_dataset_for_syndication,
        }

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        facets_dict.pop('organization', False)
        facets_dict.pop('tags', False)

        return facets_dict

    # IFacets
    def organization_facets(self, facets_dict, group_type, package_type):
        facets_dict.pop('organization', False)
        facets_dict.pop('tags', False)

        return facets_dict

    # IRoutes
    def before_map(self, map):
        map.connect(
            '/dataset/groups/{id}',
            controller='ckanext.mapactiontheme.controllers.package:MapactionPackageController',
            action='groups')

        return map

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactiontheme')

    #IAuthFunctions
    def get_auth_functions(self):

        permissions = {}
        if not show_organization():
            permissions = {
                'group_create': unauthorized,
                'member_create': authorized,
                'authorized': unauthorized,
                'organization_list': unauthorized,
                'organization_create': unauthorized,
                'organization_member_create': unauthorized,
                'organization_update': unauthorized,
                'organization_delete': unauthorized
            }

        return permissions

    #ITemplateHelpers
    def get_helpers(self):
        return {
            'group_name': group_name,
            'plural_group_name': plural_group_name,
            'show_follows': show_follows,
            'show_social': show_social,
            'show_organization': show_organization,
            'show_license': show_license,
            'show_groups_tab': show_groups_tab,
            'show_activity_tab': show_activity_tab,
            'ckan_home_page_name': ckan_home_page_name,
            'home_page_link': home_page_link
        }
