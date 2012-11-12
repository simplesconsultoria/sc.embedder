# -*- coding: utf-8 -*-
try:
    import json
    assert json  # silence pyflakes
except ImportError:
    import simplejson as json

import unittest2 as unittest

from zope.interface.verify import verifyClass, verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from sc.embedder.content.embedder import IEmbedder
from sc.embedder.content.embedder import Embedder
from sc.embedder.testing import INTEGRATION_TESTING

PROVIDERS = {
     'youtube': 'http://www.youtube.com/watch?v=n-zxaVt6acg&feature=g-all-u',
     'vimeo': 'http://vimeo.com/17914974',
     'slideshare': 'http://www.slideshare.net/cgiorgi/secrets-of-a-good-pitch',
     'instagram': 'http://www.flickr.com/photos/jup3nep/6796214503/?f=hp',
     }


class MultimediaTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('sc.embedder', 'multimedia')
        self.multimedia = self.folder['multimedia']
        self.multimedia.title = 'Multimedia'
        self.multimedia.reindexObject()

    def test_adding(self):
        self.assertTrue(IEmbedder.providedBy(self.multimedia))
        self.assertTrue(verifyClass(IEmbedder, Embedder))

    def test_interface(self):
        self.assertTrue(IEmbedder.providedBy(self.multimedia))
        self.assertTrue(verifyObject(IEmbedder, self.multimedia))

    def test_custom_player_size_addform(self):
        """ Check if the custom size applies to the embed code in the
            add form.
        """
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder')
        dummy_data = {}
        dummy_data['embed_html'] = '<object width="512" height="296"><param ' + \
                        'name="flashvars" value="ap=1"></param></object>'
        dummy_data['width'] = 300
        dummy_data['height'] = 200
        add_form = add_view.form_instance
        add_form.set_custom_embed_code(dummy_data)
        self.assertTrue('width="300"' in dummy_data['embed_html'])
        self.assertTrue('height="200"' in dummy_data['embed_html'])

    def test_custom_player_size_editform(self):
        """ Check if the custom size applies to the embed code in the
            edit form.
        """
        edit_view = self.multimedia.unrestrictedTraverse('edit')
        edit_form = edit_view.form_instance
        dummy_data = {}
        dummy_data['embed_html'] = '<object width="512" height="296"><param ' + \
                        'name="flashvars" value="ap=1"></param></object>'
        dummy_data['width'] = 300
        dummy_data['height'] = 200
        edit_form.set_custom_embed_code(dummy_data)
        self.assertTrue('width="300"' in dummy_data['embed_html'])
        self.assertTrue('height="200"' in dummy_data['embed_html'])

    def test_player_position_class(self):
        """ Tests the return of the css class based on the position
            selected in the form.
        """
        view = self.multimedia.unrestrictedTraverse('view')

        # Classes
        self.multimedia.player_position = u'Top'
        pos_class = view.get_player_pos_class()
        self.assertEqual(pos_class, 'top_embedded')

        self.multimedia.player_position = u'Bottom'
        pos_class = view.get_player_pos_class()
        self.assertEqual(pos_class, 'bottom_embedded')

        self.multimedia.player_position = u'Left'
        pos_class = view.get_player_pos_class()
        self.assertEqual(pos_class, 'left_embedded')

        self.multimedia.player_position = u'Right'
        pos_class = view.get_player_pos_class()
        self.assertEqual(pos_class, 'right_embedded')

    def test_get_url_widget(self):
        from z3c.form.browser.text import TextWidget
        edit_view = self.multimedia.unrestrictedTraverse('edit')
        edit_form = edit_view.form_instance
        edit_form.update()
        url_wid = edit_view.get_url_widget()
        self.assertTrue(TextWidget, url_wid)
        self.assertEqual(url_wid.id, 'form-widgets-url')

    def test_get_load_action(self):
        from z3c.form.button import ButtonAction
        edit_view = self.multimedia.unrestrictedTraverse('edit')
        edit_form = edit_view.form_instance
        edit_form.update()
        load_act = edit_view.get_load_action()
        self.assertTrue(ButtonAction, load_act)
        self.assertEqual(load_act.id, 'form-buttons-load')

    def test_vimeo_oembed(self):
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder')
        add_form = add_view.form_instance
        add_form.update()
        add_form.actions.update()

        add_form.widgets['url'].value = 'http://vimeo.com/17914974'
        action = add_form.actions['load']

        # We trigger the action of load
        add_form.handleLoad(add_form, action)
        iframe = '<iframe src="http://player.vimeo.com/video/17914974" ' + \
              'width="1280" height="720" frameborder="0" ' + \
              'webkitAllowFullScreen mozallowfullscreen ' + \
              'allowFullScreen></iframe>'

        self.assertEqual(u'The Backwater Gospel',
                        add_form.widgets['IDublinCore.title'].value)
        self.assertEqual(417,
                    len(add_form.widgets['IDublinCore.description'].value))
        self.assertEqual(iframe,
                        add_form.widgets['embed_html'].value)
        self.assertEqual(u'1280',
                        add_form.widgets['width'].value)
        self.assertEqual(u'720',
                        add_form.widgets['height'].value)

    def test_youtube_oembed(self):
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder')
        add_form = add_view.form_instance
        add_form.update()
        add_form.actions.update()

        url = 'http://www.youtube.com/watch?v=d8bEU80gIzQ'
        add_form.widgets['url'].value = url
        action = add_form.actions['load']

        # We trigger the action of load
        add_form.handleLoad(add_form, action)
        iframe = '<iframe width="459" height="344" src="http://www' + \
                '.youtube.com/embed/d8bEU80gIzQ?fs=1&feature=oembed" ' + \
                'frameborder="0" allowfullscreen></iframe>'
        self.assertEqual(u"Introducing Plone",
                        add_form.widgets['IDublinCore.title'].value)
        self.assertEqual(iframe,
                        add_form.widgets['embed_html'].value)
        self.assertEqual(u'459',
                        add_form.widgets['width'].value)
        self.assertEqual(u'344',
                        add_form.widgets['height'].value)

    def test_slideshare_oembed(self):
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder')
        add_form = add_view.form_instance
        add_form.update()
        add_form.actions.update()

        url = 'http://www.slideshare.net/baekholt/plone-4-and-' + \
              '5-plans-and-progress'

        add_form.widgets['url'].value = url
        action = add_form.actions['load']

        # We trigger the action of load
        add_form.handleLoad(add_form, action)

        iframe = '<iframe src="http://www.slideshare.net/slideshow/' + \
            'embed_code/1464608" width="427" height="356" frameborder=' + \
            '"0" marginwidth="0" marginheight="0" scrolling="no" ' + \
            'style="border:1px solid #CCC;border-width:1px 1px 0;' + \
            'margin-bottom:5px" allowfullscreen webkitallowfullscreen ' + \
            'mozallowfullscreen> </iframe> <div ' + \
            'style="margin-bottom:5px"> <strong> <a href="http://www.' + \
            'slideshare.net/baekholt/plone-4-and-5-plans-and-progress"' + \
            ' title="Plone 4 and 5, plans and progress" target="_blank">' + \
            'Plone 4 and 5, plans and progress</a> </strong> from ' + \
            '<strong><a href="http://www.slideshare.net/baekholt" ' + \
            'target="_blank">baekholt</a></strong> </div>'

        self.assertEqual(u'Plone 4 and 5, plans and progress',
                        add_form.widgets['IDublinCore.title'].value)
        self.assertEqual(iframe,
                        add_form.widgets['embed_html'].value)
        self.assertEqual(u'425',
                        add_form.widgets['width'].value)
        self.assertEqual(u'355',
                        add_form.widgets['height'].value)

    def test_soundcloud_oembed(self):
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder')
        add_form = add_view.form_instance
        add_form.update()
        add_form.actions.update()

        # We check for Vimeo that has a more complete oembed implementation
        url = 'http://soundcloud.com/nuvru/semi-plone'
        add_form.widgets['url'].value = url
        action = add_form.actions['load']

        # We trigger the action of load
        add_form.handleLoad(add_form, action)

        iframe = '<iframe width="100%" height="166" scrolling="no" ' + \
                'frameborder="no" src="http://w.soundcloud.com/' + \
                'player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks' + \
                '%2F4599497&show_artwork=true"></iframe>'

        self.assertEqual(u'Semi Plone by nuvru',
                        add_form.widgets['IDublinCore.title'].value)
        self.assertEqual(u'Well... semi.',
                        add_form.widgets['IDublinCore.description'].value)
        self.assertEqual(iframe,
                        add_form.widgets['embed_html'].value)

        # Sound cloud return percentage values
        self.assertEqual(u'100%',
                        add_form.widgets['width'].value)
        self.assertEqual(u'166',
                        add_form.widgets['height'].value)

    def test_videojs(self):
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder')
        add_form = add_view.form_instance
        add_form.update()
        add_form.actions.update()

        url = 'http://video-js.zencoder.com/oceans-clip.webm'
        add_form.widgets['url'].value = url
        action = add_form.actions['load']

        # We trigger the action of load
        add_form.handleLoad(add_form, action)
        iframe = u'\n<iframe src="http://nohost/plone/test-folder/@@embedder_videojs?\
src=http%3A%2F%2Fvideo-js.zencoder.com%2Foceans-clip.webm&\
type=video%2Fwebm"\n        class="vjs-iframe"\n        \
allowfullscreen="1" mozallowfullscreen="1" webkitallowfullscreen="1"\n        \
frameborder="0">\n</iframe>\n'
        self.assertEqual(u"",
                        add_form.widgets['IDublinCore.title'].value)
        self.assertEqual(iframe,
                        add_form.widgets['embed_html'].value)
        self.assertEqual(u'',
                        add_form.widgets['width'].value)
        self.assertEqual(u'',
                        add_form.widgets['height'].value)

        self.folder.invokeFactory('sc.embedder', 'ocean-clip')
        video = self.folder['ocean-clip']

        video.title = 'Oceans clip'
        video.width = '640'
        video.height = '264'
        video.embed_html = iframe

        self.assertItemsEqual({u'thumb_html': u'<iframe src="http://nohost/plone/test-folder/@@embedder_videojs?src=http%3A%2F%2Fvideo-js.zencoder.com%2Foceans-clip.webm&amp;type=video%2Fwebm" class="vjs-iframe" allowfullscreen="1" mozallowfullscreen="1" webkitallowfullscreen="1" frameborder="0" width="188" height="141">\n</iframe>',
                               u'embed_html': u'\n<iframe src="http://nohost/plone/test-folder/@@embedder_videojs?src=http%3A%2F%2Fvideo-js.zencoder.com%2Foceans-clip.webm&type=video%2Fwebm"\n        class="vjs-iframe"\n        allowfullscreen="1" mozallowfullscreen="1" webkitallowfullscreen="1"\n        frameborder="0">\n</iframe>\n',
                               u'description': u'',
                               u'title': u'Oceans clip'
                               },
                              json.loads(video.unrestrictedTraverse('@@tinymce-jsondetails')()))

    def test_jsonimagefolderlisting(self):
        # Now we can get a listing of the images and check if our image is there.e/'})
        output = self.folder.restrictedTraverse('@@tinymce-jsonscembedderfolderlisting')(False, 'http://nohost/plone/test-folder')
        self.assertIn('"id": "multimedia"', output)

    def test_jsonimagesearch(self):
        # The images have a similar search method. Let's find our image.
        output = self.portal.restrictedTraverse('@@tinymce-jsonscembeddersearch')('Multimedia')
        self.assertIn('"id": "multimedia"', output)
