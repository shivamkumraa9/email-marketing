import contacts.views as views
from django.urls import path


app_name = "contacts"


urlpatterns = [
	path("new/",views.new_list,name="new_list"),

	path("add/<int:list_id>/",views.add,name="add"),
	path("add-single/<int:list_id>/",views.add_single,name="add_single"),

	path("get/<int:list_id>/",views.get_all,name="get_all"),
	
	path("delete/<int:list_id>/",views.delete,name="delete"),
	path("remove/<int:list_id>/",views.remove,name="remove"),

]