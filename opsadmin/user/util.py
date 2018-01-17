from Crypto.Cipher import AES

class prpcrypt(object):
    def __init__(self,key):
        self.key = self.pad_key(bytes(key,encoding='utf-8'))
        self.mode = AES.MODE_ECB
        self.aes = AES.new(self.key,self.mode)

    def pad(self,text):
        while len(text) % 16 != 0:
            text += b' '
        return text

    def pad_key(self,key):
        while len(key) % 16 != 0:
            key += b' '
        return key

    def encrypt(self,text):
        text = bytes(text,encoding='utf-8')
        encrypt_text = self.aes.encrypt(self.pad(text))

        return encrypt_text

    def decrypt(self,serect):

        return str(self.aes.decrypt(serect),encoding='utf-8',errors='ignore').strip(' ')
