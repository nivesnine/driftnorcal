from app.admin.controllers import admin as admin_module
from app.auth.controllers import auth as auth_module
from app.site.controllers import site as site_module
from app.events.controllers import events as event_module
from app.shops.controllers import shops as shop_module
from app.media.controllers import media as media_module


def register_blueprints(app):
    app.register_blueprint(site_module)
    app.register_blueprint(auth_module)
    app.register_blueprint(admin_module)
    app.register_blueprint(event_module)
    app.register_blueprint(shop_module)
    app.register_blueprint(media_module)
