import importlib
import pkgutil
from django.apps import AppConfig
from django.urls import path, re_path, include

from scaffold import appsConfig


class Registrar:
    """
    A hierarchical registrar that supports subrouting with prefix management.
    """
    
    def __init__(self, prefix="", namespace=None):
        self.prefix = prefix.strip("/")
        self.namespace = namespace
        self.patterns = []
        self._subregistrars = []
    
    def route(self, url_string, name=None, method=None):
        """Decorator to register a view function or Class-Based View (CBV)."""
        def decorator(view_obj):
            # Check if view_obj is a Class-Based View (type check) or function
            if isinstance(view_obj, type) and hasattr(view_obj, 'as_view'):
                actual_view = view_obj.as_view()
                default_name = view_obj.__name__.lower().replace("view", "")
            else:
                actual_view = view_obj
                default_name = view_obj.__name__
            
            if method:
                actual_view._allowed_method = method
            
            full_url = self._build_url(url_string)
            view_name = name or default_name
            
            pattern = self._create_pattern(full_url, actual_view, view_name)
            self.patterns.append(pattern)
            
            return view_obj  # Return original class/function
        return decorator
    
    def include(self, subregistrar, prefix="", namespace=None):
        """Include a subregistrar with a prefix and optional namespace."""
        self._subregistrars.append({
            'subregistrar': subregistrar,
            'prefix': prefix.strip("/"),
            'namespace': namespace or subregistrar.namespace
        })

    def include_many(self, *subregistrars):
        """
        Include multiple subregistrars at once.
        Usage: router.include_many(accounts_router, products_router, billing_router)
        """
        for item in subregistrars:
            if isinstance(item, tuple):
                # Supports passing tuple: (subregistrar, prefix, namespace)
                subreg = item[0]
                prefix = item[1] if len(item) > 1 else ""
                namespace = item[2] if len(item) > 2 else None
                self.include(subreg, prefix=prefix, namespace=namespace)
            else:
                # Standard subregistrar instance (uses its own prefix/namespace)
                self.include(item)
                
    def discover(self, package_name):
        """Dynamically import all modules in a package to trigger @route decorators."""
        package = importlib.import_module(package_name)
        for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_module_name = f"{package_name}.{module_name}"
            importlib.import_module(full_module_name)
    
    def get_patterns(self):
        """Retrieve all standard Django urlpatterns."""
        all_patterns = list(self.patterns)
        
        for sub_info in self._subregistrars:
            subregistrar = sub_info['subregistrar']
            prefix = sub_info['prefix']
            namespace = sub_info['namespace']
            
            sub_patterns = subregistrar.get_patterns()
            
            # Django handles namespaces via include((patterns, instance_namespace), namespace=...)
            if namespace:
                included = include((sub_patterns, namespace), namespace=namespace)
            else:
                included = include(sub_patterns)
            
            path_prefix = f"{prefix}/" if prefix else ""
            all_patterns.append(path(path_prefix, included))
        
        return all_patterns
    
    def _build_url(self, url_string):
        url_string = url_string.strip("/")
        if self.prefix:
            prefix = f"{self.prefix}/"
        else:
            prefix = ""
            
        full = f"{prefix}{url_string}"
        # Ensure trailing slash if non-empty
        return f"{full}/" if full else ""
    
    def _create_pattern(self, url_string, view, name):
        regex_chars = ['(?', '^', '$', '|', '+', '*', '{', '}', '[', ']']
        is_regex = any(char in url_string for char in regex_chars)
        
        if is_regex:
            return re_path(f"^{url_string}$", view, name=name)
        else:
            return path(url_string, view, name=name)

# Create a main application instance
registrar = Registrar()

class MyProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myproject"

    def ready(self):
        """Runs once when Django initializes."""

        # 2. Loop strictly through YOUR local apps list
        for app_name in appsConfig.getAppNames():
            try:
                registrar.discover(app_name)
            except (ModuleNotFoundError, ImportError) as e:
                # Safe fallback if an app folder doesn't have views or submodules yet
                pass