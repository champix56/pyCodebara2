class UserCoreDatas:
    def __init__(self, uid: int, seed: int):
        self.uid = uid
        self.seed = seed

class User(UserCoreDatas):
    def __init__(self, uid: int, seed: int, nickname: str, mail: str, amount: int):
        super().__init__(uid, seed)
        self.mail = mail
        self.nickname = nickname
        self.amount = amount
    def parentInstance(self)->UserCoreDatas:
        return UserCoreDatas(self.uid,self.seed)
