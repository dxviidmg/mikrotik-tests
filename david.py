import routeros_api

connection = routeros_api.RouterOsApiPool('IP', username='admin', password='')
api = connection.get_api()