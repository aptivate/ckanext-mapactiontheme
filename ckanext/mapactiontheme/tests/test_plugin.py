import nose.tools
import unittest

from ckan.common import _
import ckan.tests.helpers as helpers
import ckan.plugins as plugins

from ckanext.mapactiontheme.plugin import MapactionthemePlugin
import ckanext.mapactiontheme.tests.helpers as custom_helpers
import ckanext.mapactiontheme.tests.factories as custom_factories

assert_equal = nose.tools.assert_equal
assert_false = nose.tools.assert_false
assert_raises = nose.tools.assert_raises
assert_regexp_matches = nose.tools.assert_regexp_matches
assert_true = nose.tools.assert_true


class DatasetFacetsTest(unittest.TestCase):
    def setUp(self):
        super(DatasetFacetsTest, self).setUp()
        self.default_facet_titles = {
            'organization': _('Organizations'),
            'groups': _('Groups'),
            'tags': _('Tags'),
            'res_format': _('Formats'),
            'license_id': _('Licenses'),
        }

    def test_removes_organization(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.dataset_facets(self.default_facet_titles,
                                            'dataset')

        self.assertTrue('organization' not in facets_dict)

    def test_removes_tags(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.dataset_facets(self.default_facet_titles,
                                            'dataset')

        self.assertTrue('tags' not in facets_dict)

    def test_facet_dict_is_left_empty(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.dataset_facets({},
                                            'dataset')

        self.assertEquals(facets_dict, {})


class OrganizationFacetsTest(unittest.TestCase):
    def setUp(self):
        super(OrganizationFacetsTest, self).setUp()
        self.default_facet_titles = {'organization': _('Organizations'),
                                     'groups': _('Groups'),
                                     'tags': _('Tags'),
                                     'res_format': _('Formats'),
                                     'license_id': _('Licenses')}

    def test_removes_organization(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.organization_facets(self.default_facet_titles,
                                                 'organization',
                                                 'dataset')

        self.assertTrue('organization' not in facets_dict)

    def test_removes_tags(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.organization_facets(self.default_facet_titles,
                                                 'organization',
                                                 'dataset')

        self.assertTrue('tags' not in facets_dict)

    def test_facet_dict_is_left_empty(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.organization_facets({},
                                                 'organization',
                                                 'dataset')

        self.assertEquals(facets_dict, {})


class TestUpdateForSyndication(custom_helpers.FunctionalTestBaseClass):
    def test_schema_createdate_transformed_to_hdx_date(self):
        metadata = {
            'createdate': '2016-02-08T12:18:24+01:30',
            'datasource': 'Test',  # Required value
        }

        dataset_dict = custom_factories.Dataset(**metadata)

        updated_dict = helpers.call_action(
            'update_dataset_for_syndication',
            dataset_dict=dataset_dict
        )

        assert_equal(updated_dict['dataset_date'], '08/02/2016')

    def test_dataset_source_is_datasource(self):
        datasource = (
            'Situational data: N/ABoundaries: GADMSettlements: '
            'GeofabrikPhysical features: GeofabrikWaterways: '
            'Geofabrik<ITA>add data sources here (concise list)</ITA>'
        )

        metadata = {
            'createdate': '2016-02-08T12:18:24+01:30',  # required field
            'datasource': datasource,
        }

        dataset_dict = custom_factories.Dataset(**metadata)
        updated_dict = helpers.call_action(
            'update_dataset_for_syndication',
            dataset_dict=dataset_dict
        )

        assert_equal(updated_dict['dataset_source'], datasource)

    def test_groups_set_from_countries(self):
        countries = (
            'ETHIOPIA, Uganda, Kenya, Tanzania, Malawi, Mozambique, Zambia, '
            'Zaire, Zimbabwe, Somalia, Sudan, Yemen, Djibouti, Eritrea, '
            'A made up country'
        )

        metadata = {
            'createdate': '2016-02-08T12:18:24+01:30',
            'datasource': 'Test',  # Required value
            'countries': countries,
        }

        dataset_dict = custom_factories.Dataset(**metadata)

        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict=dataset_dict)

        assert_equal(
            updated_dict['groups'],
            [
                {'id': 'eth'},
                {'id': 'uga'},
                {'id': 'ken'},
                {'id': 'tza'},
                {'id': 'mwi'},
                {'id': 'moz'},
                {'id': 'zmb'},
                {'id': 'zwe'},
                {'id': 'som'},
                {'id': 'sdn'},
                {'id': 'yem'},
                {'id': 'dji'},
                {'id': 'eri'},
            ]
        )

    def test_groups_default_to_world_for_no_valid_countries(self):
        countries = 'Zaire, A made up country'

        metadata = {
            'countries': countries,
        }

        metadata = {
            'createdate': '2016-02-08T12:18:24+01:30',
            'datasource': 'Test',  # Required value
            'countries': countries,
        }

        dataset_dict = custom_factories.Dataset(**metadata)

        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict=dataset_dict)

        assert_equal(
            updated_dict['groups'],
            [
                {'id': 'world'},
            ]
        )

    def test_methodology_set_to_other(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={})

        assert_equal(updated_dict['methodology'], 'Other')

    def test_methodology_other_set_to_methodology(self):
        methodology = (
            "The 'visited' coordinates come from the international Urban "
            "Search and Rescue (USAR) team reports as provided to the Virtual "
            "OSOCC and to the USAR coordination centre and are from GPS. "
            "The 'to visit' sites come from the government of Nepal as a list "
            "of names to which we have attempted to assign coordinates."
        )

        metadata = {
            'createdate': '2016-02-08T12:18:24+01:30',  # Reqired field
            'datasource': 'Test',  # Required field
            'methodology': methodology,
        }

        dataset_dict = custom_factories.Dataset(**metadata)

        updated_dict = helpers.call_action(
            'update_dataset_for_syndication',
            dataset_dict=dataset_dict
        )

        assert_equal(
            updated_dict['methodology_other'],
            methodology
        )

    def test_method_other_set_to_placeholder_if_no_values(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={})

        assert_equal(
            updated_dict['methodology_other'],
            'Not specified')

    def test_update_frequency_set_to_never(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={})

        assert_equal(
            updated_dict['data_update_frequency'],
            'Never')

    def test_update_frequency_set_to_valid_value(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={
                                               'extras': [
                                                {'key': 'data_update_frequency',
                                                 'value': 'Every week'}]})

        assert_equal(
            updated_dict['data_update_frequency'],
            'Every week')

    def test_update_frequency_set_to_invalid_value(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={
                                               'extras': [
                                                {'key': 'data_update_frequency',
                                                 'value': 'Every seven weeks'}]
                                           })

        assert_equal(
            updated_dict['data_update_frequency'],
            'Never')

    def test_update_frequency_no_extras(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={})
        assert_equal(
            updated_dict['data_update_frequency'],
            'Never')

    def test_tags_removed(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={'tags': []})

        assert_true('tags' not in updated_dict)

    def test_extras_removed(self):
        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict={'extras': []})

        assert_true('extras' not in updated_dict)

    def test_other_fields_removed(self):
        metadata = {
            'createdate': '2016-02-08T12:18:24+01:30',  # Reqired field
            'datasource': 'Test',  # Required field
            'glideno': 'glideno',
        }

        dataset_dict = custom_factories.Dataset(**metadata)
        updated_dict = helpers.call_action(
            'update_dataset_for_syndication',
            dataset_dict=dataset_dict
        )

        assert_true('glideno' not in updated_dict)
