import bcrypt

class BcryptHelper:
    """
    Helper Singleton para encriptar y verificar contraseñas con bcrypt.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BcryptHelper, cls).__new__(cls)
        return cls._instance

    def hash_password(self, plain_password: str) -> str:
        """
        Encripta una contraseña en texto plano.
        """
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si la contraseña coincide con su hash.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Instancia única para importarla fácilmente
bcrypt_helper = BcryptHelper()
