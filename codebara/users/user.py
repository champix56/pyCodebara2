class UserCoreDatas:
    def __init__(self, uid: int, seed: int,hash :str):
        self.uid = uid
        self.seed = seed
        self.hash=hash
        self.serverDataLoc='./contents/user/'+str(uid)

class User(UserCoreDatas):
    def __init__(self, uid: int, seed: int,hash:str, nickname: str, mail: str, amount: int):
        super().__init__(uid, seed,hash)
        self.mail = mail
        self.nickname = nickname
        self.amount = amount
    def parentInstance(self)->UserCoreDatas:
        return UserCoreDatas(self.uid,self.seed,self.hash)
