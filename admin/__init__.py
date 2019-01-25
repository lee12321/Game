from flask_admin import Admin, helpers, expose, AdminIndexView
from apps.models import db, BlogModel
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField
from flask_security import Security, SQLAlchemyUserDatastore
from apps.models.UserModel import User, Role
from flask_login import current_user, login_user
from flask import redirect, url_for, request, abort

admin = Admin(name='Blog', base_template='my_master.html', template_mode='bootstrap3')
user_datastore = SQLAlchemyUserDatastore(db, User, Role)  # Setup Flask-Security
security = Security()


class BlogView(ModelView):
    form_overrides = dict(content=CKEditorField)
    can_delete = False  # disable model deletion
    can_view_details = True
    create_template = 'edit.html'
    edit_template = 'edit.html'

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class FeaturedView(ModelView):
    can_delete = False  # disable model deletion
    can_view_details = True
    column_list = ('featured',)

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


admin.add_view(BlogView(BlogModel.Blog, db.session))
admin.add_view(FeaturedView(BlogModel.Featured, db.session))
