from pyramid.view import view_config
import gasStation

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'Problem Two: Gas Station'}

@view_config(route_name='result', renderer='templates/result.pt')
def result(request):
    result = gasStation.GasStation.putFile(request)
    return {'result': result}
