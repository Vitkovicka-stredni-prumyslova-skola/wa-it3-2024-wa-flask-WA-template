from datetime import date
class User:
    #Můžeme mít jen jeden konstruktor
    def __init__(self,nick,email):
        self.__datumReg = date.today()
        if email == None:
            self.__email = "Nezadán"
        else:
            self.__email = email

        self.__nick = nick
    
    def get_nick(self):
        return self.__nick
    
    def set_nick(self,nick):
        self.__nick = nick

    def get_datum_registrace(self):
        return self.__datumReg
    
    def get_email(self):
        return self.__email

    def toString(self):
        return (f"<p><b>User:</b> {self.get_nick()}</br><b>e-mail:</b> {self.__email}\n</br><b>Datum registrace:</b> {self.__datumReg}</p>")
    


        

