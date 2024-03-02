from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, ValidationError, ErrorDetail, NotFound
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status
import logging

log = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    data = {
            'data': { "results": [] },
            'error_message': "",
            'error_type': "",
    }

    if response is None:
        data['error_message'] = "Unexpected internal server error."
        data['error_type'] = "INTERNAL_SERVER_ERROR"
        log.info(f"\n\n {exc} \n\n")
        log.info(f"\n\n {context} \n\n")

        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if isinstance(exc, Http404):
        data['error_message'] = "Can't find the data with provided informations."
        data['error_type'] = "DATA_DOES_NOT_EXISTS"
        log.info(f"\n\n {exc} \n\n")
        log.info(f"\n\n {context} \n\n")
        return Response(data=data, status=status.HTTP_200_OK)

    if isinstance(exc, ValidationError):
        for value in response.data.values():
            if isinstance(value, str):
                data["error_message"] += value
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ErrorDetail):
                        data["error_message"] += str(item)

        data["error_type"] =  "VALIDATION_ERROR"
        log.info(f"\n\n {exc} \n\n")
        log.info(f"\n\n {context} \n\n")
        return Response(data=data, status=status.HTTP_200_OK)
    
    if isinstance(exc, AuthenticationFailed):
        data['error_message'] = "You need to login for trigger the process"
        data['error_type'] = "USER_UNAUTHORIZED"
        log.info(f"\n\n {exc} \n\n")
        log.info(f"\n\n {context} \n\n")
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied):
        data['error_message'] = "You don't have the permissions for this process."
        data['error_type'] = "USER_FORBIDDEN"
        log.info(f"\n\n {exc} \n\n")
        log.info(f"\n {context} \n\n")
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    return response