import json
from functools import wraps

from flask import current_app, abort


def json_swag_from(
    filepath, validation=False, definitions=None, validation_function=None
):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                with current_app.open_resource(filepath) as spec_file:
                    spec = json.load(spec_file)

                if hasattr(f, '_spec_'):
                    f._spec_.update(spec)
                else:
                    f._spec_ = spec

                if definitions:
                    if 'definitions' not in f._spec_:
                        f._spec_['definitions'] = {}
                    f._spec_['definitions'].update(definitions)

                return f(*args, **kwargs)

            except FileNotFoundError:
                current_app.logger.error(f"Swagger JSON file not found: {filepath}")
                abort(500, description="Internal server error - documentation missing")
            except json.JSONDecodeError as e:
                current_app.logger.error(
                    f"Invalid JSON in Swagger file {filepath}: {str(e)}"
                )
                abort(500, description="Internal server error - invalid documentation")
            except Exception as e:
                current_app.logger.error(f"Error loading Swagger docs: {str(e)}")
                abort(500, description="Internal server error")

        wrapper._swag_validation = validation
        wrapper._swag_validation_function = validation_function

        return wrapper

    return decorator
