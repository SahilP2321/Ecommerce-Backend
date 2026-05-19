from django.urls import path
from .views import (
    ProductListView, ProductDetailView, CategoryListView, CategoryDetailView,
    FeaturedProductsView, ProductSearchView, CreateReviewView, ProductReviewsView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('search/', ProductSearchView.as_view(), name='product-search'),
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('<slug:product_slug>/reviews/', ProductReviewsView.as_view(), name='product-reviews'),
    path('<slug:product_slug>/reviews/create/', CreateReviewView.as_view(), name='create-review'),
]