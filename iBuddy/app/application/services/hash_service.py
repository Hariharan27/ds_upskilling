import hashlib

class HashService:
    """
    Generates hashes for documents
    """

    @staticmethod
    def generate_file_hash(file_path: str) -> str:
        """
        Generate sha256 hash for given file path
        """
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:

            while chunk := f.read(8192):
                sha256.update(chunk)

        return sha256.hexdigest()