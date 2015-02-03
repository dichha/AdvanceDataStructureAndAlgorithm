'''
  File:  avltree.py  copied from avltree.shell
  Author(s): 
  Date:  
  Description:  This module provides the AVLNode and AVLTree classes.    
'''

from person import Person
from mystack import MyStack
from copy import deepcopy

testing1 = False
testing2 = False

def printStack(aStack):
   newStack = deepcopy(aStack)
   while not newStack.isEmpty():
      node = newStack.pop()
      printOneNode(node)
      
def printOneNode(aNode):
   print(aNode.item)


class AVLNode:
   def __init__(self, item, balance = 0):
      self.item = item
      self.left = None
      self.right = None
      self.balance = balance
      
   def __str__(self):
      ''' This returns a string representing an inorder traversal of the
        nodes of the tree rooted at self.  This lists the balance of each node.
      '''
      st = ''
      if self.left != None:
         st = str(self.left)
      st = st + str(self.item) + ' ' + str(self.balance) + '\n'
      if self.right != None:
         st = st + str(self.right) 
      return st
   
   def myPrint(self):
      ''' This returns a string representing a more complete picture of what
        the tree rooted at self actually looks like.
      '''
      st = '('
      if (self.left == None):
         st += '*'
      else:
         st += self.left.myPrint()
      st += str(self.item)
      if (self.right == None):
         st += '*'
      else:
         st += self.right.myPrint()
      st += ')'
      return st
   
   
   def rotateLeft(self):#case 3a
      '''  Perform a left rotation of the subtree rooted at the
       receiver.  Answer the root node of the new subtree.  
      '''
      child = self.right
      if (child == None):
         print( 'Error!  No right child in rotateLeft.' )
         return None  
      else:
         self.right = child.left 
         child.left = self
         return child

   def rotateRight(self):
      '''  Perform a right rotation of the subtree rooted at the
       receiver.  Answer the root node of the new subtree. 
      '''
      child = self.left
      if (child == None):
         print( 'Error!  No left child in rotateRight.' )
         return None 
      else:
         self.left = child.right 
         child.right = self
         return child

   def rotateRightThenLeft(self):
      '''Perform a double inside left rotation at the receiver.  We
       assume the receiver has a right child (the bad child), which has a left 
       child. We rotate right at the bad child then rotate left at the pivot 
       node, self. Answer the root node of the new subtree.  We call this 
       case 3, subcase 2.
      '''
      pivot= self
      badChild = self.right
      badGrandChild = badChild.left
      badChild.left = badGrandChild.right
      badGrandChild.right = badChild
      self.right = badGrandChild.left
      badGrandChild.left = self
      return badGrandChild
   
      
   def rotateLeftThenRight(self):#case 3.2
      '''Perform a double inside right rotation at the receiver.  We
       assume the receiver has a left child (the bad child) which has a right 
       child. We rotate left at the bad child, then rotate right at 
       the pivot, self.  Answer the root node of the new subtree. We call this 
       case 3, subcase 2.
      '''
      pivot = self
      badChild = self.left
      badGrandChild = badChild.right
      badChild.right = badGrandChild.left
      badGrandChild.left = badChild
      self.left = badGrandChild
      self.left = badGrandChild.right
      badGrandChild.right = self
      return badGrandChild 

   
