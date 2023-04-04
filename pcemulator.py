import jsonpickle
"""
Container of Nodes 
Maybe we can attach paths,
The way to get the root easier
"""
class FileSystem(object):
    def __init__(self,homeData):
        self.home=Folder(homeData,parent=None)

    # def insert(self,parent,data):
    #     insertNode = Node(data,parent)
    #     parent.addChild(insertNode)
    #     return insertNode

class Folder(object):
    def __init__(self,name,parent):
        if parent!=None:
            parent.children.append(self)
        self.children=[]
        self.name=name
    def addFolder(self,name):
        folder =Folder(name,self) #We do not append the Folder as a child because it appends itself as a child when created
        return folder
    def addFile(self,file):
        self.children.append(file)
    def __str__(self):
        return self.name

class File():
    def __init__(self,name,extension):
        self.name=name
        self.extension=extension
        self.displayName=name+"."+extension
    def __str__(self):
        return self.displayName

"""
Pc class holds a filesystem
Holds preset default pcs with their own files on them
"""
class Pc(object):
    def __init__(self,files):
        self.files=files
    @staticmethod
    def defaultPc():
        files=FileSystem("Macintosh")
        home=files.home
        users=home.addFolder("Users")
        user=users.addFolder("User")
        Desktop=user.addFolder("Desktop")
        Desktop.addFile(File("Image","png"))
        Desktop.addFile(File("Demo","txt"))
        Documents=user.addFolder("Documents")
        Pictures=user.addFolder("Pictures")
        Music=user.addFolder("Music")
        Movies=user.addFolder("Movies")
        Downloads=user.addFolder("Downloads")
        TerminalProfile=user.addFile(File(".terminalProfile",".term"))
        return Pc(files)
    @staticmethod
    def hackersPc():#Oooh maybe when you thwart the hacker you get to take over their pc which has more features
        pass
    def addTerminal(self):
        return Terminal(self)


"""
Attach onto a pc to call operations with it and display things to user
"""
class Terminal(object):
    def __init__(self,pc):
        self.pc=pc
        self.cwd=pc.files.home
        self.inputText=""

    def ls(self,args):
        folderContents=""
        lscwd=self.cwd
        searchHidden=False
        if len(args)>0:
            if args[0][0:2] =="~/":
                path = args[0][2:]
                lsterm = Terminal(self.pc)
                lsterm.cwd = self.pc.files.root
                lsterm.cd([path])
                lscwd=lsterm.cwd
            else:
                path=args[0]
                lsterm = Terminal(self.pc)
                lsterm.cwd = self.cwd
                lsterm.cd([path])
                lscwd=lsterm.cwd

            if len(args)>1:
                for arg in args[1:]:
                    if arg == "-a":
                        searchHidden=True
                    else:
                        raise Exception("Unknown Arguement")
        for child in lscwd.children:
            if isinstance(child,Folder):
                        if child.name[0]==".":
                            if searchHidden:         
                                folderContents +=child.name + " "
                        else:
                            folderContents +=child.name + " "
            else:
                if child.name[0]==".":
                            if searchHidden:         
                                folderContents +=child.displayName + " "
                else:
                    folderContents +=child.displayName + " "

        return folderContents
    

    def cd(self,args):#This is the one only for the terminal for parser
        if args==[]:
            return self.cd(["~"])
        path=args[0]
        path=path.split("/")
        if path[0]=="~":
            self.cwd=self.pc.files.root
        else:
            self._innercd(path)

    def _innercd(self,path):#make work with any working directory, so we can use for ls
        if path ==[]:
            return
        for child in self.cwd.children:
            if isinstance(child,Folder):
                if child.name==path[0]:
                    self.cwd=child
                    return self._innercd(path[1:])
            else:
                pass #child is a file
        raise Exception("No such file or directory")
        
    def parseCommand(self,input):
        try:
            input =input.split(' ')
            command = input[0]
        except Exception as CommandProcessingError:
            return("No Command Entered")
        
        args = input[1:]
        try:
            if command=='cd':
                return self.cd(args)
            elif command=='ls':
                return self.ls(args)
        except Exception as CommandReturnError:
            return(str(CommandReturnError))
        
        return("Command not found")
    


if __name__ == "__main__":
    pc =Pc.defaultPc()
    term=Terminal(pc)
    while True:
        print(term.cwd.name + ">", end="")
        result=term.parseCommand(input())
        if result!=None:
            print(result)
#TODO fake cwd for cding and for both fake cwds if some wrong path is there then return an error or something
#^^Maybe deep clone current terminal and then just cd and then return a value for the other things im gonna add next
#TODO change the getPrompt to be handled by the UI