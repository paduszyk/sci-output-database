from django.urls import include, path

urlpatterns = [
    path("articles/", include("attainments.elements.articles.urls")),
    path("patents/", include("attainments.elements.patents.urls")),
    path("grants/", include("attainments.elements.grants.urls")),
]