class AVLTree:
   def __init__(self):
      self.root = None
      self.count = 0
      
   def __str__(self):
      st = 'There are ' + str(self.count) + ' nodes in the AVL tree.\n'
      return st + str(self.root)
   
   def myPrint(self):
      return self.root.myPrint()
   
   def insert(self, newItem):
      '''  Add a new node with item newItem.  Perform any rotations 
        necessary to maintain the AVL tree, including any needed
        updates to the balances of the nodes. We do not allow duplicates. 
      '''
      if self.root == None:
         self.count = 1
         self.root = AVLNode( newItem )
      else:
         (pivot, theStack, parent, found) = self.search(newItem)
         if not found:           
            self.count += 1
            if newItem < parent.item:
               parent.left = AVLNode(newItem)
            else:
               parent.right = AVLNode(newItem)
            if pivot == None:
               self.case1(theStack,pivot,newItem)
            elif newItem < pivot.item and pivot.balance > 0:
               #print("pivot balance")
               #print(pivot.balance)               
               self.case2(theStack, pivot, newItem)
            elif (newItem > pivot.item and pivot.balance < 0):
               self.case2(theStack, pivot, newItem)
            else:
               self.case3(theStack, pivot, newItem)


   def adjustBalances(self, theStack, pivot, newItem):
      current=self.root
      done=False
      while not done and not theStack.isEmpty():
         current=theStack.pop()
         if newItem>current.item and pivot!=0:
            current.balance=current.balance+1
         elif newItem<current.item and pivot!=0:
            current.balance=current.balance-1
         if current.balance==0:
            pivot=current
            break

   def case1(self, theStack, pivot, newItem):
      '''  There is no pivot node.  Adjust the balances of all the nodes
         in theStack.
      '''
      self.adjustBalances(theStack, pivot, newItem)
            
   def case2(self, theStack, pivot, newItem):
      ''' The pivot node exists.  We have inserted a new node into the
         subtree of the pivot of smaller height.  Hence, we need to adjust 
         the balances of all the nodes in the stack up to and including 
         that of the pivot node.  No rotations are needed.
      '''
      self.adjustBalances(theStack, pivot, newItem)
            
   def case3(self, theStack, pivot, newItem):
      '''  The pivot node exists.  We have inserted a new node into the
         larger subtree of the pivot node.  Hence rebalancing and 
         rotations are needed.
      '''
      if newItem < pivot.left.item:
         print("work")
         print(pivot.left.item)
         badChild = pivot.left
         self.case3aLeft(theStack,pivot,newItem,badChild)
      elif newItem > pivot.right.item:
         badChild = pivot.right
         self.case3bRight(theStack,pivot,newItem,badChild)
      else: 
         if newItem<pivot.item and newItem>pivot.left.Item:
            badChild=pivot.left
            if badChild.right!=None:
               badGrandChild=badChild.right
            else:
               badGrandChild = None
            self.case3bLeft(theStack,pivot,newItem,badChild,badGrandChild)
         elif newItem>pivot.item and newItem<pivot.right.item:
            badChild=pivot.right
            if badChild.left!=None:
               badGrandChild=badChild.left
            else:
               badGrandChild=None
      
            self.case3bRight(theStack,pivot,newItem,badChildGrandChild)
      
         
   def case3aLeft(self, theStack, pivot, newItem, badChild):
      '''  We are inserting into the left subtree of the pivot and
        are inserting into the left subtree of the badChild.  We perform
        a right rotation at the pivot.
      #'''
      if newItem < badChild and newItem<pivot:
         pivot.rotateRight()
         current = self.root
      while current != None:
         if newItem<current.item:
            current=current.left
         else:
            current=current.right
      if newItem < badChild and newItem<pivot:
         pivot.rotateRight()      
         
      
      
   def case3aRight(self, theStack, pivot, newItem, badChild):
      '''  We are inserting into the right subtree of the pivot and
        are inserting into the right subtree of the badChild.  We perform
        a left rotation at the pivot.
      '''
      self.adjustBalances(theStack, pivot, newItem)
      badChild = pivot.right
      if newItem > badChild and newItem > pivot:
         pivot.rotateLeft()

      
   def case3bLeft(self, theStack, pivot, newItem, badChild, badGrandChild):  
      '''  We are inserting into the left subtree of the pivot and inserting
        into the right subtree of the badChild.  We rotate left at the bad
        child, then rotate right at the pivot
      '''
      self.adjustBalances(theStack, pivot, newItem)
      badChild = pivot.left
      if badChild.right != None:
         badGrandChild = badChild.right
         if newItem > badChild and newItem < pivot:
            badChild.rotateLeft()
            pivot.rotateRight()
      else:
         badGrandChild = None
         if newItem > badChild and newItem < pivot:
            badChild.rotateLeft()
            pivot.rotateRight()              
      
   def case3bRight(self, theStack, pivot, newItem, badChild, badGrandChild):  
      '''  We are inserting into the right subtree of the pivot and inserting
        into the left subtree of the badChild.  We rotate right at the bad
        child, then rotate left at the pivot
      '''
      self.adjustBalances(theStack, pivot, newItem)
      badChild = pivot.right
      if badChild.right!= None:
         badGrandChild = badChild.right
         if newItem < badChild and newItem >pivot:
            badChild.rotateRight()
            pivot.rotateLeft()
      else:
         badGrandChild = None
         badChild.rotateRight()
         pivot.rotateLeft()
         
            
         
   def search(self, newItem):
      current=self.root
      pivot=None
      found=False
      theStack=MyStack()
      while not found and current!=None:
          parent=current
          if newItem<current.item:
              theStack.push(current)
              if current.balance!=0:
                  pivot=current
              current=current.left
          elif newItem ==current.item:
              theStack.push(current)
              found=True
          else:
              theStack.push(current)
              if current.balance!=0:
                  pivot=current
              current=current.right
      return (pivot,theStack,parent,found)
   
            
   def printSearch(self, searchResult):
      print('The pivot is: ') 
      printOneNode(searchResult[0])
      print('The stack, from top to bottom, is ')
      printStack(searchResult[1]) 
      print('The parent is:')
      printOneNode(searchResult[2])
      print('Found is', searchResult[3])
      print()

            
