from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({"erro": str(error), "sucesso": False}), 400

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return jsonify({"erro": str(error), "sucesso": False}), 500

