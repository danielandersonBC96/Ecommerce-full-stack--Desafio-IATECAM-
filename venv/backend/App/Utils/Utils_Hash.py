from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def hash(value: str) -> str:
        """
        Hashes the provided value using bcrypt.

        Args:
            value (str): The value to be hashed (e.g., password).

        Returns:
            str: The bcrypt hashed value.
        """
        return pwd_context.hash(value)

    @staticmethod
    def compare_hash(plain_value: str, hashed_value: str) -> bool:
        """
        Compares a plain value with a hashed value to verify if they match.

        Args:
            plain_value (str): The plain value to compare (e.g., password).
            hashed_value (str): The previously hashed value to compare against.

        Returns:
            bool: True if the plain value matches the hashed value, False otherwise.
        """
        return pwd_context.verify(plain_value, hashed_value)
