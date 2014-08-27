from zipfile import ZipFile
import json 
import os #for system("pause")

class ZipHintCracker:
    def __init__(self, passCandidate, zipPath, hashPath):
        self.pwdHint       = passCandidate
        self.zipInfo       = ZipFile(zipPath, "r")
        self.loadPermutations(hashPath)
    
    #tests a password on a given zip file
    def testPwd(self, pwd, checkMethod=ZipFile.testzip):
        self.zipInfo.setpassword(pwd)
        try:
            checkMethod(self.zipInfo)
            #if no exception was raised, it was the right password
            return True
        except RuntimeError as err:
            #if it's not the right password, intercept the runtime error
            if err[0] == 'Bad password for file':
                return False
            #the runtime error was not one we expected, re-raise it
            else:
                raise

    #test all elements in a table (or iterateable ;))
    def testTable(self,table):
        for i in table:
            if self.testPwd(i): #if it's the right password
                return i		#return the password
        return False			#otherwise return False
    
	#test the hint string
    def testHint(self):
        return self.testTable(self.permuteHint())
    
    #set up the hash from a json file of possible substitution
    def loadPermutations(self,path):
        with open(path) as f:
            self.permHash = json.load(f)

    #permute a given character based on a dictionary of known substitutions
    #   is a generator, so this function returns an iteratable object
    def permuteCharacter(self,char):
        if(char): #as long as we're not dealing with "" (empty string)
            if(char.isalpha()):  #yield both cases of any alphabetical character
                yield char.upper()
                yield char.lower()
        #if the character is in the hash then run through all its members
        else:
            yield char

        if(type(self.substitutions.get(char)) == list):
            for perm in self.substitutions.get(char):
                yield perm

    #permute a given string based on a dictionary of known substitutions
    #   is a generator, so it's used in for loops
    def permuteString(self, string):
        char = string[:1]
        rest = string[1:]
        if(len(string)> 1):
            for permutation in self.permuteCharacter(char):
                for restPermutation in self.permuteString(rest):
                    yield permutation+restPermutation
        else:
            for permutation in self.permuteCharacter(char):
                yield permutation
    
    def permuteHint(self):
        return self.permuteString(self.pwdHint)

print("program loaded, I hope you're in interactive mode")
os.system("pause")
