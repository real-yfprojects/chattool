import re

class Protocol:
    pass

class SendMessage(Protocol):
    def __init__(self, version, name, text, role='user', encoding='ascii'):
        self.version = version
        self.name = name
        self.role = role
        self.text = text
        self.encoding = encoding

    def makemessage(self):
        self.message = (f'[INFO]version="{self.version}"[/INFO]' # version will be a version object when final
        f'[REGISTER]name="{self.name}",role="{self.role}"[/REGISTER]'
        f'[MESSAGE]length="{len(self.text)}",'
        f'message="{self.text}"[/MESSAGE]')

    def getraw(self):
        return self.message # return just protocol message
    def getbin(self):
        return self.message.encode(self.encoding) # return encoded message

class RecieveMessage(Protocol):
    def __init__(self, message, encoding='ascii'):
        self.message = message
        self.encoding = encoding
        
    def decodemessage(self):

        text = self.message.decode(self.encoding)
        print(text)

        info = re.search('INFO(.+?)/INFO', text) # isolate info part
        if info:
            version = info.group(1)[1:-1]
        else:
            raise Exception # will be custom exception object when final
        
        register = re.search('REGISTER(.+?)/REGISTER', text) # isolate register part
        if register:
            name = register.group(1)[1:-1]
            role = register.group(1)[1:-1]
        else:
            raise Exception # will be custom exception object when final

        message = re.search('MESSAGE(.+?)/MESSAGE', text)
        if message:
            length = message.group(1)[1:-1]
            rcvmessage = message.group(1)[1:-1]
        else:
            raise Exception # will be custom exception object when final

        return {'version':version, 'name':name, 'role':role, 'length':length, 'message':rcvmessage}



class StartConnection(Protocol):
    pass

if __name__ == '__main__':
    mymessage = SendMessage(1.0, 'Simon', 'Hello World') # test all protocols
    mymessage.makemessage()
    rcv = RecieveMessage(mymessage.getbin(), 'ascii')
    print(rcv.decodemessage())