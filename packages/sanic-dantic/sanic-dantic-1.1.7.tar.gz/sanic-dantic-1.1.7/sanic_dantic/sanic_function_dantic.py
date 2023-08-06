# -*- coding: utf-8 -*-
from functools import wraps

from sanic.request import Request

from .basic_definition import validate, DanticModelObj


def parse_params(methods: [str] = None, header=None, path=None, query=None, form=None, body=None):
    """
    Sanic Dantic Function View type check decorator, you can use it for any view.

    It can be used in function-based view:

    - you can use it directly without **methods** param

    It's also can used in Class-based view:

    - **methods** parameter is not required. it will be applicable to all view checks if don't give

    :param methods: List Type, which is used to specify the method, and decorate all method if it is not given
    :param header: pydantic.BaseModel
    :param path: pydantic.BaseModel
    :param query: pydantic.BaseModel
    :param form: pydantic.BaseModel
    :param body: pydantic.BaseModel
    :param strict: bool or list, if bool, all models will use strict mode or not, if list, the same model name's model will use strict mode
    """
    
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            _request = [item for item in (request,) + args if isinstance(item, Request)][0]
            if (methods and _request.method.upper() in [_.upper() for _ in methods]) or not methods:
                model_obj = DanticModelObj(header=header, path=path, query=query, form=form, body=body)
                parsed_args = validate(_request, **model_obj.items)
                kwargs.update({'params': parsed_args})
                _request.ctx.params = parsed_args
            response = await f(request, *args, **kwargs)
            return response
        
        return decorated_function
    
    return decorator
