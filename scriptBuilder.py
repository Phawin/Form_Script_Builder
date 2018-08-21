def convertList(lst):
    ret = "[<INSIDE>]"
    inside = ""
    n = len(lst)
    for i in range(n):
        inside+=str(lst[i])
        if(i<n-1):
            inside += ", "
    return ret.replace("<INSIDE>",inside)

import random as rnd
class Question:
    def __init__(self):
        self.header = ""
        self.opt = ""
        self.body = ""
        self.choiceStuff = ""
        self.hasChoice = False
        self.hasHeader = False
        pass
    
    def setQuestionType(self,questionType):
        s = "var item = form.add[SOMETHING]Item();\n"
        
        dic = {"TEXT":"Text",
               "PARAGRAPH":"ParagraphText",
               "DATE":"Date",
               "DATETIME":"DateTime",
               "TIME":"Time"}
        
        self.hasChoice = False
        if(questionType == "MULTIPLE CHOICE"):
            self.hasChoice = True
            s = s.replace("[SOMETHING]","MultipleChoice")
        elif (questionType == "CHECKBOX"):
            self.hasChoice = True
            s = s.replace("[SOMETHING]","Checkbox")
        elif (questionType == "LIST"):
            self.hasChoice = True
            s = s.replace("[SOMETHING]","List")
        else:
            s = s.replace("[SOMETHING]",dic.get(questionType,"Text"))
            
        self.header = s
        self.hasHeader = True
        
    def printResult(self):
        print(self.opt)
        
    def getResult(self):
        self.compileMe()
        return self.opt
    
    def __str__(self):
        return self.getResult()
        
    def compileMe(self):
        self.opt = ""
        if(not(self)):
            print("Compilation Error: No Declaration")
            return
        self.opt = ""
        self.opt+= "//Question Header\n\n"
        self.opt+= self.header
        self.opt+= "\n\n"
        self.opt+= "//Question Configuration\n\n"
        self.opt+= self.body
        self.opt+="\n"
        if(self.hasChoice):
            self.opt+= "\n//Choices\n\n"
            self.opt+= self.choiceStuff
            self.opt+= "\n"
    
    #Question Properties
    
    def setTitle(self,title):
        s = "item.setTitle('[TITLE]');\n".replace("[TITLE]",title)
        self.body += s
        
    def setPoints(self,val):
        val = int(val)
        s = "item.setPoints([SCORE]);\n".replace("[SCORE]",str(val))
        self.body += s
        
    def setRequired(self,arg = False):
        s = "item.setRequired(false);\n"
        if(arg):
            s = s.replace("false","true")
        self.body += s
    
    def setHelpText(self,helpText):
        self.body += "item.setHelpText('[HELP_TEXT]');\n".replace("[HELP_TEXT]",helpText)
        
    #Dealing with "Choices"
    def setChoice(self,choiceList,hasKey = False,shuffleOrder = False):
        togo = []
        for p in choiceList:
            if(not hasKey):
                togo.append("item.createChoice('[CHOICE]')".replace("[CHOICE]",str(p)))
            else: #Has Answer Key
                s = "item.createChoice('[CHOICE]',false)"
                if(p[1]):
                    s = s.replace("false","true")
                s = s.replace("[CHOICE]",str(p[0]))
                togo.append(s)
        #Now we have all element
        if(shuffleOrder):
            rnd.shuffle(togo)
        middle = convertList(togo)
        
        self.choiceStuff = "item.setChoices(<LIST>);\n".replace("<LIST>",middle)
        
class Item:
    def __init__(self):
        self.header = ""
        self.opt = ""
        self.body = ""
        self.hasHeader = False
        pass
        
    def printResult(self):
        print(self.opt)
        
    def getResult(self):
        self.compileMe()
        return self.opt
    
    def __str__(self):
        return self.getResult()
        
    def compileMe(self):
        self.opt = ""
        if(not(self)):
            print("Compilation Error: No Declaration")
            return
        self.opt = ""
        self.opt+= "//Item Header\n\n"
        self.opt+= self.header
        self.opt+= "\n\n"
        self.opt+= "//Item Configuration\n\n"
        self.opt+= self.body
        self.opt+="\n\n"
        
    #Item Type Set
    def setItemType(self,itemType):
        dic = {"PAGE BREAK":"PageBreak",
               "SECTION HEADER": "SectionHeader",
               "IMAGE": "Image"}
        s = "var item = form.add[SOMETHING]Item();\n"
        s = s.replace("[SOMETHING]",dic.get(itemType,"SectionHeader"))
        self.header = s
        self.hasHeader = True
    
    #Question Properties
    
    def setTitle(self,title):
        s = "item.setTitle('[TITLE]');\n".replace("[TITLE]",title)
        self.body += s
    
    def setHelpText(self,helpText):
        self.body += "item.setHelpText('[HELP_TEXT]');\n".replace("[HELP_TEXT]",helpText)

class Image(Item):
    def __init__(self):
        Item.__init__(self)
        Item.setItemType(self,"IMAGE")
        
    def setImageURL(self,url): #Public Image
        s1 = "var img = UrlFetchApp.fetch('[URL]');\n".replace("[URL]",url)
        s2 = "item.setImage(img);\n"
        self.body+=s1
        self.body+=s2
        
    def setAlignment(self,alignmentOption):
        allowed = ["LEFT","CENTER","RIGHT"]
        if(not alignmentOption in allowed):
            alignmentOption = "LEFT"
        s = "item.setAlignment(FormApp.Alignment.<SOMETHING>);\n".replace("<SOMETHING>",alignmentOption)
        self.body+=s
        
    def setWidth(self,width):
        width = int(width)
        s = "item.setWidth(<W>);\n".replace("<W>",str(width))
        self.body+=s

class FormBuilder:
    
    def __init__(self):
        self.opt = "" #Set an empty string as an output
        self.hasHeader = False
        self.header = "//No Header"
        self.body = ""
        
    def addMe(self,s):
        self.opt+=s
        
    def printResult(self):
        print(self.opt)
        
    def getResult(self):
        self.compileMe()
        return self.opt
    
    def __str__(self):
        return self.getResult()
        
    #Script Creator
    
    def compileMe(self):
        self.opt = ""
        self.opt+= "//Header\n\n"
        self.opt+= self.header
        self.opt+= "\n\n"
        self.opt+= "//Body\n\n"
        self.opt+= self.body
        
    #Functions about the form location
    def createNewForm(self,formName):
        s = "var form = FormApp.create('[FORM_NAME]');\n".replace("[FORM_NAME]",formName)
        self.header = s
        self.hasHeader  = True
        
    def useOldForm(self,formId):
        s = "var form = FormApp.openById('[FORM_ID]');\n".replace("[FORM_ID]",formId)
        self.header = s
        self.hasHeader  = True
        
    #Functions about Form Setting
    def setIsQuiz(self,arg):
        if(not(self.header)):
            print("Cannot set a quiz, as you don't have an active form")
            return
        s = "form.setIsQuiz(false);\n"
        if(arg):
            s = s.replace("false","true")
        self.header += s
        
    #Function about object!
    def addObject(self,obj):
        s = "    //Object\n\n" + str(obj) + "    //End Of Object\n\n"
        self.body += s