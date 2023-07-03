from ..webapp import db
def blueprints():
    from .main import main as main_blueprint
    from .questions_controllers import question as question_blueprint
    return [main_blueprint,question_blueprint]