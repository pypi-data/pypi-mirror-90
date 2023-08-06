class Victoire:

    def __init__(self, type, alive_players, joueurs):
        self.gagnants = []
        self.message = ""
        self.type = type
        if type == "pede":
            for j in joueurs.values():
                if j.get_ident() == "pede":
                    self.gagnants.append((j.get_name(), j.get_ident()))
                    self.message = "Victoire de {} en tant que pédé!".format(j.get_name())
        elif type == "ble":
            self.message = "Victoire des blés!"
            for name in alive_players:
                for j in joueurs.values():
                    if j.get_name() == name:
                        self.gagnants.append((j.get_name(), j.get_ident()))
        elif type == "tony":
            for j in joueurs.values():
                if j.get_ident() == "tony":
                    self.gagnants.append((j.get_name(), j.get_ident()))
                    self.message = "Victoire de {} en tant que Tony!".format(j.get_name())
        elif type == "loup-garou":
            for j in joueurs.values():
                if j.get_ident() == "loup-garou":
                    self.gagnants.append((j.get_name(), j.get_ident()))
                    self.message = "Victoire de {} en tant que loup-garou!".format(j.get_name())
        else:
            raise ValueError("No victory defined for this type: {}".format(type))





