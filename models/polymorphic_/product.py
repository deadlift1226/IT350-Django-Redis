# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField

from shop.models.product import BaseProductManager, BaseProduct, CMSPageReferenceMixin
from shop.models.defaults.mapping import ProductPage, ProductImage
from ..manufacturer import Manufacturer


@python_2_unicode_compatible
class Product(CMSPageReferenceMixin, BaseProduct):
    """
    Base class to describe a polymorphic product. Here we declare common fields available in all of
    our different product types. These common fields are also used to build up the view displaying
    a list of all products.
    """
    product_name = models.CharField(
        _("Product Name"),
        max_length=255,
    )

    slug = models.SlugField(
        _("Slug"),
        unique=True,
    )

    caption = HTMLField(
        verbose_name=_("Caption"),
        blank=True,
        null=True,
        configuration='CKEDITOR_SETTINGS_CAPTION',
        help_text=_("Short description used in the catalog's list view of products."),
    )

    # common product properties
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Manufacturer"),
    )

    # controlling the catalog
    order = models.PositiveIntegerField(
        _("Sort by"),
        db_index=True,
    )

    cms_pages = models.ManyToManyField(
        'cms.Page',
        through=ProductPage,
        help_text=_("Choose list view this product shall appear on."),
    )

    images = models.ManyToManyField(
        'filer.Image',
        through=ProductImage,
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    objects = BaseProductManager()

    # filter expression used to lookup for a product item using the Select2 widget
    lookup_fields = ('product_name__icontains',)

    def __str__(self):
        return self.product_name

    @property
    def sample_image(self):
        return self.images.first()
