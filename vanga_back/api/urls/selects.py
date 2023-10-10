from django.urls import path

from ..views.selects import (CategoriesWithSalesInShop, CategoryViewSet,
                             GroupsWithSalesInShop, ProductViewSet,
                             SubcategoriesWithSalesInShop)

urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('category/', CategoryViewSet.as_view({'get': 'list'})),
    path(
        'groups_whith_sales/',
        GroupsWithSalesInShop.as_view({'get': 'list'})
    ),
    path('categories_with_sales/',
         CategoriesWithSalesInShop.as_view({'get': 'list'})),
    path('subcategories_with_sales/',
         SubcategoriesWithSalesInShop.as_view({'get': 'list'})),
]
