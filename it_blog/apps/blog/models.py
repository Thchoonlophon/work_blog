from django.db import models
from django.conf import settings
from django.shortcuts import reverse
import markdown
import re


# Create your models here.

# 文章关键词，用来作为SEO中keywords
class Keyword(models.Model):
    name = models.CharField('Article Keywords', max_length=32)

    class Meta:
        verbose_name = 'Keywords'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField('Article Tags', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('Description', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='Used as a description in SEO, length reference SEO standard')

    class Meta:
        verbose_name = 'Tags'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

    def get_article_list(self):
        '''返回当前标签下所有发表的文章列表'''
        return Article.objects.filter(tags=self)


# 文章分类
class Category(models.Model):
    name = models.CharField('Categories', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('Description', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='Used as a description in SEO, length reference SEO standard')

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)


# 文章
class Article(models.Model):
    IMG_LINK = '/static/blog/img/summary.png'
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Author', on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='Article Title')
    summary = models.TextField('Article Abstract', max_length=230, default='The article summary is equivalent to the page description content, please be sure to fill in...')
    body = models.TextField(verbose_name='Contents')
    img_link = models.CharField('Picture Address', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='Creation Time', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Modified Time', auto_now=True)
    views = models.IntegerField('Reading Amount', default=0)
    slug = models.SlugField(unique=True)
    is_top = models.BooleanField('Stick', default=False)

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    keywords = models.ManyToManyField(Keyword, verbose_name='Keywords',
                                      help_text='Article keywords, used as keywords in SEO, the best use of long tail words, 3-4 enough')

    class Meta:
        verbose_name = 'Articles'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()


# 时间线
class Timeline(models.Model):
    COLOR_CHOICE = (
        ('primary', 'Basic-Blue'),
        ('success', 'Succeed-Green'),
        ('info', 'Info-Azure'),
        ('warning', 'Warning-Orange'),
        ('danger', 'Danger-Red')
    )
    SIDE_CHOICE = (
        ('L', 'Left'),
        ('R', 'Right'),
    )
    STAR_NUM = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    side = models.CharField('Location', max_length=1, choices=SIDE_CHOICE, default='L')
    star_num = models.IntegerField('Star Count', choices=STAR_NUM, default=3)
    icon = models.CharField('Icon', max_length=50, default='fa fa-pencil')
    icon_color = models.CharField('Icon color', max_length=20, choices=COLOR_CHOICE, default='info')
    title = models.CharField('Title', max_length=100)
    update_date = models.DateTimeField('Update Time')
    content = models.TextField('Main Contents')

    class Meta:
        verbose_name = 'Timeline'
        verbose_name_plural = verbose_name
        ordering = ['update_date']

    def __str__(self):
        return self.title[:20]

    def content_to_markdown(self):
        return markdown.markdown(self.content,
                                 extensions=['markdown.extensions.extra', ]
                                 )


# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('Number', help_text='The number determines the order in which the pictures are played, no more than 5 pictures')
    title = models.CharField('Title', max_length=20, blank=True, null=True, help_text='The title can be empty')
    content = models.CharField('Description', max_length=80)
    img_url = models.CharField('Picture Address', max_length=200)
    url = models.CharField('Target Link', max_length=200, default='#', help_text='Image jump hyperlink, default # means no jump')

    class Meta:
        verbose_name = 'Picture racing lamp'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]


# 死链
class Silian(models.Model):
    badurl = models.CharField('Dead Link Address', max_length=200, help_text='Note: the address is a full link format starting with HTTP')
    remark = models.CharField('Dead Link Info', max_length=50, blank=True, null=True)
    add_date = models.DateTimeField('Submit Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Dead Link'
        verbose_name_plural = verbose_name
        ordering = ['-add_date']

    def __str__(self):
        return self.badurl


class FriendLink(models.Model):
    name = models.CharField('Site Name', max_length=50)
    description = models.CharField('Site Description', max_length=100, blank=True)
    link = models.URLField('Blogroll Address', help_text='Please fill in the full formal address beginning with HTTP or HTTPS')
    logo = models.URLField('Site LOGO', help_text='Please fill in the full formal address beginning with HTTP or HTTPS', blank=True)
    create_date = models.DateTimeField('Creation Time', auto_now_add=True)
    is_active = models.BooleanField('Is Validy', default=True)
    is_show = models.BooleanField('Display at Index', default=False)

    class Meta:
        verbose_name = 'Blogroll'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        '''提取友链的主页'''
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])

class AboutBlog(models.Model):
    body = models.TextField(verbose_name='About Contents')
    create_date = models.DateTimeField(verbose_name='Creation Time', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Modified Time', auto_now=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'About'

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

