# -*- coding: utf-8 -*-
from plone import api
from plone.app.standardtiles import PloneMessageFactory as _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from plone.supermodel.model import Schema
from plone.tiles import Tile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema

import json


class ISliderTile(Schema):
    """
    """
    collection_uid = schema.Choice(
        title=_(u"Select an existing content"),
        required=True,
        vocabulary="plone.app.vocabularies.Catalog",
    )
    directives.widget(
        "collection_uid",
        RelatedItemsFieldWidget,
        pattern_options={"selectableTypes": ["Collection"]},
    )

    infinite = schema.Bool(title=_(u"Infinite"), required=False, default=True)

    dots = schema.Bool(title=_(u"Dots"), required=False, default=True)

    arrows = schema.Bool(title=_(u"Arrows"), required=False, default=True)

    centerMode = schema.Bool(title=_(u"Center"), required=False, default=False)

    fade = schema.Bool(title=_(u"fade"), required=False, default=False)

    vertical = schema.Bool(title=_(u"vertical mode"), required=False, default=False)

    autoplay = schema.Bool(title=_(u"Autoplay mode"), required=False, default=False)

    pauseOnFocus = schema.Bool(title=_(u"pause on focus"), required=False, default=True)

    cssEase = schema.TextLine(
        title=_(u"ccsEase"),
        description=_(u"Use css ease"),
        required=False,
        default=_(u"linear"),
    )
    autoplaySpeed = schema.Int(
        title=_(u"autoplaySpeed"),
        description=_(u"Speed of autoplay"),
        required=False,
        default=2000,
    )

    slidesToShow = schema.Int(
        title=_(u"Show"),
        description=_(u"Slides to show"),
        required=False,
        default=4,
    )

    slidesToScroll = schema.Int(
        title=_(u"Scroll"),
        description=_(u"Slider to scroll"),
        required=False,
        default=4,
    )

    speed = schema.Int(
        title=_(u"Speed"),
        description=_(u"Speed"),
        required=False,
        default=300,
        min=100,
    )

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Limit of slides"),
        required=False,
        default=10,
    )
    size = schema.TextLine(
        title=_(u"Image size"),
        description=_(u"Size of image slider (ex: thumb, large,...)"),
        required=False,
        default=_(u"thumb"),
    )
    model.fieldset(
        'display',
        label=_(u'Display options'),
        fields=[
            'title',
            'description',
            'date',
            'all_button',
        ],
    )

    title = schema.Bool(
        title=_(u"Title"),
        required=False,
        default=True,
    )

    description = schema.Bool(
        title=_(u"Description"),
        required=False,
        default=True,
    )

    date = schema.Bool(
        title=_(u"Date"),
        required=False,
        default=True,
    )

    all_button = schema.Bool(
        title=_(u"All button"),
        required=False,
        default=True,
    )

    breakpoint_full = schema.Int(
        title=_(u"breakpoint_full"),
        description=_(u"What size to display in breakpoint_full"),
        required=False,
        default=1024,
    )
    slidesToShow_full = schema.Int(
        title=_(u"slidesToShow_full"),
        description=_(u"how many element to display in breakpoint_full"),
        required=False,
        default=1,
    )

    slidesToScroll_full = schema.Int(
        title=_(u"slidesToScroll_full"),
        description=_(u"how many element scroll in breakpoint_full"),
        required=False,
        default=1,
    )

    breakpoint_medium = schema.Int(
        title=_(u"breakpoint_medium"),
        description=_(u"What size to display in breakpoint_medium"),
        required=False,
        default=600,
    )
    slidesToShow_medium = schema.Int(
        title=_(u"slidesToShow_medium"),
        description=_(u"how many element to display in breakpoint_medium"),
        required=False,
        default=1,
    )
    slidesToScroll_medium = schema.Int(
        title=_(u"slidesToScroll_medium"),
        description=_(u"how many element scroll in breakpoint_medium"),
        required=False,
        default=1,
    )
    breakpoint_small = schema.Int(
        title=_(u"breakpoint_small"),
        description=_(u"What size to display in breakpoint_small"),
        required=False,
        default=480,
    )
    slidesToShow_small = schema.Int(
        title=_(u"slidesToShow_small"),
        description=_(u"how many element to display in breakpoint_small"),
        required=False,
        default=1,
    )
    slidesToScroll_small = schema.Int(
        title=_(u"slidesToScroll_small"),
        description=_(u"how many element scroll in breakpoint_small"),
        required=False,
        default=1,
    )


class SliderTile(Tile):
    """
    """

    template = ViewPageTemplateFile('templates/slider.pt')

    def __call__(self):
        return self.template()

    def contents(self):
        # import pdb; pdb.set_trace()
        uid = self.data["collection_uid"]
        attrs = json.dumps(
            {
                "infinite": self.data["infinite"],
                "dots": self.data["dots"],
                "slidesToShow": self.data["slidesToShow"],
                "slidesToScroll": self.data["slidesToScroll"],
                "speed": self.data["speed"],
                "arrows": self.data["arrows"],
                "centerMode": self.data["centerMode"],
                "fade": self.data["fade"],
                "vertical": self.data["vertical"],
                "cssEase": self.data["cssEase"],
                "autoplay": self.data["autoplay"],
                "autoplaySpeed": self.data["autoplaySpeed"],
                "pauseOnFocus": self.data["pauseOnFocus"],
                "responsive": [
                    {
                        "breakpoint": self.data["breakpoint_full"],
                        "settings": {
                            "slidesToShow": self.data["slidesToShow_full"],
                            "slidesToScroll":self.data["slidesToScroll_full"]
                        }
                    },
                    {
                        "breakpoint": self.data["breakpoint_medium"],
                        "settings": {
                            "slidesToShow": self.data["slidesToShow_medium"],
                            "slidesToScroll":self.data["slidesToScroll_medium"]
                        }
                    },
                    {
                        "breakpoint": self.data["breakpoint_small"],
                        "settings": {
                            "slidesToShow": self.data["slidesToShow_small"],
                            "slidesToScroll":self.data["slidesToScroll_small"]
                        }
                    }
                ]
            }
        )
        display = {
            "title": self.data["title"],
            "description": self.data["description"],
            "date": self.data["date"],
            "all_button": self.data["all_button"],
        }

        size = {
            "size": self.data["size"],
        }
        data = {
            "url": "",
            "results": [],
            "options": attrs,
            "display": display,
            "size": size,
        }
        limit = self.data["limit"]
        if uid and limit:
            collection = api.content.get(UID=uid)
            if collection:
                data["url"] = collection.absolute_url()
                if collection.portal_type == "Collection":
                    data["results"] = collection.queryCatalog(
                        batch=True, b_size=limit)
        return data
