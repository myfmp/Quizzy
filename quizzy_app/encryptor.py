from cryptography.fernet import Fernet

# Replace this with your actual key (Base64 encoded)
SECRET_KEY = b'7wfipQTkMo4wVqBZiKmBkWR86DPv8J51G5EpL5I3-NI='

SECRET_KEY_2 = b'7ofipQTkMo4wVqBZiKmBkWR86DPv8J51G5EpL5I3-NI='

def encrypt_data(data):
    cipher_suite = Fernet(SECRET_KEY)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

def decrypt_data(cipher_text):
    cipher_suite = Fernet(SECRET_KEY)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text

def encrypt_data_2(data):
    cipher_suite = Fernet(SECRET_KEY_2)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

def decrypt_data_2(cipher_text):
    cipher_suite = Fernet(SECRET_KEY_2)
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text