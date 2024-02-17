
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add_physical_info_about_bodybuilder/', views.add_physical_info_about_bodybuilder, name='add_physical_info_about_bodybuilder'),
    path('generate_physical_indicators/', views.generate_physical_indicators, name='generate_physical_indicators'),
    path('manipulating_with_indicators/', views.manipulating_with_indicators, name='manipulating_with_indicators'),
    path('table/', views.table, name='table'),
    path('update_info_about_bodybuilder/', views.update_info_about_bodybuilder, name='update_info_about_bodybuilder'),
    path('create_graphic/', views.create_graphic, name='create_graphic'),
    path('recomendation/', views.recomendation, name='recomendation'),
    path('assessment_of_physical_conditions/', views.assessment_of_physical_conditions, name='assessment_of_physical_conditions'),
    path('create_diagram_for_pulse/', views.create_diagram_for_pulse, name='create_diagram_for_pulse'),
    path('create_diagram_for_steps/', views.create_diagram_for_steps, name='create_diagram_for_steps'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)