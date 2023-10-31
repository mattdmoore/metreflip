def parameters(rotation, metre, foil):
    return {'rotation': rotation, 'metre': metre, 'foil': foil}


RHYTHM_PARAMETERS = {
    # Pool 1
    195: parameters(2, 3, True),
    259: parameters(4, None, False),

    94: parameters(1, 3, True),
    135: parameters(0, None, False),

    31: parameters(4, 4, True),
    196: parameters(0, None, False),

    29: parameters(0, 4, True),
    133: parameters(2, None, False),

    # Pool 2
    70: parameters(1, 3, True),
    76: parameters(1, None, False),

    66: parameters(1, 3, True),
    82: parameters(3, None, False),

    36: parameters(2, 4, True),
    57: parameters(0, None, False),

    27: parameters(0, 4, True),
    148: parameters(0, None, False)
}
