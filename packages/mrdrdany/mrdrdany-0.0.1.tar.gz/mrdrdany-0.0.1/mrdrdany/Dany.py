class Dany:

    def __init__(self):
        self.name = 'Doctor'
        self.lastname = 'Dany'
        self.nickname = 'Mr'

    def WhoIAm(self):
        '''
        This is a function that will show the name. 
        '''
        print('My name is: {}'.format(self.name))
        print('My lastname is: {}'.format(self.lastname))
        print('My nickname is: {}'.format(self.nickname))

    @property
    def email(self):
        return 'email: {}{}{}@gmail.com'.format(self.nickname.lower(),self.name.lower(),self.lastname.lower())

    def thainame(self):
        print('นายดอกเตอร์ แดนนี่')
        return 'นายดอกเตอร์ แดนนี่'
    
    def __str__(self):
        return 'This is a Loong Dany Class'

if __name__ == '__main__':
 
    myloong = Dany()
        
print(myloong)
print(myloong.name)
print(myloong.lastname)
print(myloong.nickname)
myloong.WhoIAm()
print(myloong.email)

myloong.thainame()

print('----------')
mypaa = Dany()

mypaa.name = 'Somsri'
mypaa.lastname = 'Konthai'
mypaa.nickname = 'Sri'
mypaa.WhoIAm()
print(mypaa.name)
print(mypaa.lastname)
print(mypaa.nickname)

