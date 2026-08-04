from django.urls import path, include

app_configs = [
	{ 'app_name': 'accounts', 'url': None, 'namespace': 'accounts' },
]

def getAppUrls():
    urlpatterns = []
    for config in app_configs:
        if config['url']:
            urlpatterns.append(
                path(f"{config['url']}", include(f"{config['app_name']}.urls", namespace=config['namespace']))
            )
    return urlpatterns

def getAppNames():
    return [config['app_name'] for config in app_configs]