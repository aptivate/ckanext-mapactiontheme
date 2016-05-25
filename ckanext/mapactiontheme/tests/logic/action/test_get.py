import nose.tools

import ckan.tests.helpers as helpers

import ckan.plugins as plugins

assert_equals = nose.tools.assert_equals
assert_true = nose.tools.assert_true
assert_regexp_matches = nose.tools.assert_regexp_matches


class GetTestBase(helpers.FunctionalTestBase):
    @classmethod
    def setup_class(cls):
        super(GetTestBase, cls).setup_class()
        plugins.load('mapactiontheme')

    @classmethod
    def teardown_class(cls):
        plugins.unload('mapactiontheme')
        super(GetTestBase, cls).teardown_class()


class TestPackageShow(GetTestBase):
    def setup(self):
        super(TestPackageShow, self).setup()

        self.parent = helpers.call_action('package_create',
                                          name='ma001-01')

        self.v2 = helpers.call_action('package_create',
                                      name='ma001-01-02',
                                      extras=[{'key': 'versionnumber',
                                               'value': '02'}])

        self.v1 = helpers.call_action('package_create',
                                      name='ma001-01-01',
                                      extras=[{'key': 'versionnumber',
                                               'value': '01'}])

        self.v3 = helpers.call_action('package_create',
                                      name='ma001-01-03',
                                      extras=[{'key': 'versionnumber',
                                               'value': '03'}])

        helpers.call_action('package_relationship_create',
                            subject=self.v3['id'],
                            type='child_of',
                            object=self.parent['id'])

        helpers.call_action('package_relationship_create',
                            subject=self.v1['id'],
                            type='child_of',
                            object=self.parent['id'])

        helpers.call_action('package_relationship_create',
                            subject=self.v2['id'],
                            type='child_of',
                            object=self.parent['id'])

    def test_latest_version_displayed_when_showing_parent(self):
        dataset = helpers.call_action('package_show',
                                      id=self.parent['id'])

        assert_equals(dataset['name'], self.v3['name'])

    def test_child_version_displayed_when_showing_child(self):
        dataset = helpers.call_action('package_show',
                                      id=self.v2['id'])

        assert_equals(dataset['name'], self.v2['name'])

    def test_other_versions_displayed_when_showing_parent(self):
        dataset = helpers.call_action('package_show',
                                      id=self.parent['id'])

        assert_equals(dataset['versions'], [self.v3['name'],
                                            self.v2['name'],
                                            self.v1['name']])

    def test_other_versions_displayed_when_showing_child(self):
        dataset = helpers.call_action('package_show',
                                      id=self.v2['id'])

        assert_equals(dataset['versions'], [self.v3['name'],
                                            self.v2['name'],
                                            self.v1['name']])
