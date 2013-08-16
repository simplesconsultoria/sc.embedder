There's a frood who really knows where his towel is
---------------------------------------------------

1.0b4 (unreleased)
^^^^^^^^^^^^^^^^^^

- Fix WCGA and W3C validation issues (iframes) (closes `#8`_).
  [rodfersou]


1.0b3 (2013-07-23)
^^^^^^^^^^^^^^^^^^

- Fix a couple AJAX quoting/unquoting problems on the TinyMCE plugin.
  [jsbueno]

- Add helper methods image_thumb and tag in order to be listed in 
  folder_summary_view [ericof]

- Fix an UnicodeDecodeError with our plugin for TinyMCE [ericof]


1.0b2 (2012-12-03)
^^^^^^^^^^^^^^^^^^

- Fix a conflict with plone.formwidget.namedfile NamedImage widget
  implementation. [jpgimenez]


1.0b1 (2012-11-27)
^^^^^^^^^^^^^^^^^^

- Update package dependecies for Plone 4.3 compatibility. [hvelarde]

- Fix functional tests. [hvelarde]

- Rename package: was sc.content.embedder and now is sc.embedder. [hvelarde]

- Support for VideoJS as fallback if static file and no supported provider.
  [jpgimenez]

- Fixed the rendering of the embedded code to not break the main view.
  [jpgimenez]

- Allow selecting, embedding and rendering sc.embedder content into TinyMCE
  widgets as if it were images. [jpgimenez]

- VideoJS embedder code implemented as an iframe, to simplify the integration
  with TinyMCE. [jpgimenez]


1.0a3 (2012-10-04)
^^^^^^^^^^^^^^^^^^

- Fixed KeyError: 'width' when saving embeded HTML with percentages.
  [davilima6]


1.0a2 (2012-09-05)
^^^^^^^^^^^^^^^^^^

- Functional tests were updated to run with robotframework-selenium2library.
  [hvelarde]

- i18n was fixed and Spanish translation was updated. [hvelarde]

- Brazilian Prtuguese translation was fixed. [agnogueira]


1.0a1 (2012-09-05)
^^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#8`: https://github.com/simplesconsultoria/sc.embedder/issues/8
