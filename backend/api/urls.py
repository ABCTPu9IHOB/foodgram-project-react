from django.urls import include, path

urlpatterns = (
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('users.urls')),
    path('', include('recipes.urls')),
)
