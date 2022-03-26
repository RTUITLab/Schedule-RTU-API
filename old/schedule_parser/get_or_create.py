def get_or_create(session, model, **kwargs):
    instance = (model).query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance