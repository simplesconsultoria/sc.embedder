# -*- coding: utf-8 -*-
"""Module with the apapters tests."""

from plone import api
from sc.embedder.testing import INTEGRATION_TESTING
from sc.embedder.testing import IS_PLONE_5

import unittest


class AdaptersTestCase(unittest.TestCase):
    """Adapters test class."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Tests configuration."""
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.multimedia = api.content.create(
                self.portal,
                'sc.embedder',
                title='Multimedia',
                description='New Multimedia',
                embed_html='<iframe width="480" height="270" '
                'src="https://www.teste.com/embed/tesste?feature=oembed" '
                'allowfullscreen></iframe>',
                width=300,
                height=200,
            )

    @unittest.skipIf(IS_PLONE_5, 'Plone 5 has no Products.TinyMCE.')
    def test_json_details(self):
        """Test if JSONDetails adapter returns all keys."""
        from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
        adapter = IJSONDetails(self.multimedia, None)
        uid = self.multimedia.UID()
        expected = '{{"thumb_html": "%3Ciframe%20width%3D%22188%22%20height'\
            '%3D%22141%22%20src%3D%22https%3A//www.teste.com/embed/tesste%3F'\
            'feature%3Doembed%22%20allowfullscreen%3E%3C/iframe%3E",'\
            ' "uid_relative_url": "resolveuid/{0}", "thumb": "", "uid_url": '\
            '"http://nohost/plone/resolveuid/{0}", "url": '\
            '"http://nohost/plone/multimedia", "description": '\
            '"New Multimedia", "title": "Multimedia", "embed_html": '\
            '"%3Ciframe%20width%3D%22480%22%20height'\
            '%3D%22270%22%20src%3D%22https%3A//www.teste.com/embed/'\
            'tesste%3Ffeature%3Doembed%22%20allowfullscreen%3E%3C/'\
            'iframe%3E", "anchors": []}}'.format(uid)
        result = adapter.getDetails()
        self.assertEqual(expected, result)
