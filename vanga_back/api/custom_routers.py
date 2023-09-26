from rest_framework.routers import DefaultRouter


class OnlyGetRouter(DefaultRouter):
    """
    Router class that have only GET method
    """
    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        disallow_methods = ('post', 'put', 'patch', 'delete')
        for method in disallow_methods:
            if method in bound_methods.keys():
                del bound_methods[method]
        return bound_methods
