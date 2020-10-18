from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from product.models import Product

class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
    def lastmod(self,obj):
        return obj.timeStamp
class StaticViewSitemap(Sitemap):
    def items(self):
        return {'product:show','product:detail','product:home'}
    def loaction(self,item):
        return reverse(item)