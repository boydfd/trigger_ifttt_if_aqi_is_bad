def retry_for_exception_decorator(exception, times=5):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            def wrapper_inner():
                return function(*args, **kwargs)

            return retry_for_exception(exception, wrapper_inner, times)

        return wrapper

    return real_decorator


def retry_for_exception(exception, function, times=5):
    for i in range(times):
        try:
            return function()
        except exception:
            if i + 1 == times:
                raise exception