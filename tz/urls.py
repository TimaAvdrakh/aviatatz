from django.urls import path
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get-cheapest-ticket', CheapestTicketView.as_view()),
    path('get-all-cache', AllCachedKeys.as_view()),
]
