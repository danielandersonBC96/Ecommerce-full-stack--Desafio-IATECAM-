import bcrypt

class Hash:
    @staticmethod
    def hash(value: str) -> str:
        salt = bcrypt.gensalt()
        hashed_value = bcrypt.hashpw(value.encode('utf-8'), salt)
        return hashed_value.decode('utf-8')

    @staticmethod
    def compare_hash(plain_value: str, hashed_value: str) -> bool:
        return bcrypt.checkpw(plain_value.encode('utf-8'), hashed_value.encode('utf-8'))
