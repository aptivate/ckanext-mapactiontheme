from ckan.plugins import toolkit

import ckan.logic as logic
from ckan.logic.action.get import package_show as ckan_package_show


def package_show(context, data_dict):
    parent = ckan_package_show(context, data_dict)

    children = []

    try:
        children = toolkit.get_action('package_relationships_list')(
            context,
            data_dict={'id': parent['id'],
                       'rel': 'parent_of'})
    except logic.NotFound:
        pass

    latest_version = parent
    highest_version_number = 0

    for child in children:
        data_dict['id'] = child['object']
        version = ckan_package_show(context, data_dict)
        extras_dict = {e['key']: e['value'] for e in version['extras']}
        if extras_dict['versionnumber'] > highest_version_number:
            latest_version = version
            highest_version_number = extras_dict['versionnumber']

    return latest_version
