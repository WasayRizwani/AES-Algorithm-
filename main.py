import time
import random
class AES_KeyGenerator:
    def __init__(self,InputKey,rounds):
        self.InputLength = len(InputKey)
        self.InputKey = InputKey
        self.Key = []
        self.rounds = rounds


        self.Sbox =[['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
                    ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
                    ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
                    ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
                    ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
                    ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
                    ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
                    ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
                    ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
                    ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
                    ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
                    ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
                    ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
                    ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
                    ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
                    ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]


        self.Rcon = [['01', '00', '00', '00'],
                        ['02', '00', '00', '00'],
                        ['04', '00', '00', '00'],
                        ['08', '00', '00', '00'],
                        ['10', '00', '00', '00'],
                        ['20', '00', '00', '00'],
                        ['40', '00', '00', '00'],
                        ['80', '00', '00', '00'],
                        ['1b', '00', '00', '00'],
                        ['36', '00', '00', '00']]

        self.hextoDec={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    def KeyExpansion(self):
        inputkey=self.InputKey
        for r in range(self.rounds):
            if r==0:
                for i in range(0,len(inputkey),8):
                    self.Key.append(''.join(inputkey[i:i+8]))

            lastKey=self.Key[-1]
            # print("LAST kEY IS ",lastKey)
            shiftedLastKey=self.CirculaShiftRow(lastKey)
            while len(shiftedLastKey)<8:
                shiftedLastKey+='0'

            # print("SHIFTED LAST KEY IS ",shiftedLastKey)
            subLastKey=self.SboxSubstitution(shiftedLastKey)
            # print("SUBSTITUTED LAST KEY IS ",subLastKey)
            RConLastKey=self.Add_Rcon(subLastKey,r)
            # print("RCON ADDED LAST KEY IS ",RConLastKey)

            newKey=hex(int(self.Key[r*4],16)^int(RConLastKey,16))
            newKey=newKey[2:]
            while len(newKey)<8:
                newKey='0'+newKey
            self.Key.append(newKey)

            for i in range((r*4)+1,(r*4)+4): #1,4  5,8  9,12  13,16
                newKey=hex(int(self.Key[i],16)^int(self.Key[i+3],16))
                newKey=newKey[2:]
                while len(newKey)<8:
                    newKey='0'+newKey
                self.Key.append(newKey)
        return self.Key
    def SboxSubstitution(self,row):
        newRow=''
        for i in range(0,len(row),2):
            # print(i)
            x=int(self.hextoDec[row[i]])
            y=int(self.hextoDec[row[i+1]])
            newRow+=self.Sbox[x][y]
        return newRow
    def Add_Rcon(self,row,round):
        z=''.join(self.Rcon[round])
        row=''.join(row)
        answer=hex(int(row,16)^int(z,16))
        answer=answer[2:]
        if len(answer)==7:
            answer='0'+answer
        return answer
    def CirculaShiftRow(self, Row):
        newRow=Row[2:]+Row[:2]
        return newRow

class AES_Encryption():
    def __init__(self,plainText,Keys,rounds):
        self.plainText=plainText
        self.keys=Keys
        self.rounds=rounds
        self.hextoDec={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
    def addRoundKey(self,round,plainText):
        key=''.join(self.keys[round*4:round*4+4])
        print("KEY IS ",key)
        # print("KEY IS ",key)
        answer=hex(int(plainText,16)^int(key,16))
        answer=answer[2:]
        if len(answer)<32:
            while len(answer)<32:
                answer='0'+answer
        return answer
    def SubBytes(self,plainText):
        self.Sbox = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
                     ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
                     ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
                     ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
                     ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
                     ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
                     ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
                     ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
                     ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
                     ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
                     ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
                     ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
                     ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
                     ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
                     ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
                     ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]
        newPlainText=''
        for i in range(0,len(plainText),2):
            x=int(self.hextoDec[plainText[i]])
            y=int(self.hextoDec[plainText[i+1]])
            newPlainText+=self.Sbox[x][y]
        return newPlainText
    def ShiftRows(self,plainText):
        matrix=[[],[],[],[]]
        for i in range(0,len(plainText),8):
            matrix[0].append(plainText[i:i+2])
            matrix[1].append(plainText[i+2:i+4])
            matrix[2].append(plainText[i+4:i+6])
            matrix[3].append(plainText[i+6:i+8])
        for i in range(1,4):
            matrix[i]=matrix[i][i:]+matrix[i][:i]
        return matrix
    def Multiply_MixColumns(self,NumberOfShifts,hexaValue):
        originalHexaValue=hexaValue
        hexaValue=int(hexaValue,16)

        # print('hello noov',hexaValue)
        if NumberOfShifts==2:
            hexaValue=hexaValue<<1
            # print(hexaValue)
            if hexaValue>255:
                hexaValue=hexaValue^283
        elif NumberOfShifts==3:
            hexaValue = hexaValue << 1
            # print(hexaValue)
            if hexaValue > 255:
                hexaValue = hexaValue ^ 283
            hexaValue=hexaValue^int(originalHexaValue,16)
        else:
            return originalHexaValue
        return hex(hexaValue)[2:]

    def MixRows(self,matrix):
        mixColumnMatrix=[['02','03','01','01'],
                         ['01','02','03','01'],
                         ['01','01','02','03'],
                         ['03','01','01','02']]
        newMatrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    newMatrix[i][j]^=int(self.Multiply_MixColumns(int(mixColumnMatrix[i][k]),matrix[k][j]),16)
                newMatrix[i][j]=hex(newMatrix[i][j])[2:]
                if len(newMatrix[i][j])==1:
                    newMatrix[i][j]='0'+newMatrix[i][j]

        return newMatrix
    def BackToText(self,matrix):
        plainText=''
        for i in range(4):
            plainText+=''.join(matrix[0][i])
            plainText+=''.join(matrix[1][i])
            plainText+=''.join(matrix[2][i])
            plainText+=''.join(matrix[3][i])
        return plainText
    def Encrypt(self):
        plainText=self.plainText
        plainText=self.addRoundKey(0,plainText)
        print('Round 0 input',plainText)
        print('-'*50)
        for i in range(self.rounds):
            if i==self.rounds-1:
                print(' ******* Round  ', i + 1)
                subBytes = self.SubBytes(plainText)
                print('SubBytes output :', subBytes)
                shiftRows = self.ShiftRows(subBytes)
                print('shiftRows output : ', shiftRows)
                shiftRows = self.BackToText(shiftRows)
                plainText=self.addRoundKey(i+1,shiftRows)
                print('Round',plainText)

            else:
                print(' ******* Round  ',i+1)
                subBytes=self.SubBytes(plainText)
                print('SubBytes output :',subBytes)
                shiftRows=self.ShiftRows(subBytes)
                print('shiftRows output : ',shiftRows)
                mixRows=self.MixRows(shiftRows)

                NewPlainText=self.BackToText(mixRows)
                print('Output After Mix Columns is :',NewPlainText)
                RoundAnswer=self.addRoundKey(i+1,NewPlainText)
                print('Round Answer',RoundAnswer[:8]+' '+RoundAnswer[8:16]+' '+RoundAnswer[16:24]+' '+RoundAnswer[24:32])
                plainText=RoundAnswer

            print('-----------------------------------------------------------------------------------------------------------------')
        print('Cipher Text is :',plainText)
        return plainText
            # if i==1:





        plainText=self.plainText
        plainText=self.SubBytes(plainText)
        plainText=self.ShiftRows(plainText)
        plainText=self.MixRows(plainText)
        return plainText

class AES_Decryptor:
    def __init__ (self,EncryptedText,Keys):
        self.EncryptedText=EncryptedText
        self.keys=Keys
        self.InverseSbox=[['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb'],
                            ['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb'],
                            ['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e'],
                            ['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25'],
                            ['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92'],
                            ['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84'],
                            ['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06'],
                            ['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b'],
                            ['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73'],
                            ['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e'],
                            ['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b'],
                            ['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4'],
                            ['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f'],
                            ['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef'],
                            ['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61'],
                            ['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']]
        self.hextoDec = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10,
                        'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    def Multiply_MixColumns(self,NumberOfShifts,hexaValue):
        originalHexaValue = hexaValue
        hexaValue = int(hexaValue, 16)
        result = 0
        degree = 8
        while NumberOfShifts != 1:
            if NumberOfShifts & 1 == 1:
                result = result ^ hexaValue
            hexaValue = hexaValue << 1
            if hexaValue & 256 == 256:
                hexaValue = hexaValue ^ 283
            NumberOfShifts = NumberOfShifts >> 1
        result = result ^ hexaValue
        return hex(result)[2:]
    def MixRows(self,plainText):
        matrix=[[],[],[],[]]
        for i in range(0, len(plainText), 8):
            matrix[0].append(plainText[i:i + 2])
            matrix[1].append(plainText[i + 2:i + 4])
            matrix[2].append(plainText[i + 4:i + 6])
            matrix[3].append(plainText[i + 6:i + 8])

        mixColumnMatrix=[['14','11','13','9'],
                         ['9','14','11','13'],
                         ['13','9','14','11'],
                         ['11','13','9','14']]
        newMatrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    newMatrix[i][j]^=int(self.Multiply_MixColumns(int(mixColumnMatrix[i][k]),matrix[k][j]),16)
                newMatrix[i][j]=hex(newMatrix[i][j])[2:]
                if len(newMatrix[i][j])==1:
                    newMatrix[i][j]='0'+newMatrix[i][j]

        return newMatrix
    def AddRoundKey(self,plainText):
        key=''
        for i in range(4):
            temp=key
            key=self.keys.pop()
            key=key+temp


        print("KEY IS ", key)
        # print("KEY IS ",key)
        answer = hex(int(plainText, 16) ^ int(key, 16))
        answer = answer[2:]
        if len(answer) < 32:
            while len(answer) < 32:
                answer = '0' + answer
        return answer
    def ShiftRows(self,plainText):
        matrix=[[],[],[],[]]
        for i in range(0,len(plainText),8):
            matrix[0].append(plainText[i:i+2])
            matrix[1].append(plainText[i+2:i+4])
            matrix[2].append(plainText[i+4:i+6])
            matrix[3].append(plainText[i+6:i+8])
        print('Matrix is :',matrix)
        for i in range(1,4):
            matrix[i]=matrix[i][4-i:]+matrix[i][:4-i]
        return matrix
    def BackToText(self,matrix):
        plainText=''
        for i in range(4):
            plainText+=''.join(matrix[0][i])
            plainText+=''.join(matrix[1][i])
            plainText+=''.join(matrix[2][i])
            plainText+=''.join(matrix[3][i])
        return plainText
    def SubBytes(self,plainText):

        newPlainText=''
        for i in range(0,len(plainText),2):
            x=int(self.hextoDec[plainText[i]])
            y=int(self.hextoDec[plainText[i+1]])
            newPlainText+=self.InverseSbox[x][y]
        return newPlainText
    def Decrypt(self,plainText):
        print("\n\n\n Decryption Started \n\n\n")
        plainText=self.AddRoundKey(plainText)
        for i in range(9):
            print('-' * 50)
            print("Round ",i+1)
            plainText=self.SubBytes(plainText)
            print("Sub Bytes is ",plainText)
            plainText=self.BackToText(self.ShiftRows(plainText))
            print("Shift Rows is ",plainText)
            plainText=self.AddRoundKey(plainText)
            print("Add Round Key is ",plainText)
            plainText = self.BackToText(self.MixRows(plainText))
            print("Mix Columns is ", plainText)
        print('-' * 50)
        print("Round 10")
        plainText=self.SubBytes(plainText)
        print("Sub Bytes is ",plainText)
        plainText=self.BackToText(self.ShiftRows(plainText))
        print("Shift Rows is ",plainText)
        plainText=self.AddRoundKey(plainText)
        print("Original Text is ",plainText)
        return plainText
f=''
for i in range(32):
    f+='0'

def Test(key,text):
    #AES Key Expansion
    mytest= AES_KeyGenerator(key,10)
    AllKeys=mytest.KeyExpansion()
    #AES Encryption
    myencryptor=AES_Encryption(text.lower(),AllKeys,10)
    EncryptedMesaage= myencryptor.Encrypt()

    #AES DECRYPTION
    MyDecryptor=AES_Decryptor(EncryptedMesaage,AllKeys)
    MyDecryptor.Decrypt(EncryptedMesaage)
with open("key.txt", "r") as file:
    key = file.read()
with open("text.txt", "r") as file:
    text = file.read()
print("Original Text is ",text)
Test(key,text)


def hex_number( count, padded = False ):
    # This currently generates a number of length count hex digits.
    # Pad on the left with 0's if padded is True:
    x = random.randint( 0, 16**count )
    hexdig = "%x" % x
    if padded:
        out = hexdig.zfill( count ) # pad with 0 if necessary
        return out
    else:
        return hexdig


count=0
t_end = time.time() + 60
while time.time() < t_end:
    # do whatever you do
    text=hex_number(32)
    print("Original Text is ", text)
    key=hex_number(32)
    while len(key)<32:
        key='0'+key
    while len(text)<32:
        text='0'+text
    Test(key,text)
    count+=1


print("\n\n\n")
print("Final Results ")
print("Number of tests is ",count)
print("Throughput is ",count/60," tests per second")
