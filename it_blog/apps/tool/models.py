from django.db import models


# Create your models here.

class ToolCategory(models.Model):
    name = models.CharField('Site Category name', max_length=20)
    order_num = models.IntegerField('Serial Number', default=99, help_text='Serial Numbers can be used to adjust the order, the smaller the more forward')

    class Meta:
        verbose_name = 'Tools Categories'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name


class ToolLink(models.Model):
    name = models.CharField('Site Name', max_length=20)
    description = models.CharField('Site Description', max_length=100)
    link = models.URLField('Site Link')
    order_num = models.IntegerField('Serial Number', default=99, help_text='Serial Numbers can be used to adjust the order, the smaller the more forward')
    category = models.ForeignKey(ToolCategory, verbose_name='Site Category', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Recommended Tools'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name
