from flask import Flask, Blueprint

from apps.blog.celery_task import make_celery
from conf import settings
from flask_ckeditor import CKEditor
from flask_admin import helpers as admin_helpers
from flask import url_for
from flask_login import LoginManager
from apps.models.UserModel import User
from flask_login import current_user
import flaskfilemanager

blueprint = Blueprint('blueprint', __name__)

import apps.blog.routes  # 导入视图函数


def create_app():
    from apps.models import db
    from admin import admin, security, user_datastore

    app = Flask(__name__, static_folder=settings.ProductSetting.STATIC_FOLDER)
    app.register_blueprint(blueprint)  # 注册蓝图
    app.config.from_object(settings.ProductSetting)  # 修改设置
    db.init_app(app)  # APP注册数据库
    ckeditor = CKEditor(app)
    security_ctx = security.init_app(app, user_datastore)
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security_ctx.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    admin.init_app(app)

    def my_access_control_function():
        """
        :return: True if the user is allowed to access the filemanager, otherwise False
        """
        # You can do whatever permission check you need here
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    flaskfilemanager.init(app, access_control_function=my_access_control_function)  # 文件管理器
    return app
