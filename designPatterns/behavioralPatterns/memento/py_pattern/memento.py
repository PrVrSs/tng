import copy


def Memento(obj, deep=False):
    state = (copy.copy, copy.deepcopy)[bool(deep)](obj.__dict__)

    def restore():
        obj.__dict__.clear()
        obj.__dict__.update(state)
    return restore


class Transaction:
    """
    A transaction guard. This is realy just
    syntactic suggar arount a memento closure.
    """

    deep = False

    def __init__(self, *targets):
        self.targets = targets
        self.states = None
        self.commit()

    def commit(self):
        self.states = [Memento(target, self.deep) for target in self.targets]

    def rollback(self):
        for state in self.states:
            state()


class Transactional(object):
    """
    Adds transactional semantics to methods. Methods decorated
    with @transactional will rollback to entry state upon exceptions.
    """

    def __init__(self, method):
        self.method = method

    def __get__(self, obj, T):
        def transaction(*args, **kwargs):
            state = Memento(obj)
            try:
                return self.method(obj, *args, **kwargs)
            except:
                state()
                raise
        return transaction


if __name__ == '__main__':

    class NumObj(object):

        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return '<%s: %r>' % (self.__class__.__name__, self.value)

        def increment(self):
            self.value += 1

        @Transactional
        def do_stuff(self):
            self.value = '1111' # <- invalid value
            self.increment()    # <- will fail and rollback

    n = NumObj(-1)
    print(n)
    t = Transaction(n)
    try:
        for i in range(3):
            n.increment()
            print(n)
        t.commit()
        print('-- commited')
        for i in range(3):
            n.increment()
            print(n)
        n.value += 'x'  # will fail
        print(n)
    except:
        t.rollback()
        print('-- rolled back')
    print(n)
    print('-- now doing stuff ...')
    try:
        n.do_stuff()
    except:
        print('-> doing stuff failed!')
        import traceback
        traceback.print_exc(0)
        pass
    print(n)
