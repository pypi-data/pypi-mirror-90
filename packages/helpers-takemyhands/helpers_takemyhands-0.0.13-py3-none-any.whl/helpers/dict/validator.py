def delete_duplicates(self, list):
    """ Delete duplicate dictionary in 'List' """
    return [dict(t) for t in {tuple(d.items()) for d in list}]

    