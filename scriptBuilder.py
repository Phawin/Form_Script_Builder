#Edit for Special Characters '\n' : Aug 30, 2018

import random as rnd
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
        if(not(self.hasHeader)):
            print("Compilation Error: No Declaration")
            return
        self.opt = ""
        self.opt+= "//Item Header\n\n"
        self.opt+= self.header
        self.opt+= "\n\n"
        self.opt+= "//Item Configuration\n\n"
        self.opt+= self.body
        self.opt+="\n\n"


    #Small Utility Function
    def formatString(self,s):
        return s.replace("\n","\\n")
        
    #Item Type Set
    def setItemType(self,itemType):
        dic = {"PAGE BREAK":"PageBreak",
               "SECTION HEADER": "SectionHeader",
               "IMAGE": "Image",
               "TEXT":"Text",
               "PARAGRAPH":"ParagraphText",
               "DATE":"Date",
               "DATETIME":"DateTime",
               "TIME":"Time",
               "MULTIPLE CHOICE":"MultipleChoice",
               "CHECKBOX":"Checkbox",
               "LIST":"List"}
        s = "var item = form.add[SOMETHING]Item();\n"
        s = s.replace("[SOMETHING]",dic.get(itemType,"SectionHeader"))
        self.header = s
        self.hasHeader = True
    
    #General Item Properties
    
    def setTitle(self,title):
        title = self.formatString(title)
        s = "item.setTitle('[TITLE]');\n".replace("[TITLE]",title)
        self.body += s
    
    def setHelpText(self,helpText):
        helpText = self.formatString(helpText)
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

    def setImageDriveId(self,fileId): #Google Drive File ID
        s1 = "var img = DriveApp.getFileById('[ID]');\n".replace("[ID]",fileId)
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

class Question(Item):
    
    def __init__(self):
        Item.__init__(self)
        self.choiceStuff = ""
        
    def setQuestionType(self,qt):
        Item.setItemType(self,qt)
        
    #General Question Configuration
    def setPoints(self,val):
        val = int(val)
        s = "item.setPoints([SCORE]);\n".replace("[SCORE]",str(val))
        self.body += s
        
    def setRequired(self,arg = False):
        s = "item.setRequired(false);\n"
        if(arg):
            s = s.replace("false","true")
        self.body += s
    
class ChoiceQuestion(Question):
    def __init__(self):
        Question.__init__(self)
        self.choiceStuff = True
    
    def convertList(self,lst):
        ret = "[<INSIDE>]"
        inside = ""
        n = len(lst)
        for i in range(n):
            inside+=str(lst[i])
            if(i<n-1):
                inside += ", "
        return ret.replace("<INSIDE>",inside)
    
    def setChoice(self,choiceList,hasKey = False,shuffleOrder = False):
        togo = []
        for p in choiceList:
            if(not hasKey):
                togo.append("item.createChoice('[CHOICE]')".replace("[CHOICE]",self.formatString(str(p))))
            else: #Has Answer Key
                s = "item.createChoice('[CHOICE]',false)"
                if(p[1]):
                    s = s.replace("false","true")
                s = s.replace("[CHOICE]",self.formatString(str(p[0])))
                togo.append(s)
        #Now we have all element
        if(shuffleOrder):
            rnd.shuffle(togo)
        middle = self.convertList(togo)
        
        self.choiceStuff = "item.setChoices(<LIST>);\n".replace("<LIST>",middle)
        
    #Overriding Functions
    def compileMe(self):
        self.opt = ""
        if(not(self.hasHeader)):
            print("Compilation Error: No Declaration")
            return
        self.opt = ""
        self.opt+= "//Item Header\n\n"
        self.opt+= self.header
        self.opt+= "\n\n"
        self.opt+= "//Item Configuration\n\n"
        self.opt+= self.body
        self.opt+="\n"
        self.opt+= "//Choice Information\n\n"
        self.opt+= self.choiceStuff
        self.opt+= "\n\n"
        
class CodeBuilder:
    def __init__(self):
        self.data = ""
        self.indent = 0
        
    def setData(self,s,indentCount = 0):
        self.data = s
        self.indent = indentCount
        
    def __str__(self):
        ret = ""
        q = self.data.split("\n")
        idn = " " * self.indent
        for s in q:
            ret+=idn+s+"\n"
        return ret
        
class FormBuilder:
    
    def __init__(self):
        self.opt = "" #Set an empty string as an output
        self.hasHeader = False
        self.header = "//No Header"
        self.body = ""
        self.cb = CodeBuilder()

        
    def addMe(self,s):
        self.opt+=s
        
    def printResult(self):
        print(self.opt)
        
    def getResult(self):
        self.compileMe()
        return self.opt
    
    def __str__(self):
        return self.getResult()

    #Small Utility Function
    def formatString(self,s):
        return s.replace("\n","\\n")
        
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
        formName = self.formatString(formName)
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

    def setCollectEmail(self,collect):
        s = "form.setCollectEmail(false);\n"
        if(collect):
            s = s.replace("false","true")
        self.header += s
        
    def setDescription(self,description):
        description = self.formatString(description)
        s = "form.setDescription('<BODY>');\n".replace("<BODY>",description)
        self.header += s
        
    def setTitle(self,title):
        title = self.formatString(title)
        s = "form.setTitle('<BODY>');\n".replace("<BODY>",title)
        self.header += s
        
    #Function about object!
    def addObject(self,obj,comment = ""):
        self.cb.setData(str(obj),4)
        s = "//Object "+ comment +"\n\n" + str(self.cb) + "//End Of Object "+comment+"\n\n"
        self.body += s