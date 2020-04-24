# -*- coding: utf-8 -*-
from django.urls import path
from .views import (Toolview, regexview, useragent_view, html_characters,
                    docker_search_view, editor_view,
                    )

urlpatterns = [
    path('', Toolview, name='total'),  # 工具汇总页
    path('regex/', regexview, name='regex'),  # 正则表达式在线
    path('user-agent/', useragent_view, name='useragent'),  # user-agent生成器
    path('html-special-characters/', html_characters, name='html_characters'),  # HTML特殊字符查询
    path('docker-search/', docker_search_view, name='docker_search'),  #docker镜像查询
    path('markdown-editor/', editor_view, name='markdown_editor'), # editor.md 工具
]
