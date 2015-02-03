'''
  File: btree.shell   -- save as btree.py
  Author(s): 
  Date: 
  Description: 
'''

from mystack import MyStack
from myqueue import MyQueue
from person import Person
from copy import deepcopy
import sys

class BTreeNode:
    '''
      This module provides the BTreeNode class.  This class will
      be used by the BTree class.  Much of the functionality of
      BTrees is provided by this class.
    '''
    def __init__(self, degree = 1):
        ''' Create an empty node with the indicated degree.'''
        self.numberOfKeys = 0
        self.items = [None]*2*degree
        self.child = [None]*(2*degree+1)
        self.index = None

    def __str__(self):
        st = 'The contents of the node with index '+ \
             str(self.index) + ':\n'
        for i in range(0, self.numberOfKeys):
            st += '   Index   ' + str(i) + '  >  child: '
            st += str(self.child[i])
            st += '   item: '
            st += str(self.items[i]) + '\n'
        st += '                 child: '
        st += str(self.child[self.numberOfKeys]) + '\n'
        return st
    def getNumberOfKeys(self):
        return self.numberOfKeys
    
    def setIndex(self, anInteger):
        self.index = anInteger    
        

    def addItemAndSplit(self, anItem, left, right):
        ''' 
          If the receiver is not full, generate an error.
          If full, split the receiver into two nodes, the
          smallest degree + 1 keys staying in the original node.
          The largest degree keys go into a new node which is
          returned. Note that the last child of the receiver
          and the first child of the new node will be the same.
        '''
      
        #print(anItem)
        degree=len(self.items)//2
        searchDict=self.searchNode(anItem)
        #print(searchDict)
        index=searchDict['nodeIndex']
        #print(index)
        if(self.isFull):
            if (searchDict['found']==False):
                tempNode=BTreeNode(degree+1) #temporary node 
                tempNode.copyItemsAndChildren(self,0,index,0)
                #print(tempNode)
                tempNode.insertItem(anItem,left,right)#inserts in ascending order
                #print("yoyo")
                #print(tempNode)
                
                tempNode.copyItemsAndChildren(self,index,2*degree-1,index+1)
                #print(tempNode)
                tempNode.items[index]=anItem
                tempNode.child[index]=left
                tempNode.child[index+1]=right
                
                self.numberOfKeys=0 #need to set to 0 so that there is no 'index out of range' error, phew..
                self.copyItemsAndChildren(tempNode,0,degree,0)#smallestdegree + 1 keys staying in the original node
    
                
                newNode=BTreeNode(degree)
                newNode.copyItemsAndChildren(tempNode,degree+1,2*degree,0)#The largestdegree keys go into a newNode
                #print(newNode)
                #tempNode.copyItemsAndChildren(self,0,degree,0)
               
                return newNode
            else:
                print("Error")
            
        else:
            st="The receiver node is not full"
        return st
    
    
    def childIndexOf(self, anIndex):
        '''  Answer the index of the child, in the receiver,
          which contains anIndex.  Print an error message if
          there is no such child in the receiver.
        '''
        index = -1
        found = False
        k = 0
        while not found and k <= self.numberOfKeys:
            if self.child[k] == anIndex:
                found = True
                index = k
            else:
                k += 1
        #print("yoyo")
        #print(index)
        if index < 0:
            print( 'Error in childIndexOf' )
        return index

    def clear(self):
        self.numberOfKeys = 0
        self.items = [None]*len(self.items)
        self.child = [None]*len(self.child)
    
    def copyItemsAndChildren(self, fromNode, start, finish, index):
        ''' The receiver, self, gets the contents of the fromNode, from
          index start to finish, along with the next child.  The
          copying within the receiver begins at position index.
        '''
        #copy Items
        itemIndex=index
        #print(itemIndex)
        for item in fromNode.items[start:finish+1]:
            #print(item)
            self.items[itemIndex]=item
            itemIndex+=1
            self.numberOfKeys+=1 #counting number of items
            
        #copy child    
        childIndex=index
        for item in fromNode.child[start:finish+2]:
            #print(item)
            self.child[childIndex]=item
            childIndex+=1
            
        
        pass
    
    def copyWithRight(self, aNode, parentNode):  
        '''Answer a node which contains all the items and children
          of the receiver, followed by the parent item followed by
          all the items and children of aNode.  The receiver and
          aNode are left and right siblings with respect to an
          item within the parentNode.
        '''
        #print("Hello")
        #print(aNode)        
        designatedSib=aNode
        parent=parentNode
        parentItemIndex =parent.childIndexOf(self.index)
        #print(parentItemIndex)
        if parentItemIndex >=0:
            if parentItemIndex==parent.getNumberOfKeys():
                parentItemIndex-=1
            parentItem=parent.items[parentItemIndex]
            result=BTreeNode(len(self.items))#here self is refering to nodeToSearch
            #copy items to resultNode from nodeToSearch
            result.copyItemsAndChildren(self,0,self.numberOfKeys-1,0)#copyItemsAndChildren(self,fromNode,start,finish,index)
            #copy parentItem to resultNode
            result.items[self.numberOfKeys]=parentItem
            result.numberOfKeys+=1
            #copy designatedSib to resultNode
            result.copyItemsAndChildren(designatedSib,0,designatedSib.getNumberOfKeys()-1,result.numberOfKeys)
            return result           
      
     
    def insertItem(self, anItem, left = None, right = None): 
        ''' We assume that the receiver is not full. anItem is
          inserted into the receiver with child indices left and
          right.  This is done while retaining the <= ordering on
          the key of the item.  If the insertion is successful,
          answer True.  If not, answer False.
        '''
        #receiver is the self
        searchDict=self.searchNode(anItem)
        nodeIndex=searchDict['nodeIndex']
        #print(nodeIndex)
        if(searchDict['found']==False):
            for i in range(self.numberOfKeys,nodeIndex,-1):
                self.items[i]=self.items[i-1]#copying to the lastIndex until nodeIndex-1
                self.child[i+1]=self.child[i]
            self.items[nodeIndex]=anItem
            self.child[nodeIndex]=left
            self.child[nodeIndex+1]=right
            self.numberOfKeys+=1 #increasing the numberOfKeys by 1
        return(searchDict['found'])
    
                
                
        
            

    def isFull(self):
        ''' Answer True if the receiver is full.  If not, return
          False.
        '''
        
        return (self.numberOfKeys == len(self.items))

    def removeChild(self, index):
        ''' If index is valid, remove and answer the child at
          location index.  If not, answer None.  In any event,
          do NOT update the key count.  We copy all the rest of
          the child entries towards the start one position.
          The method removeItem will decrement numberOfKeys.
        '''
        pass

    def removeItem(self, index):
        ''' If index is valid, remove and answer the item at
          location index.  Move the rest of the items to fill the
          gap.  Update the key count.  If the index is not valid,
          answer None.
        '''
        if index<=self.numberOfKeys:
            temp=self.items[index]
            remainKey=self.numberOfKeys-1
            for i in range(index,remainKey,1):
                self.items[i]=self.items[i+1]#shifting 1 place to right
            self.numberOfKeys -=1
            self.items[remainKey]=None #putting last item to be None    
            self.removeChild(index) #removing Ritem's child
            return temp
        else:
            return None
            
            
            
    

    def searchNode(self, anItem):
        '''Answer a dictionary satisfying: at 'found'
          either True or False depending upon whether the receiver
          has a matching item;  at 'nodeIndex', either the index of
          the matching item, or in the case of an unsuccessful
          search, the index of the smallest (first) item such that
          anItem < item, or self.numberOfKeys if all items
          are < anItem.  In other words, nodeIndex is the place in the node
          where the object is, or should go if there is room in the node.
        '''
        #print("hello")
        #print(self.items)prints [15, 20, 30, 35] correct
        searchItem=anItem
        count=0
        index=None        
        found=False
        while ((not found) and (count<self.numberOfKeys)):
            if self.items[count]!=searchItem:
                if self.items[count]> searchItem:
                    index=count
                    count=self.numberOfKeys+1
                else:
                    count+=1 #for items less than self.items[count], count+1 is the index
            else:
                found=True
                index=count
        if count==self.numberOfKeys:
            index=self.numberOfKeys
            
        searchDict={'nodeIndex':index,'found':found}
        #print(searchDict['found'])
        
        return searchDict
               
            
            
            
                       
        
    def setIndex(self, anInteger):
        self.index = anInteger

    def setNumberOfKeys(self, anInt ):
        self.numberOfKeys = anInt
    def getNumberOfKeys(self):
        return self.numberOfKeys    

