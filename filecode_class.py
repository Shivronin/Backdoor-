import base64

class Filecode():

    @staticmethod
    def on_code(path :str):
        with open(path, '+rb') as file:
            data = file.read()
        b64 = base64.b64encode(data)
        return b64

    @staticmethod
    def on_decode(path :str, file):
        with open(path, 'wb') as output_file:
            output_file.write(base64.b64decode(file))
