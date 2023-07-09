from ..webapp import db


def blueprints():
    from .main import main as main_blueprint
    from .questions_controllers import question as question_blueprint
    from .exams_controllers import exam as exam_blueprint

    return [main_blueprint, question_blueprint, exam_blueprint]
