

def model_str(instance, attr):
    return hasattr(instance, attr) and getattr(instance, attr) \
           or f'<{instance.__class__.__name__}: {instance.id}>'