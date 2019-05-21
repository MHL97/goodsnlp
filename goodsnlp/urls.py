from django.conf.urls import include, url
from django.contrib import admin
from myapp import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'goodsnlp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(urls, namespace='myapp')),
]
