from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.resources import ModelResource
from admin_panel.models import User, Request, FAQ, Dispatcher, Post, UserLog, NotificationsSettings, ManagerCard, Case


class CustomImportExport(ImportExportModelAdmin, ExportActionModelAdmin):
    pass


# setup export
class UserResource(ModelResource):
    class Meta:
        model = User
        import_id_fields = ('id',)


class UserLogResource(ModelResource):
    class Meta:
        model = UserLog
        fields = ['id', 'user__username', 'state', 'created_at']


class RequestResource(ModelResource):
    class Meta:
        model = Request
        fields = ['id', 'user__username', 'user__fio', 'type', 'support_data', 'calculator_data', 'manager__username', 'created_at']


@admin.register(User)
class UserAdmin(CustomImportExport):
    resource_classes = [UserResource]
    list_display = ('id', 'user_id', 'fio', 'username', 'status', 'manager', 'created_at', 'last_activity')
    list_display_links = ('id', 'user_id')
    list_editable = ('fio', 'username', 'status', 'manager')
    list_filter = ('status',)


@admin.register(UserLog)
class UserLogAdmin(CustomImportExport):
    resource_classes = [UserLogResource]
    list_display = [field.name for field in UserLog._meta.fields]


@admin.register(Request)
class RequestAdmin(CustomImportExport):
    resource_classes = [RequestResource]
    list_display = ('id', 'user', 'calculator_data', 'support_data', 'manager', 'manager_answer', 'created_at')
    list_filter = ('user',)


@admin.register(ManagerCard)
class ManagerCardAdmin(CustomImportExport):
    list_display = [field.name for field in ManagerCard._meta.fields]
    list_editable = [field.name for field in ManagerCard._meta.fields if field.name != 'id']


@admin.register(FAQ)
class FAQAdmin(CustomImportExport):
    list_display = [field.name for field in FAQ._meta.fields]
    list_editable = [field.name for field in FAQ._meta.fields if field.name != 'id' and field.name != 'created_at']


@admin.register(Case)
class FAQAdmin(CustomImportExport):
    list_display = [field.name for field in Case._meta.fields]
    list_editable = [field.name for field in Case._meta.fields if field.name != 'id' and field.name != 'created_at']


@admin.register(Dispatcher)
class DispatcherAdmin(CustomImportExport):
    list_display = [field.name for field in Dispatcher._meta.fields]


@admin.register(Post)
class PostAdmin(CustomImportExport):
    list_display = [field.name for field in Post._meta.fields]
    list_editable = [field.name for field in Post._meta.fields if field.name != 'id' and field.name != 'created_at']


@admin.register(NotificationsSettings)
class NotificationsSettingsAdmin(CustomImportExport):
    list_display = [field.name for field in NotificationsSettings._meta.fields]
    list_editable = [field.name for field in NotificationsSettings._meta.fields if field.name != 'id']


# sort models from admin.py by their registering (not alphabetically)
def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list
