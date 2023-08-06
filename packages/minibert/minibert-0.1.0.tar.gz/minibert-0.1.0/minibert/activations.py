import torch.nn.functional as F


def parse_activation_function(act):
    act = act.strip().lower()
    if act in ("nothing", "none"):
        return lambda x: x
    else:
        return getattr(F, act)
