from ..webapp import db
def blueprints():
    from .main import main as main_blueprint
    return [main_blueprint]