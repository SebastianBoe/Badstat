def add_query(request):
    query = request.GET['q']
    if query:
        return {'query' : query}
    else: return {}