class BTree:
    '''  Comment about the class BTree!!
    '''
    def __init__(self, degree):
        # This method is complete.
        self.degree = degree
        self.rootNode = BTreeNode(degree)
        
        # If time, file creation code, etc.
        self.nodes = {}  # A dictionary
        self.stackOfNodes = MyStack()
        self.rootNode.setIndex(1)
        self.writeAt(1, self.rootNode)
        self.rootIndex = 1
        self.freeIndex = 2

    def __str__(self):
        # This method is complete.
        #print(self.rootIndex)
        st = '  The degree of the BTree is ' + str(self.degree)+\
             '.\n'
        st += '  The index of the root node is ' + \
              str(self.rootIndex) + '.\n'
        
        for x in range(1, self.freeIndex):
            node = self.readFrom(x)
            #print(node)
            if node.getNumberOfKeys() > 0:
                st += str(node) 
        return st
    def inorderSuccessor(self,anItem):
        searchTreeDict=self.searchTree(anItem)
        if searchTreeDict['found']:
            currentNode=self.readFrom(searchTreeDict['fileIndex'])
            self.stackOfNodes.push(currentNode)
            #finding rightChildNode
            rightChildNode=self.readFrom(currentNode.child[searchTreeDict['nodeIndex']+1])
            currentNode=rightChildNode
            nextNode=currentNode.items[0]
            #go left as much as possible
            while currentNode.child[0]!=None:
                self.stackOfNodes.push(currentNode)
                currentNode=self.readFrom(currentNode.child[0])
                nextNode=currentNode.items[0]
            return nextNode,currentNode
        else:
            return None
            
            
        
    def merge(self,nodeToSearch,designatedSib,parent):#merge when the node and its designatedSib have <2N keys
        newNode=nodeToSearch.copyWithRight(designatedSib,parent)
        newNode.setIndex(nodeToSearch.index)
        nodeToSearch=newNode
        self.writeAt(nodeToSearch.index,nodeToSearch)#puting in self.nodes()
        parentItemIndex=parent.childIndexOf(nodeToSearch.index)
        if parentItemIndex>parent.getNumberOfKeys()-1:
            parentItemIndex-=1
        parent.removeItem(parentItemIndex)
        parent.child[parentItemIndex]=nodeToSearch.index
        self.writeAt(parent.index,parent)
        designatedSib.setNumberOfKeys(0)#removing desigSib
        #looking if parent has atlest self.degree items else merge
        if parent.getNumberOfKeys()<self.degree and parent!=self.rootNode:
            grandParent=self.stackOfNodes.pop()
            designatedSib=self.designatedSibling(parent,grandParent)
            #needs to call merge until root
            self.merge(designatedSib,parent,grandParent)
            if grandParent==self.rootNode:
                self.rootNode.setNumberOfKeys(0)
                self.rootIndex=designatedSib.index
                self.rootNode=parent
                    
    def redistribute(self, nodeToSearch,designatedSib,parent):#
        tempNode=nodeToSearch.copyWithRight(designatedSib,parent)
        #print("YoYo")
        #print(tempNode)
                    
        separatingKey=(((tempNode.getNumberOfKeys())+1)//2)-1
        parentItemIndex=parent.childIndexOf(nodeToSearch.index)
        if parentItemIndex>parent.getNumberOfKeys()-1:
            parentItemIndex-=1
        parent.items[parentItemIndex]=tempNode.items[separatingKey]
        nodeToSearch.copyItemsAndChildren(tempNode,0,separatingKey-1,0)
        nodeToSearch.setNumberOfKeys(separatingKey)
        
        #new # and kind of items in sibling
        designatedSib.copyItemsAndChildren(tempNode,separatingKey+1,tempNode.getNumberOfKeys()-1,0)
        
        designatedSib.setNumberOfKeys(tempNode.getNumberOfKeys()-separatingKey-1)
        
        
        
        
    def designatedSibling(self,nodeToSearch,parent):#finding correct sib. for merge
        nodeIndex=nodeToSearch.index
        #print("hello")
        #print(nodeIndex)#prints 4 correct
        #print(parent)
        parentItemIndex=parent.childIndexOf(nodeIndex)
        #print(parentItemIndex)#prints 1, correct
        
        #returning the correct designatedSib
        if parentItemIndex>parent.getNumberOfKeys():
            parentItemIndex-=1
        if parentItemIndex==parent.getNumberOfKeys():#left DS
            return self.readFrom(parent.child[parentItemIndex-1])
        elif parentItemIndex<parent.getNumberOfKeys():#right DS
            return self.readFrom(parent.child[parentItemIndex+1])
            
        
        
        

    def delete(self, anItem):
        ''' Answer None if a matching item is not found.  If found,
          answer the entire item.  
        '''
        searchTreeDict=self.searchTree(anItem)
        #print("yoyo")
        #print(searchTreeDict)# prints{'nodeIndex': 1, 'fileIndex': 4, 'found': True} correct
        if(not searchTreeDict['found']):
            return None
        else:
            nodeToSearch=self.readFrom(searchTreeDict['fileIndex'])
            #print(nodeToSearch)
            if (nodeToSearch.child[0]==None):#checking for if it is a leafNode
                nodeToSearch.removeItem(searchTreeDict['nodeIndex'])
                parent=self.stackOfNodes.pop()#stackOfNodes has nodes pushed during the searchTree method
                #print(parent)#prints node with index 8 correct
                designatedSib=self.designatedSibling(nodeToSearch,parent)
                totalNumOfKeys=nodeToSearch.getNumberOfKeys()+designatedSib.getNumberOfKeys()
                if totalNumOfKeys>=2*self.degree:
                    self.redistribute(nodeToSearch,designatedSib,parent)
                    return anItem
                else:
                    self.merge(nodeToSearch,designatedSib,parent)
                    return anItem
                
            else:
                nextNode,currentNode=self.inorderSuccessor(anItem)
                nodeToSearch.items[searchTreeDict['nodeIndex']],currentNode.items[0]=currentNode.items[0],nodeToSearch.items[searchTreeDict['nodeIndex']]
                currentNode.removeItem(0)
                if (currentNode==self.rootNode) or (currentNode.getNumberOfKeys()>self.degree):
                    return anItem
                else:
                    parent=self.stackOfNodes.pop()
                    designatedSib=self.designatedSibling(currentNode,parent)
                    totalNumOfKeys=currentNode.getNumberOfKeys()+designatedSib.getNumberOfKeys()+1
                    if totalNumOfKeys>2*self.degree:
                        self.redistribute(currentNode,designatedSib,parent)
                        return anItem
                    else:
                        self.merge(currentNode,designatedSib,parent)
                        return anItem
                                                                                        
                    
                    
            
                
                
            
        
            
        

    def inorderOn(self, aFile):
        '''
          Print the items of the BTree in inorder on the file 
          aFile.  aFile is open for writing.
          This method is complete at this time.
        '''
        aFile.write("An inorder traversal of the BTree:\n")
        self.inorderOnFrom( aFile, self.rootIndex)

    def inorderOnFrom(self, aFile, index):
        ''' Print the items of the subtree of the BTree, which is
          rooted at index, in inorder on aFile.
        '''
        currentNode=self.readFrom(index)
        if currentNode!=None:
            for i in range(currentNode.getNumberOfKeys()):
                if currentNode.child[i]!=None:
                    self.inorderOnFrom(aFile,currentNode.child[i])#doing recursion on each node item's child until leafNode is found
                aFile.write(str(currentNode.items[i])+'\n')
            if currentNode.getNumberOfKeys()!=None:#moving to next item in a node
                self.inorderOnFrom(aFile,currentNode.child[currentNode.getNumberOfKeys()])
                
                            
        pass
    def splitNode(self,aNode,anItem,left,right):#during overflow split node creating a newNode
        
            #print(anItem), 35 correct
            #print(aNode),gives 27 and 50 ,correct
            #print("hello")
            newNode=aNode.addItemAndSplit(anItem,left,right)
            
            #print(newNode) #correct newNode with 50 
            newNode.setIndex(self.freeIndex)#careful not .index! it is setIndex
            #print(newNode.index)
            
            self.writeAt(newNode.index,newNode)
            self.freeIndex+=1 #incrementing for newNode
            middleItem=aNode.items[self.degree] #middle goes to parentNode
            #print(middleNode)
            #decreasing original aNode node #of Keys
            aNode.items[self.degree] = None
            aNode.numberOfKeys-=1 #so does not print None
            #print(aNode)
            self.writeAt(aNode.index,aNode) 
            
            if aNode==self.rootNode:
                newRoot=BTreeNode(self.degree)
                newRoot.insertItem(middleItem,aNode.index,newNode.index)# self.insertItem(anItem,left,right), giving references
                newRoot.setIndex(self.freeIndex)
                self.writeAt(self.freeIndex,newRoot)
                self.freeIndex+=1
                self.rootNode=newRoot  #here root reference changes
                self.rootIndex=newRoot.index
            else:
                nodeInPath=self.stackOfNodes.pop()
                if nodeInPath.isFull():#split till not full, recursion
                    self.splitNode(nodeInPath,middleItem,aNode.index,newNode.index)#splitNode(self,aNode,anItem,left,right)
                else:
                    nodeInPath.insertItem(middleItem,aNode.index,newNode.index)
                    self.writeAt(nodeInPath.index,nodeInPath)     

    def insert(self, anItem):
        ''' Answer None if the BTre already contains a matching
          item. If not, insert a deep copy of anItem and answer
          anItem.
        '''
        searchTreeDict = self.searchTree(anItem)
        #print("yoyo")
        #print(searchTreeDict)
        if (searchTreeDict['found']==True):#if True 
            return None
        else:
            newItem = deepcopy(anItem)
            nodeToInsert = self.readFrom(searchTreeDict['fileIndex'])#searchItem ['fileIndex'] give index of a node
            if nodeToInsert.isFull():
                self.splitNode(nodeToInsert,newItem,None,None)
            else:
                nodeToInsert.insertItem(newItem)
                self.writeAt(nodeToInsert.index,nodeToInsert)#inserting into an array of node dict w/ modification
        return anItem            
        
    def levelByLevel(self, aFile):
        ''' Print the nodes of the BTree level-by-level on aFile.
        '''
        aFile.write("A level-by-level listing of the nodes:\n")
        queue=MyQueue()
        queue.enqueue(self.rootNode)
        while not queue.isEmpty():
            currentNode=queue.dequeue()
            aFile.write(str(currentNode))
            for i in range(currentNode.getNumberOfKeys()+1):
                child=self.readFrom(currentNode.child[i])
                if child!=None:
                    queue.enqueue(child)
                
        pass

    def readFrom(self, index):
        ''' Answer the node at entry index of the btree structure.
          Later adapt to files.  This method is complete at this time.
        '''
        if self.nodes.__contains__(index):
            return self.nodes[index]
        else:
            return None

    def recycle(self, aNode):
        # For now, do nothing
        # This method is complete at this time.
        aNode.clear()

    def retrieve(self, anItem):
        ''' If found, answer a deep copy of the matching item.
          If not found, answer None
        '''
        searchTreeDict=self.searchTree(anItem)
        if not searchTreeDict['found']:
            return None
        else:
            item=deepcopy(self.readFrom(searchTreeDict['fileIndex']).items[searchTreeDict['nodeIndex']])
                
        return item
        pass

    def searchTree(self, anItem):
        ''' Answer a dictionary.  If there is a matching item, at
          'found' is True, at 'fileIndex' is the index of the node
          in the BTree with the matching item, and at 'nodeIndex'
          is the index into the node of the matching item.  If not,
          at 'found' is False, but the entry for 'fileIndex' is the
          leaf node where the search terminated.  An important
          function of this method is that it pushes all of the
          nodes of the search path from the rootnode, down to,
          but not including the corresponding leaf node of a search
          (or the node containing a match).  Again, the rootnode
          is pushed if it is not a leaf node and has no match.
        '''
        self.stackOfNodes.clear()#clearing previously put nodes
        currentNode=self.rootNode
        searchDict=currentNode.searchNode(anItem)
        #print(searchDict)
        while(not searchDict['found']) and (not currentNode.child[0]==None):#currentNode.child[0]it's not leaf node
            self.stackOfNodes.push(currentNode)
            nextSearchNode=currentNode.child[searchDict['nodeIndex']]
            #print(nextSearchNode)
            currentNode=self.readFrom(nextSearchNode)
            searchDict=currentNode.searchNode(anItem)
        searchTreeDict={'fileIndex':currentNode.index,'nodeIndex':searchDict['nodeIndex'],'found':searchDict['found']}
        return searchTreeDict   
                        
                                    
    def update(self, anItem):
        ''' If found, update the item with a matching key to be a
          deep copy of anItem and answer anItem.  If not, answer None.
        '''
        searchTreeDict=self.searchTree(anItem)
        if not searchTreeDict['found']:
            return None
        else:
            node=self.readFrom(searchTreeDict['fileIndex'])
            node.items[searchTreeDict['nodeIndex']]=deepcopy(anItem)
            return anItem
            
        pass
    

    def writeAt(self, index, aNode):
        ''' Set the element in the btree with the given index
          to aNode.  This method must be invoked to make any
          permanent changes to the btree.  We may later change
          this method to work with files.
          This method is complete at this time.
        '''
        self.nodes[index] = aNode

def main():
    print('Our names are Laura Masadieu and Dichha Rai ')
    
    print("Test the BTreeNode class:")
    
    # Poor style using instance variables directly!
    # Makes for easier testing, though!!
    n = BTreeNode(2)
    n.items[0:4] = [15,20,30,35]
    n.child[0:5] = [1,2,3,4,5]
    #n.items[0:6] = [15,20,30,35,40,45]
      
    n.numberOfKeys = 4
    #n.numberOfKeys=6
    n.index = 11
    print( "Run 1" )
    print( n.searchNode(30))
    print( n.searchNode(10) )
    print( n.searchNode(31) )
    print( n.searchNode(40) )
    #print( n.searchNode(16) )
    #print( n.searchNode(25) )
    #print( n.searchNode(46))
    print( '' )
    
    b = BTreeNode(3)
    b.index = 133
    b.insertItem(500,19,21) # Child indices do NOT make sense!
    b.insertItem(150,31,43)
    b.insertItem(200,50,62)
    b.insertItem(700,70,18)
    b.insertItem(100,19,10)
    b.insertItem(300,11,12)    
    print( "Run 2" )
    print( b )


    n = BTreeNode(1)
    n.index = 12
    n.insertItem(50,3,34)
    n.insertItem(100, 34, 37)
    print( "Run 3" )
    print( n.searchNode(100) )
    print( n.searchNode(31) )
    print( n.searchNode(90) )
    print( n.searchNode(150) )
    print( '' )
    
    n = BTreeNode(2)
    n.items[0:4] = [15,20,30,35]
    n.child[0:5] = [1,2,3,4,5]
    n.numberOfKeys = 4
    n.index = 10
    print( "Run 4" )
    print( n )
    print( n.addItemAndSplit(32,4,13) )# Try adding 10, 36, ... 
    #print( n.addItemAndSplit(10,7,1) )# Try adding 10, 36, ...
    #print( n.addItemAndSplit(23,3,19) )
    #print( n.addItemAndSplit(16,8,9) )
    print( n )
    
    # This next part is useful for deletion
    n = BTreeNode(4)
    n.items[0:8] = [15,20,30,35,None,None,None,None]
    n.child[0:9] = [1,2,3,4,5,None,None,None,None]
    n.numberOfKeys = 4
    n.index = 6

    p = BTreeNode(4)
    p.items[0:8] = [40,50,60,70,None,None,None,None]
    p.child[0:9] = [6,7,8,9,10,None,None,None,None]
    p.setNumberOfKeys(4)
    p.setIndex(17)

    m = BTreeNode(4)
    m.items[0:8] = [41,42,43,44,None,None,None,None]
    m.child[0:9] = [11,12,13,14,15,None,None,None,None]
    m.setNumberOfKeys(4)
    m.setIndex(7)
    print( "Run 5" )
    print( m )

    new = n.copyWithRight(m,p) 
    print( "Run 6" )
    print( new )
    
    print('Test the BTree class:')
    
    print( ' # run #1 -------------------------------' )
    bt = BTree(1)
    bt.insert(50)
    bt.insert(27)
    bt.insert(35)
    print( bt )

    bt.insert(98)
    bt.insert(201)
    print( bt )

    bt.insert(73)
    bt.insert(29)
    bt.insert(150)
    bt.insert(15)
    print( bt )

    bt.insert(64)
    print( bt )

    bt.insert(83)
    bt.insert(90)
    print( bt )

    bt.insert(87)
    bt.insert(253)
    print( bt )

    bt.insert(84)
    print( bt )
    
    
    print( ' # run #2 -------------------------------' )
    t = BTree(1)
    t.insert(Person('Joe', 38))
    t.insert(Person('Susie',48))
    t.insert(Person('Billy',39))
    t.insert(Person('Tomas',12))
    t.insert(Person('Don',35))
    t.update(Person('Willy', 12))
    print( t.retrieve(Person('', 48)) )
    print( t )

    t.levelByLevel(sys.stdout)
    t.inorderOn(sys.stdout)
    t.delete(Person('',35))
    t.inorderOn(sys.stdout)
    

    print( ' # run#3 -------------------------------' )
    bt = BTree(2)
    bt.insert(20)
    bt.insert(40)
    bt.insert(10)
    bt.insert(30)
    bt.insert(15)
    bt.insert(35)
    bt.insert(7)
    bt.insert(26)
    bt.insert(18)
    bt.insert(22)
    bt.insert(5)
    bt.insert(42)
    bt.insert(13)
    bt.insert(46)
    bt.insert(27)
    bt.insert(8)
    bt.insert(32)
    bt.insert(38)
    bt.insert(24)
    bt.insert(45)
    bt.insert(25)
    print( bt )
    
    
    print( ' # run#4 -------------------------------' )
    bt = BTree(2)
    bt.insert(20)
    bt.insert(40)
    bt.insert(10)
    bt.insert(30)
    bt.insert(15)
    bt.insert(35)
    bt.insert(7)
    bt.insert(26)
    bt.insert(18)
    bt.insert(22)
    bt.insert(5)
    bt.insert(42)
    bt.insert(13)
    bt.insert(46)
    bt.insert(27)
    bt.insert(8)
    bt.insert(32)
    bt.insert(38)
    bt.insert(24)
    bt.insert(45)
    bt.insert(25)
    bt.delete(35)
    bt.delete(38)
    bt.delete(25)
    bt.delete(38)
    print( bt )

    print( ' #run #5 -------------------------------' )
    bt = BTree(1)
    bt.insert(27)
    bt.insert(50)
    bt.insert(35)
    bt.insert(29)
    bt.insert(150)
    bt.insert(98)
    bt.insert(73)
    bt.insert(201)
    print( bt )
    bt.delete(35)
    bt.delete(98)
    bt.delete(29)
    bt.delete(73)
    bt.delete(50)
    bt.delete(150)
    bt.delete(12)
    bt.delete(98)
    print( bt )
    


if __name__ == '__main__': main()

''' The output:
[evaluate btree.py]
My/Our name(s) is/are :Dichha Rai and Laura Mesadieu
Test the BTreeNode class:
Run 1
{'nodeIndex': 2, 'found': True}
{'nodeIndex': 0, 'found': False}
{'nodeIndex': 3, 'found': False}
{'nodeIndex': 4, 'found': False}

Run 2
The contents of the node with index 133:
   Index   0  >  child: 19   item: 100
   Index   1  >  child: 10   item: 150
   Index   2  >  child: 50   item: 200
   Index   3  >  child: 11   item: 300
   Index   4  >  child: 12   item: 500
   Index   5  >  child: 70   item: 700
                 child: 18

Run 3
{'nodeIndex': 1, 'found': True}
{'nodeIndex': 0, 'found': False}
{'nodeIndex': 1, 'found': False}
{'nodeIndex': 2, 'found': False}

Run 4
The contents of the node with index 10:
   Index   0  >  child: 1   item: 15
   Index   1  >  child: 2   item: 20
   Index   2  >  child: 3   item: 30
   Index   3  >  child: 4   item: 35
                 child: 5

The contents of the node with index None:
   Index   0  >  child: 4   item: 32
   Index   1  >  child: 13   item: 35
                 child: 5

The contents of the node with index 10:
   Index   0  >  child: 1   item: 15
   Index   1  >  child: 2   item: 20
   Index   2  >  child: 3   item: 30
                 child: 4

Run 5
The contents of the node with index 7:
   Index   0  >  child: 11   item: 41
   Index   1  >  child: 12   item: 42
   Index   2  >  child: 13   item: 43
   Index   3  >  child: 14   item: 44
                 child: 15

Run 6
The contents of the node with index None:
   Index   0  >  child: 1   item: 15
   Index   1  >  child: 2   item: 20
   Index   2  >  child: 3   item: 30
   Index   3  >  child: 4   item: 35
   Index   4  >  child: 5   item: 40
   Index   5  >  child: 11   item: 41
   Index   6  >  child: 12   item: 42
   Index   7  >  child: 13   item: 43
   Index   8  >  child: 14   item: 44
                 child: 15

Test the BTree class:
 # run #1 -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 35
                 child: 2

  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 35
   Index   1  >  child: 2   item: 98
                 child: 4
The contents of the node with index 4:
   Index   0  >  child: None   item: 201
                 child: None

 # run #1 A -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
   Index   1  >  child: None   item: 73
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 98
                 child: 4
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
                 child: 6

  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
   Index   1  >  child: 8   item: 98
                 child: 4
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
                 child: 6
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None

 # run #1 B -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
                 child: 8
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
   Index   1  >  child: 6   item: 83
                 child: 10
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None
The contents of the node with index 9:
   Index   0  >  child: None   item: 90
                 child: None
The contents of the node with index 10:
   Index   0  >  child: 9   item: 98
                 child: 4

  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
                 child: 8
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
   Index   1  >  child: 6   item: 83
                 child: 10
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None
The contents of the node with index 9:
   Index   0  >  child: None   item: 87
   Index   1  >  child: None   item: 90
                 child: None
The contents of the node with index 10:
   Index   0  >  child: 9   item: 98
   Index   1  >  child: 4   item: 201
                 child: 11
The contents of the node with index 11:
   Index   0  >  child: None   item: 253
                 child: None

  The degree of the BTree is 1.
  The index of the root node is 15.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
                 child: 8
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
                 child: 6
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None
The contents of the node with index 9:
   Index   0  >  child: None   item: 84
                 child: None
The contents of the node with index 10:
   Index   0  >  child: 9   item: 87
                 child: 12
The contents of the node with index 11:
   Index   0  >  child: None   item: 253
                 child: None
The contents of the node with index 12:
   Index   0  >  child: None   item: 90
                 child: None
The contents of the node with index 13:
   Index   0  >  child: 4   item: 201
                 child: 11
The contents of the node with index 14:
   Index   0  >  child: 10   item: 98
                 child: 13
The contents of the node with index 15:
   Index   0  >  child: 7   item: 83
                 child: 14

 # run #2 -------------------------------
Name: Susie Id: 48 
  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: Name: Willy Id: 12 
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: Name: Susie Id: 48 
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: Name: Don Id: 35 
   Index   1  >  child: 4   item: Name: Billy Id: 39 
                 child: 2
The contents of the node with index 4:
   Index   0  >  child: None   item: Name: Joe Id: 38 
                 child: None

A level-by-level listing of the nodes: 
The contents of the node with index 3:
   Index   0  >  child: 1   item: Name: Don Id: 35 
   Index   1  >  child: 4   item: Name: Billy Id: 39 
                 child: 2
The contents of the node with index 1:
   Index   0  >  child: None   item: Name: Willy Id: 12 
                 child: None
The contents of the node with index 4:
   Index   0  >  child: None   item: Name: Joe Id: 38 
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: Name: Susie Id: 48 
                 child: None
An inorder traversal of the BTree:
Name: Willy Id: 12 
Name: Don Id: 35 
Name: Joe Id: 38 
Name: Billy Id: 39 
Name: Susie Id: 48 
An inorder traversal of the BTree:
Name: Willy Id: 12 
Name: Joe Id: 38 
Name: Billy Id: 39 
Name: Susie Id: 48 
 # run#3 -------------------------------
  The degree of the BTree is 2.
  The index of the root node is 9.
The contents of the node with index 1:
   Index   0  >  child: None   item: 5
   Index   1  >  child: None   item: 7
   Index   2  >  child: None   item: 8
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 22
   Index   1  >  child: None   item: 24
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 10
   Index   1  >  child: 5   item: 20
                 child: 2
The contents of the node with index 4:
   Index   0  >  child: None   item: 32
   Index   1  >  child: None   item: 35
   Index   2  >  child: None   item: 38
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 13
   Index   1  >  child: None   item: 15
   Index   2  >  child: None   item: 18
                 child: None
The contents of the node with index 6:
   Index   0  >  child: None   item: 42
   Index   1  >  child: None   item: 45
   Index   2  >  child: None   item: 46
                 child: None
The contents of the node with index 7:
   Index   0  >  child: None   item: 26
   Index   1  >  child: None   item: 27
                 child: None
The contents of the node with index 8:
   Index   0  >  child: 7   item: 30
   Index   1  >  child: 4   item: 40
                 child: 6
The contents of the node with index 9:
   Index   0  >  child: 3   item: 25
                 child: 8

 # run#4 -------------------------------
  The degree of the BTree is 2.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 5
   Index   1  >  child: None   item: 7
   Index   2  >  child: None   item: 8
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 22
   Index   1  >  child: None   item: 24
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 10
   Index   1  >  child: 5   item: 20
   Index   2  >  child: 2   item: 26
   Index   3  >  child: 7   item: 42
                 child: 6
The contents of the node with index 5:
   Index   0  >  child: None   item: 13
   Index   1  >  child: None   item: 15
   Index   2  >  child: None   item: 18
                 child: None
The contents of the node with index 6:
   Index   0  >  child: None   item: 45
   Index   1  >  child: None   item: 46
                 child: None
The contents of the node with index 7:
   Index   0  >  child: None   item: 27
   Index   1  >  child: None   item: 30
   Index   2  >  child: None   item: 32
   Index   3  >  child: None   item: 40
                 child: None

 #run #5 -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
   Index   1  >  child: None   item: 29
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
   Index   1  >  child: None   item: 73
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 35
   Index   1  >  child: 2   item: 98
                 child: 4
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None

  The degree of the BTree is 1.
  The index of the root node is 1.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
   Index   1  >  child: None   item: 201
                 child: None
'''
