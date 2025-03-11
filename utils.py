def _get_tr(in_dict):
    return in_dict.get('RepetitionTime')


def _len(inlist):
    return len(inlist)


def _dof(inlist):
    return len(inlist) - 1


def _neg(val):
    return -val

def _dict_ds(in_dict, sub, order=['bold', 'mask', 'events', 'regressors', 'tr']):
    return tuple([in_dict[sub][k] for k in order])