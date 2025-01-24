from django.urls import path
from .views import RegisterView, LoginView, ProfileView, AddPetView  ,PublicPetDashboardView, DeletePetView, SearchPetView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('pets/add/', AddPetView.as_view(), name='add_pet'), 
    path('pets/search/', SearchPetView.as_view(), name='search_pet'), 
    path('dashboard/pets/', PublicPetDashboardView.as_view(), name='public_pet_dashboard'),
    path('pets/<int:pet_id>/delete/', DeletePetView.as_view(), name='delete_pet'),
]
