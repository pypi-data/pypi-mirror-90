class Joueur:
    def __init__(self, name):
        self._name = name
        self._ident = None
        self._alive = True

    def get_name(self):
        return self._name

    def get_ident(self):
        return self._ident

    def set_ident(self, ident):
        if self._ident is not None:
            raise ValueError("Trying to set identity twice for this player: {}".format(self._name))
        self._ident = ident

    def reset(self):
        self._ident = None
        self._alive = True

    def is_alive(self):
        return self._alive

    def kill(self):
        if not self._alive:
            raise ValueError("Trying to kill already dead player: {}".format(self._name))
        self._alive = False