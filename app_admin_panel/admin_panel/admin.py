from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.resources import ModelResource
from admin_panel.models import User, Request, FAQ, Dispatcher, Post


class CustomImportExport(ImportExportModelAdmin, ExportActionModelAdmin):
    pass


# setup export
class UserResource(ModelResource):
    class Meta:
        model = User
        import_id_fields = ('id',)


class RequestResource(ModelResource):
    class Meta:
        model = Request
        fields = ['id', 'user__username', 'user__fio', 'type', 'support_data', 'calculator_data', 'manager__username', 'created_at']


@admin.register(User)
class UserAdmin(CustomImportExport):
    resource_classes = [UserResource]
    list_display = ('id', 'user_id', 'fio', 'username', 'status', 'created_at')
    list_display_links = ('id', 'user_id')
    list_editable = ('fio', 'username', 'status')


@admin.register(Request)
class RequestAdmin(CustomImportExport):
    resource_classes = [RequestResource]
    list_display = ('id', 'user', 'calculator_data', 'support_data', 'manager', 'manager_answer', 'created_at')
    list_filter = ('user',)


@admin.register(FAQ)
class FAQAdmin(CustomImportExport):
    list_display = [field.name for field in FAQ._meta.fields]
    list_editable = [field.name for field in FAQ._meta.fields if field.name != 'id' and field.name != 'created_at']


@admin.register(Dispatcher)
class DispatcherAdmin(CustomImportExport):
    list_display = [field.name for field in Dispatcher._meta.fields]


@admin.register(Post)
class PostAdmin(CustomImportExport):
    list_display = [field.name for field in Post._meta.fields]
    list_editable = [field.name for field in Post._meta.fields if field.name != 'id' and field.name != 'created_at']


# sort models from admin.py by their registering (not alphabetically)
def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list
