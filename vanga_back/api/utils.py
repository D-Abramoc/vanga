def get_query_params(query_params) -> list[int]:
    return dict(
        [
            (key, query_params.getlist(key))
            for key in query_params
        ]
    )
