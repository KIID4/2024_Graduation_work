# 사용자 정보 저장
class userInfo:
    def __init__(self, userID, fileName):
        self.userID = userID
        self.fileName = fileName

    def get_userID(self):
        return self.userID

    def get_fileName(self):
        return self.fileName