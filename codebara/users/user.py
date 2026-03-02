class UserCoreDatas:
    def __init__(self, uid: int, seed: int):
        self.uid = uid
        self.seed = seed

class User(UserCoreDatas):
    def __init__(self, uid: int, seed: int, nickname: str, mail: str, amount: int):
        super(uid, seed)
        self.mail = mail
        self.nickname = nickname
        self.amount = amount
