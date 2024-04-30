class CommonUtils:

    def __init__(self):
        pass

    # 文字列から4バイト文字を消す
    def remove_4bytes_char(self, text):
        
        # 文字列を bytearray に変換
        byte_string = bytearray(text.encode('utf-8'))

        # バイト列から4バイトのUTF-8文字を除去する
        while b'\xf0' in byte_string:
            index = byte_string.index(b'\xf0')
            if index + 3 < len(byte_string):
                for _i in range(4):
                    byte_string.pop(index)

        # bytearrayを文字列に変換
        return byte_string.decode('utf-8')