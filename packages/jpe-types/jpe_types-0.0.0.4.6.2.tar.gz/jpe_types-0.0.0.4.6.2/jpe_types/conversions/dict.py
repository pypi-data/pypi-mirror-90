from jpe_types.utils import copy


def combineDicts(master: dict, lower: dict):
    """combine 2 dicts

    dot this later
    """
    res = copy(master)
    for key, val in zip(lower, lower.values()):
        if isinstance(val, dict) and key in res:
            res[key] = combineDicts(res[key], lower[key])
            continue
        res[key] = copy(val)

    
    
    return res