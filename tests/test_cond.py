import goto


def test_empty_cond():
    res = goto.util.cond()
    assert res() == None


def test_single_value_cond():
    res = goto.util.cond(
        ('a', 'b')
    )()
    assert res == 'b'


def test_multiple_value_cond():
    res = goto.util.cond(
        ('a', 'b'),
        ('b', 'c')
    )()
    assert res == 'b'


def test_single_function_cond():
    # Identity function
    ident = lambda x: lambda: x

    res = goto.util.cond(
        (ident('a'), 'b')
    )()
    assert res == 'b'
    res = goto.util.cond(
        (ident('a'), ident('b'))
    )()
    assert res == 'b'
    res = goto.util.cond(
        ('a', ident('b'))
    )()
    assert res == 'b'


def test_multiple_function_cond():
    # Identity function
    ident = lambda x: lambda: x

    res = goto.util.cond(
        (ident('a'), ident('b')),
        (ident('b'), ident('c'))
    )()
    assert res == 'b'
    res = goto.util.cond(
        (ident(False), ident('b')),
        (ident('b'), ident('c'))
    )()
    assert res == 'c'

def test_with_arguments():
    is_equal = lambda x: lambda y: x == y

    res = goto.util.cond(
        (is_equal('x'), 'y'),
        (is_equal('y'), 'z'),
        (is_equal('z'), 'x')
    )('z')
    assert res == 'x'

