from flask import Flask, Blueprint
from conf import settings
from flask_ckeditor import CKEditor
from flask_admin import helpers as admin_helpers
from flask import url_for
from flask_login import LoginManager
from apps.models.UserModel import User
blueprint = Blueprint('blueprint', __name__)

import apps.blog.routes  # 导入视图函数


def create_app():
    from apps.models import db
    from admin import admin, security, user_datastore

    app = Flask(__name__, static_folder=settings.DevSetting.STATIC_FOLDER)
    app.register_blueprint(blueprint)  # 注册蓝图
    app.config.from_object(settings.DevSetting)  # 修改设置
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

    return app
