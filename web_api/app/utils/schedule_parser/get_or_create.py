def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    # print(instance)
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance