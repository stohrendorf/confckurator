def make_id_response(id):
    """
    Usually used for requests that create single resources.
    :param id: ID of of the created resource.
    :return: Single ID response.
    """
    return {'id': id}


def make_empty_response():
    """
    Usually used for requests that delete resources.
    :return: An empty object.
    """
    return {}
