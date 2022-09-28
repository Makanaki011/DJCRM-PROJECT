from django.urls import path

from .views import (
        lead_detail, 
        lead_update, lead_delete, 
        LeadListView, AssignAgentView, 
        CategoryListView, 
        LeadCreateView, 
        CategoryDetailView, 
        CategoryUpdateView,
        CategoryCreateView,
        CategoryDeleteView,
        LeadCategoryUpdateView
)






app_name= "leads"


urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/',  lead_detail.as_view(), name='lead-detail'),
    path('add-lead/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:pk>/update/', lead_update.as_view(), name='lead-update'),
    path('<int:pk>/delete/', lead_delete.as_view(), name='lead-delete'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name="assign_agent"),
    path('categories/', CategoryListView.as_view(), name="category-list"),
    path('<int:pk>/categories/', CategoryDetailView.as_view(), name="category-detail"),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
   
    
    
    
]