def main():
   print("our names are Dichha Rai and Yunfei Xie ")
   a = AVLNode(27, 1)
   b = AVLNode(39, -1)
   c = AVLNode(-137)
   d = AVLNode(2934,-1)
   e = AVLNode(33)
   f = AVLNode(100)
   g = AVLNode(30)
   h = AVLNode(35)

   t = AVLTree()
   t.root = b
   b.left = a
   a.left = c
   a.right = e
   b.right = d
   d.left = f
   e.left = g
   e.right = h
   
   print(t)
   print(t.myPrint())
   print(t.myPrint() == '(((*-137*)27((*30*)33(*35*)))39((*100*)2934*))')
   print()
   searchResult = t.search(30)
   t.printSearch(searchResult)
   print(t.root.rotateLeftThenRight())
   print(t.myPrint())
   print()
   
   print("Testing cases 1 and 2: \n")
   t = AVLTree()
   t.insert(57)
   #print(t)
   t.insert(30)
   #print(t)
   t.insert(72)
   t.insert(26)
   #print(t)
   t.insert(35)
   #print(t)
   t.insert(63)
   #print(t)
   t.insert(33)
   print(t)
   print(t.myPrint())
   print(t.myPrint() == '(((*26*)30((*33*)35*))57((*63*)72*))')
               
if __name__ == '__main__': main()
   
''' Output from evaluation main():
My (our) name is (are) 
There are 0 nodes in the AVL tree.
-137 0
27 1
30 0
33 0
35 0
39 -1
100 0
2934 -1

(((*-137*)27((*30*)33(*35*)))39((*100*)2934*))
True

The pivot is: 
27
The stack, from top to bottom, is 
30
33
27
39
The parent is:
30
Found is True

-137 0
27 1
30 0
33 0
35 0
39 -1
100 0
2934 -1

((*35*)39((*100*)2934*))

Testing cases 1 and 2: 

There are 7 nodes in the AVL tree.
26 0
30 1
33 0
35 -1
57 -1
63 0
72 -1

(((*26*)30((*33*)35*))57((*63*)72*))
True
'''
