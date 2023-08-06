import binascii
import hashlib
import secrets


class Hashing(object):
    def __init__(self):
        self.salt = secrets.token_hex(8)

    @staticmethod
    def _hashify(input_string):
        """Converts the input string to a NTLM hash and returns the hash

        Parameters:
            input_string: string to be converted to NTLM hash
        Returns:
            Converted NTLM hash
        """

        output = hashlib.new('md4', input_string.encode('utf-16le')).digest()

        return binascii.hexlify(output).decode('utf-8').upper()

    def get_hashes(self, input_file):
        """Reads the input file of passwords, converts them to NTLM hashes

        Parameters:
            input_file: file containing strings to convert to NTLM hashes
        Returns:
            Dict that replicates HIBP format: 'hash:occurrence_count'
        """

        output_dict = {}
        with open(input_file, 'r') as f:
            for item in f:
                if item:
                    output_dict[self._hashify(item.strip())] = '0'

        return output_dict

    def obfuscate(self, input_hash):
        """Further hashes the input NTLM hash with a random salt

        Parameters:
            input_hash: hash to be obfuscated
        Returns:
            String containing obfuscated hash
        """

        output = hashlib.new('md4', (input_hash + self.salt).encode('utf-16le')).digest()

        return binascii.hexlify(output).decode('utf-8').upper()
