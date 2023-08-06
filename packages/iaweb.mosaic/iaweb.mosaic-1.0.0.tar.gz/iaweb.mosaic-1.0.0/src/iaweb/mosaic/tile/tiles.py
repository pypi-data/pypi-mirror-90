# -*- coding: utf-8 -*-
from plone import api
from plone.app.standardtiles import PloneMessageFactory as _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.supermodel.model import Schema
from plone.tiles import Tile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema


class INewsTile(Schema):
    """A tile that displays a listing of content items"""

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    uid = schema.Choice(
        title=_(u"Select an existing content"),
        required=True,
        vocabulary='plone.app.vocabularies.Catalog',
    )
    directives.widget(
        'uid',
        RelatedItemsFieldWidget,
        pattern_options={'selectableTypes': ['Collection', 'Folder']},
    )

    limit = schema.Int(
        title=_(u'Limit'),
        description=_(u'Limit Search Results'),
        required=False,
        default=8,
        min=1,
    )

    limit_slider = schema.Int(
        title=_(u'Limit slider'),
        description=_(u'Number of element in slider'),
        required=False,
        default=4,
        min=1,
    )


class NewsTile(Tile):
    """A tile that displays a listing of content items"""

    template = ViewPageTemplateFile('templates/tile_news.pt')

    def __call__(self):
        return self.template()

    def contents(self):
        uid = self.data["uid"]
        data = {
            'url': '',
            'results': [],
        }
        if uid:
            container = api.content.get(UID=uid)
            catalog = api.portal.get_tool('portal_catalog')
            limit = self.data["limit"]
            if container:
                data["url"] = container.absolute_url()
                if container.portal_type == 'Folder':
                    results = container.listFolderContents(
                        contentFilter={"portal_type": ["Event", "News Item"]},
                    )
                    for result in results[:limit]:
                        obj = catalog(UID=result.UID())
                        if obj:
                            data["results"].append(obj[0])
                if container.portal_type == 'Collection':
                    results = container.queryCatalog(batch=True, b_size=limit)
                    for result in results:
                        data["results"].append(result)
        return data

    def title(self):
        return self.data["title"]

    @property
    def slider_limit(self):
        return self.data["limit_slider"]

    def slider_class(self):
        limit = self.data["limit_slider"]
        if limit == 1:
            return 'flexslider carousel one'
        else:
            return 'flexslider carousel multiple'
