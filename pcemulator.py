import jsonpickle
"""
Container of Nodes 
Maybe we can attach paths,
The way to get the root easier
"""
class FileSystem(object):
    def __init__(self,homeData):
        self.home=Folder(homeData,None)

    # def insert(self,parent,data):
    #     insertNode = Node(data,parent)
    #     parent.addChild(insertNode)
    #     return insertNode

class Folder(object):
    def __init__(self,name,parent):
        self.parent=parent
        if self.parent!=None:#should only be done when creating a Filesystem with home
            self.parent.children.append(self)
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
        self.data=""
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
            if args[0][0:2] =="~/":#Starting from home
                path = args[0][2:]
            else:
                path=args[0]#starting from cwd

            lsterm = Terminal(self.pc)#seperate terminal so we don't change this terminals cwd
            lsterm.cwd = self.cwd
            lsterm.cd([path])
            lscwd=lsterm.cwd

            #process optional args
            if len(args)>1:
                for arg in args[1:]:
                    if arg[0]=="-":
                        pass
                    else:
                        raise Exception("That is not a correct argument")

        #different ways to get printable names for Folders and Children
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
    

    def cd(self,args):
        if len(args)>1:
            for arg in args[1:]:
                if arg[0]=="-":
                    pass
                else:
                    raise Exception("That is not a correct argument")
        if args==[] or args[0][0]=="~":#Throws error if we evaluate args[0][0] if they don't exist, unless we don't evaluate because we end if early
            self.cwd=self.pc.files.home
        else:
            path=args[0]
            path=path.split("/")
            self._innercd(path)
        



    def _innercd(self,path):
        if path ==[]:#Base case, we went through each part of the path
            return
        if path[0]=="..":
            self.cwd=self.cwd.parent
            return self._innercd(path[1:])
        for child in self.cwd.children:
            if isinstance(child,Folder):
                if child.name==path[0]:
                    self.cwd=child
                    return self._innercd(path[1:])
            else:
                pass #child is a file
        raise Exception("No such directory")
    



    def touch(self,args):
        if len(args)>1:
            for arg in args[1:]:
                if arg[0]=="-":
                    pass
                else:
                    raise Exception("That is not a correct argument")
        lastPeriod=arg.rfind(".")
        self.cwd.addFile(File(arg[:lastPeriod],arg[lastPeriod+1:]))



    def mkDir(self,args):
        pass




    def rmDir(self,args):
        if len(args)>1:
            for arg in args[1:]:
                if arg[0]=="-":
                    pass
                else:
                    raise Exception("That is not a correct argument")
        for child in self.cwd.children:
            if isinstance(child,Folder):
                if child.name==args[0]:
                    self.cwd.children.remove(child)
            else:
                pass
        raise Exception("No such directory")


    
        

    def rm(self,args):
        pass




    def parseCommand(self,input):#TODO TODO TODO process optional args so it can pass through [main arg,[optional args]]
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
            elif command=='touch':
                return self.touch(args)
        except Exception as errorInApp:
            return(str(errorInApp))
        
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