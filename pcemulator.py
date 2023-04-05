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

    def ls(self,args):


        searchHidden=False
        if args==None:
            paths=[]
            optArgs=[]
        else:
            paths, optArgs = args
            for optArg in optArgs:
                if optArg=="-a":
                    searchHidden=True
                else:
                    raise Exception("Optional Arguements are not valid for ls")
            
        
        folderContents=""
        lscwd=self.cwd

        if len(paths)>0:
            for path in paths: 
                if path[0:2] =="~/":#Starting from home
                    self.cwd=self.pc.files.home

                lsterm = Terminal(self.pc)#seperate terminal so we don't change this terminals cwd
                lsterm.cwd = self.cwd
                lsterm.cd(([path],[]))
                lscwd=lsterm.cwd

                folderContents+=lsterm.cwd.name +":\n"
                for child in lscwd.children: 
                    if isinstance(child,Folder):         #different ways to get printable names for Folders and Children
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
                if path != paths[-1]:
                    folderContents+="\n\n"
                    
        else:
            for child in lscwd.children: 
                if isinstance(child,Folder):         #different ways to get printable names for Folders and Children
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

        if args==None:
            mainArgs=[]
            optArgs=[]
        else:
            mainArgs, optArgs = args
        
        if mainArgs==[]:
            self.cwd=self.pc.files.home
            return

        for optArg in optArgs:
            raise Exception("Cd does not take any optinal arguments")
        if len(mainArgs)>1:
            raise Exception("Cd only takes in one main argument: path")
        
        path=mainArgs[0]

        if path[0]=="~":
            self.cwd=self.pc.files.home
            path=path.split("/")
            self._innercd(path[1:])
        else:
            path=path.split("/")
            self._innercd(path)
        
    def _innercd(self,path):#TODO fake terminal so we don't mess up real terminal when cding
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
        if args==None:
            raise Exception("Touch requires argument: fileName")
        else:
            mainArgs, optArgs=args

        for optArg in optArgs:
            raise Exception("Touch does not take any optinal arguments")
        
        fileNames = mainArgs

        cwdFilesStr=self.ls(None)

        for fileName in fileNames:
            if fileName in cwdFilesStr:
                pass
            else:
                lastPeriod=fileName.rfind(".")   
                if lastPeriod==-1:#no period in string
                    self.cwd.addFile(File(fileName[:lastPeriod],""))
                self.cwd.addFile(File(fileName[:lastPeriod],fileName[lastPeriod+1:]))


    def mkDir(self,args):#TODO accept multiple path arguments
        mainArgs, optArgs=args
        for arg in optArgs:
            raise Exception("mkDir takes in no arguments")
        
        for path in mainArgs:
            path =path.split("/")
            directoryName=path[-1]
            path =path[:-1] # if theres one element then []
            
            mkterm = Terminal(self.pc)#seperate terminal so we don't change this terminals cwd
            mkterm.cwd = self.cwd
            if path!=[]:
                mkterm.cd((path,[]))
            mkcwd=mkterm.cwd

            for child in mkcwd.children:
                if isinstance(child,Folder):
                    if child.name==directoryName:
                        raise Exception("Folder already exists")
                    
            mkcwd.addFolder(directoryName)





    def rmDir(self,args):
        mainArgs, optArgs=args
        for arg in optArgs:
            raise Exception("rmDir takes in no arguments")
        
        for path in mainArgs:
            path =path.split("/")
            directoryName=path[-1]
            path =path[:-1] # if theres one element then []
            rmterm = Terminal(self.pc)#seperate terminal so we don't change this terminals cwd
            rmterm.cwd = self.cwd

            if path!=[]:
                try:
                    path="/".join(path)
                    rmterm.cd(([path],[]))
                except:
                    raise Exception("No such file or Directory")
                
            rmcwd=rmterm.cwd

            for index,child in enumerate(rmcwd.children):
                if directoryName == child.name:
                    rmcwd.children.remove(child)
                    break
                else:
                    if index==len(rmcwd.children)-1:
                        raise Exception("No such directory")




    
        

    def rm(self,args):
        pass




    def parseCommand(self,input):
        try:
            input =input.split(' ')
            command = input[0]
        except Exception as CommandProcessingError:
            return("No Command Entered")
        
        args = input[1:]
        optionalArgs=[]
        mainArgs=[]

        for arg in args:
            if arg[0]=="-":
                optionalArgs.append(arg)
            else:
                mainArgs.append(arg)
        if mainArgs==[] and optionalArgs==[]:
            formattedArgs=None
        else:
            formattedArgs=(mainArgs,optionalArgs)

        try:
            if command=='cd':
                return self.cd(formattedArgs)
            elif command=='ls':
                return self.ls(formattedArgs)
            elif command=='touch':
                return self.touch(formattedArgs)
            elif command=='mkdir':
                return self.mkDir(formattedArgs)
            elif command=="rmdir":
                return self.rmDir(formattedArgs)
            
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
