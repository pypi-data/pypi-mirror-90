
class Section ():
    ''' Defines how the text should be stored along with subsections '''
    def __init__(self,name,parent,headinglevel):
        self.name = name
        self.parent= parent
        self.headinglevel = headinglevel
        self.text = ""
        self.section_names= []
        self.sections = dict()
        return None

    def __str__(self):
        return str({"text":self.text,"sections":self.section_names})

    def addText(self,text):
        ''' Checks if text inputted is a string and then adds text to text variable else throw Type Error '''
        if isinstance(text,str):
            self.text += text
        else:
            raise TypeError("You can only use string with addText") 

    def addSection(self,sect):
        ''' Checks if section inputted is a section object and then add it to sections dictionary else throw Type Error '''
        if type(sect) == type(self):
            self.sections.update({sect.name:sect})
            self.section_names += [sect.name]
        else:
            raise TypeError("You can only add other sections as a child to another section.")
    def getSection(self,name):
        ''' Returns section object based on section name if section does not exist in sections return -1 '''
        return self.sections.get(name,-1)

