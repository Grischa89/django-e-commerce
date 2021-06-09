from django.urls import path
from rating import views

urlpatterns = [
    path('products/rate_product/<slug:category_slug>/<slug:product_slug>/', views.rate_product, name='rate-product'),
    path('products/ratings/<slug:category_slug>/<slug:product_slug>/', views.AllRatingsList.as_view(), name="all-ratings"),
    # path('get_rating_avg/', views.RatingsViewSet.as_view()),
]