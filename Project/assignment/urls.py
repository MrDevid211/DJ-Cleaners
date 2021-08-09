from django.conf.urls import include, url
from django.contrib import admin
from main import views as main_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'assignment.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls), # Убрал include для исправления ошибки
    url(r'^cleaners/', include(('cleaners.urls', 'cleaners'), namespace='cleaners')),
    url(r'^customers/', include(('customers.urls', 'customers') , namespace='customers')),
    url(r'^$', main_views.home)
]
