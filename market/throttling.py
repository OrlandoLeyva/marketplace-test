from rest_framework.throttling import UserRateThrottle, AnonRateThrottle 

class ProductCreteThrottle(UserRateThrottle):
    '''
    If the method is post, applies throttle using the product-create scope
    '''
    scope = 'product-create'

    def allow_request(self, request, view):
        if not request.method == 'POST':
            return True
        return super().allow_request(request, view)

class ProductListThrottle(UserRateThrottle):
    '''
    If the method is get, applies throttle using the list-create scope
    '''
    scope = 'product-list'

    def allow_request(self, request, view):
        if not request.method == 'GET':
            return True
        return super().allow_request(request, view)

class UpdateDeleteThrottle(UserRateThrottle):
    scope = 'update_delete'

    def allow_request(self, request, view):
        # check if the request method is PUT or DELETE
        if request.method not in ['PUT', 'DELETE']:
            return True

        # limit the number of update and delete requests to 5 per day per user
        return super().allow_request(request, view)
