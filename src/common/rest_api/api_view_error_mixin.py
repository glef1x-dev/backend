from typing import Optional, Any

from django.core.exceptions import NON_FIELD_ERRORS, ObjectDoesNotExist, ValidationError
from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class DeveloperErrorResponseException(Exception):
    """
    An exception class that wraps a DRF Response object so that
    it does not need to be recreated when returning a response.
    Intended to be used with and by DeveloperErrorViewMixin.
    """

    def __init__(self, response: Response) -> None:
        super().__init__()
        self.response = response


class DeveloperErrorViewMixin:

    @classmethod
    def api_error(cls, status_code: int, developer_message: str,
                  error_code: Optional[str] = None) -> DeveloperErrorResponseException:
        response = cls._make_error_response(status_code, developer_message, error_code)
        return DeveloperErrorResponseException(response)

    @classmethod
    def _make_error_response(cls, status_code: int, developer_message: str,
                             error_code: Optional[str] = None) -> Response:
        """
        Build an error response with the given status code and developer_message
        """
        error_data = {'developer_message': developer_message}
        if error_code is not None:
            error_data['error_code'] = error_code
        return Response(error_data, status=status_code)

    @classmethod
    def _make_validation_error_response(cls, validation_error: Any) -> Response:
        """
        Build a 400 error response from the given ValidationError
        """
        if hasattr(validation_error, 'message_dict'):
            response_obj = {}
            message_dict = dict(validation_error.message_dict)
            # Extract both Django form and DRF serializer non-field errors
            non_field_error_list = (
                message_dict.pop(NON_FIELD_ERRORS, []) +
                message_dict.pop('non_field_errors', [])
            )
            if non_field_error_list:
                response_obj['developer_message'] = non_field_error_list[0]
            if message_dict:
                response_obj['field_errors'] = {
                    field: {'developer_message': message_dict[field][0]}
                    for field in message_dict
                }
            return Response(response_obj, status=400)
        else:
            return cls._make_error_response(400, validation_error.messages[0])

    def handle_exception(self, exc: Exception) -> Response:
        """
        Generalized helper method for managing specific API exception workflows
        """
        if isinstance(exc, DeveloperErrorResponseException):
            return exc.response
        elif isinstance(exc, APIException):
            return self._make_error_response(exc.status_code, exc.detail)
        elif isinstance(exc, (Http404, ObjectDoesNotExist)):
            return self._make_error_response(404, str(exc) or 'Not found.')
        elif isinstance(exc, ValidationError):
            return self._make_validation_error_response(exc)
        else:
            raise  # lint-amnesty, pylint: disable=misplaced-bare-raise
