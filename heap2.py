
'''
  File:  heap.shell -- change to .py
  Author: Dichha Rai
  Date:9/11/12
  Description:  This module provides the class Heap.  We can create heaps which
     are either largest-on-top or smallest-on-top.  We can also create heaps 
     with a maximum number of children of our choice.  As written, the default
     number of children is 3 and the default initial capacity is 5.  These
     parameters can be changed by the way we invoke the class constructor.
     
     The module also provides the efficient heap sort method.  By default, the
     methods sorts objects in increasing order.  But we can also sort objects
     in decreasing order.
     
     Our implementation works for objects of any class that understand the
     relational operators.

'''

testing = False
from person import Person
import math

def heapSort(aSequence, increasingOrder = True):
   '''  This method will answer a list of the elements of aSequence, which
     by default will be sorted in increasing order.  To sort in decreasing
     order, send a second parameter which is False.
   '''
   # Do last, after buildFrom() and siftDownFrom(), other methods.
   # More code needed!  Create a heap, h, ...
   #return h.elements[:]
   h = Heap(largestOnTop = increasingOrder)
   h.elements = h.buildFrom(aSequence) # Phase I
   #print(h.elements) prints elemetns with largest on to if it is else smallest on top
   
   heapSize = h.size
   #print("work!")
   #print(heapSize)
   while heapSize > 0: #phase II
      tempNode = h.elements[heapSize-1]
      h.elements[heapSize-1] = h.elements[0]
      h.elements[0] = tempNode       
      heapSize-= 1
      h.siftDownFrom(0)
      
   return h.elements[0:]



class Heap:
   '''
    The class Heap provides a generic heap abstract data type.
    The instances of this class can hold objects of any sort that
    understand the relational operators.  It also allows us to create
    heaps with any maximum number of children.
   '''
    
   DefaultCapacity = 5           #  A class variable
   DefaultNumberOfChildren = 3   #  Another class variable

   def __init__(self, capacity = DefaultCapacity,
            largestOnTop = True, numberOfChildren =
                DefaultNumberOfChildren):
      self.size = 0
      self.capacity = capacity
      self.largestOnTop = largestOnTop
      self.elements = [None]*capacity
      self.maxChildren = numberOfChildren

   def __str__(self): # is required when the string representation of object is needed
      if self.largestOnTop:
         sortOfHeap = 'largest on top'
      else:
         sortOfHeap = 'smallest on top'
      st = 'It is a ' + sortOfHeap + ' heap:\n'+ 'The size of the heap is '+ str(self.size)+'.\n'+'The capacity of the heap is '+ str(self.capacity) + '.\n' + 'The elements of the heap are: '+ '\n' + str(self.elements[0:self.size]) +'\n'
       
      return st

   def addToHeap(self,newObject):
      '''If the heap is full, double its current capacity.
         Add the newObject to the heap, maintaining it as a
         heap of the same type.  Answer newObject.
      '''
      if self.size == self.capacity:
            tempList=[None]*(2*len(self.elements))#doubling the capacity of the original elementList capacity
            self.capacity=len(tempList)
            for i in range(self.size):# range is from 0 to (size-1)
               tempList[i]=self.elements[i]
            self.elements=tempList
            
      self.elements[self.size]=newObject
      self.siftUpFrom(self.size)
      self.size+=1  
      #return self.elements
      pass  # Allows compilation of file.  Replace with actual code.

   def bestChildOf(self, index, lastIndex):
      ''' Answer the index of the "best child" of self.elements[index], if it
        exists. If not, answer None.  lastIndex is the index of the last 
        object in the heap.  For a largest on top heap, the best child is the
        largest child.  For a smallest on top heap, it is the smallest child
        of the node with the given index.
      '''
      bestChild = None
      curParentIndex = index
      firstChildIndex = (self.maxChildren*curParentIndex) + 1
      if firstChildIndex > lastIndex: # no children
         return None
      endIndex = (self.maxChildren*curParentIndex) + self.maxChildren # a tree with max children possible
      if lastIndex >= endIndex :# node 
         endIndex = endIndex
      else: 
         endIndex = lastIndex
      bestChild = firstChildIndex
      for childIndex in range(firstChildIndex+1, endIndex+1,1):
         if self.largestOnTop and self.elements[childIndex] > self.elements[bestChild]:
            bestChild = childIndex
         elif not self.largestOnTop and self.elements[childIndex] < self.elements[bestChild]:
            bestChild = childIndex
      #print(bestChild)
      return bestChild
              
   def buildFrom(self, aSequence):
      '''  Create a heap from the elements in aSequence. This method uses
         the siftDownFrom() method so it is O(len(aSequence)).
      '''
      self.elements = list(aSequence)
      #print(self.elements)
      self.size = self.capacity = len(aSequence)
      lastIndex = self.size - 1
      parentIndex = (lastIndex - 1) // self.maxChildren
      while parentIndex >= 0:
         self.siftDownFrom(parentIndex)
         parentIndex -= 1 #going to all previous nodes till the root node
      return self.elements # passing the values to the heapSort
   

   def removeTop(self):
      '''  If the heap is not empty, remove the top element
        of the heap and adjust the heap accordingly.  Answer the object
        removed.  If the heap is empty, return None.
      '''
      if self.size == 0:
         return None
      else:
         tempNode = self.elements[0]
         self.elements[0] = self.elements[self.size-1]
         self.size -= 1
         if self.size > 0:
            self.siftDownFrom(0)
      return tempNode
         
         

   def siftDownFrom(self, fromIndex ):
      '''fromIndex is the index of an element in the heap.
        Pre: elements[fromIndex..size-1] satisfies the heap condition,
        except perhaps for the element self.elements[fromIndex].
        Post:  That element is sifted down as far as neccessary to
        maintain the heap structure for elements[fromIndex..size-1].
      '''
      curParentIndex = fromIndex
      lastChildIndex = self.size -1
      bestChildIndex = self.bestChildOf(curParentIndex,lastChildIndex)
      #print(bestChildIndex)
      
      
      #while curParentIndex <= lastChildIndex and (bestChildIndex != None):
         #bestChildIndex = self.bestChildOf(curParentIndex,lastChildIndex)
     
      while curParentIndex <= lastChildIndex:
         if bestChildIndex == None:
            return         
         if self.largestOnTop and self.elements[bestChildIndex] > self.elements[curParentIndex]:
            tempNode=self.elements[curParentIndex]
            self.elements[curParentIndex] = self.elements[bestChildIndex]
            self.elements[bestChildIndex] = tempNode
            #print(tempNode)
            #self.siftDownFrom(bestChildIndex)# recursive call
            curParentIndex = bestChildIndex
            #bestChildIndex = self.bestChildOf(curParentIndex,lastChildIndex)
         if not self.largestOnTop and self.elements[bestChildIndex] < self.elements[curParentIndex]:
            tempNode=self.elements[curParentIndex]
            self.elements[curParentIndex] = self.elements[bestChildIndex]
            self.elements[bestChildIndex] = tempNode
            #print(tempNode)
            #self.siftDownFrom(bestChildIndex)# recursive call 
            curParentIndex = bestChildIndex
            #bestChildIndex = self.bestChildOf(curParentIndex,lastChildIndex)
         else:
               break
            
            
   
      #return self.elements
            
         

   def siftUpFrom(self, child):
      ''' child is the index of a node in the heap.  Sift that
      node up as far as necessary to ensure that the path satisfies
      the heap condition.
      '''
      childIndex = child
      parentIndex = (childIndex - 1)//self.maxChildren
      while parentIndex >= 0:
         if self.largestOnTop and self.elements[childIndex] > self.elements[parentIndex]:
            tempNode=self.elements[parentIndex]
            #print(tempNode)
            self.elements[parentIndex] = self.elements[childIndex]
            self.elements[childIndex] = tempNode
            #self.siftUpFrom(parentIndex) #recursive call of the siftUpFrom() for parent node
            childIndex = parentIndex
            parentIndex = (childIndex - 1)//self.maxChildren
            
         elif not self.largestOnTop and self.elements[childIndex] < self.elements[parentIndex]:
            tempNode=self.elements[childIndex]
            #print(tempNode)
            self.elements[parentIndex] = tempNode
            self.elements[childIndex] = self.elements[parentIndex]
            #self.siftUpFrom(childIndex)
            childIndex =parentIndex
            parentIndex = (childIndex - 1)//self.maxChildren
         else:
            break

         
     
      
   def levelByLevelString(self):
      ''' Return a string which lists the contents of the heap
         level by level.
      '''
      maxLevel = math.ceil(math.log(self.size*(self.maxChildren - 1) + 1)/
              math.log(self.maxChildren))
      index = 0
      st= []
      for i in range(int(maxLevel)):
         st.append('\nLevel '+str(i+1)+ ':'+'\n')
         nodeNum = pow(self.maxChildren,i)
         end = index + nodeNum
         #print(end)
         if end < self.size:
            end = end
         else:
            end = self.size
         for j in range(index, end):
            st.append(str(self.elements[j])+'\n')
         index = index + nodeNum
      return ''.join(st)
            
            
         
            
              

   #  Other methods?
   #  Use Doc strings for all methods!
        
def main():
   print("My name is DICHHA RAI ")
   h = Heap()
   h.addToHeap(20)
   h.addToHeap(40)
   h.addToHeap(-10)
   h.addToHeap(72)
   h.addToHeap(84)
   h.addToHeap(-100)
   h.addToHeap(54)
   h.addToHeap(66)
   h.addToHeap(99)
   h.addToHeap(1000)
   h.addToHeap(900)
   print(h)

   h.elements[0] = 50
   h.siftDownFrom(0)
   print(h)

   h.elements[0] = 60
   h.siftDownFrom(0)
   print(h)

   h = Heap(3, False)
   h.buildFrom((20,40,-10, 72, 84, -100, 54,66, 99))
   print("Output from buildFrom():" + "\n" + str(h))

   theList = heapSort([10, 30, -100, 50, 20, 30, -40,70, 5, 50])
   print(theList)

   theList = heapSort([10, 30, -100, 50, 20, 30, -40,70, 5, 50], False)
   print(theList)
    
   print( "\nThe following is the extra output that happens when we" )
   print( " create a heap that can have 5 children per node. \n" )
   heap = Heap(numberOfChildren = 5)
   heap.buildFrom((10, 20, -29, 16, 70, 30, 20, 100, 38, -293, \
     77, -19, -77, 230, 91, -230, -48, 23))
   print(heap)

   a = heapSort((10, 20, -29, 16, 70, 30, 20, 100, 38, -293, \
     77, -19, -77, 230, 91, -230, -48, 23))
   print(a)


   #  Extra stuff to test removeTop()
   h = Heap()
   h.addToHeap(20)
   h.addToHeap(40)
   h.addToHeap(-10)
   h.addToHeap(72)
   h.addToHeap(84)
   h.addToHeap(-100)
   h.addToHeap(54)
   h.addToHeap(66)
   h.addToHeap(99)
   h.addToHeap(1000)
   h.addToHeap(900)
   print(h)

   print("Output from removeTop(): "+ "\n" + str(h.removeTop()))
   print(h)

   print( "trying heapSort method:" )
   print( heapSort((20, -30, 45, 921, 37, 200, -1000, 4000, 57)) )
   print(  heapSort((20, -30, 45, 921, 37, 200, -1000, 4000, 57), False))
   joe = Person('Joe', 99)
   jill = Person('Jill', 200)
   walt = Person('Walter', 3000)
   dave = Person('David', 23)
   kent = Person('Kent', 220)
   alan = Person('Al', 110)
   folks = [joe, jill, walt, dave, kent, alan]
   print( heapSort(folks) )
   print( heapSort(folks, False ))
   
   h = Heap()
   h.addToHeap(20)
   h.addToHeap(40)
   h.addToHeap(-10)
   h.addToHeap(72)
   h.addToHeap(84)
   h.addToHeap(-100)
   h.addToHeap(54)
   h.addToHeap(66)
   h.addToHeap(99)
   h.addToHeap(1000)
   h.addToHeap(900)
   print()
   print( 'A level by level listing of the heap:' )
   print( h.levelByLevelString() )


if __name__ == '__main__': main()

'''  The following is the output from running this code:
My name is YOUR NAME
[evaluate heap.py]
It is a largest on top heap:
The size of the heap is 11.
The capacity of the heap is 20.
The elements of the heap are: 
1000
72
99
900
20
-100
54
-10
66
84
40

It is a largest on top heap:
The size of the heap is 11.
The capacity of the heap is 20.
The elements of the heap are: 
900
72
99
50
20
-100
54
-10
66
84
40

It is a largest on top heap:
The size of the heap is 11.
The capacity of the heap is 20.
The elements of the heap are: 
99
72
84
50
20
-100
54
-10
66
60
40

Output from buildFrom():
It is a smallest on top heap:
The size of the heap is 9.
The capacity of the heap is 9.
The elements of the heap are: 
-100
20
-10
72
84
40
54
66
99

[-100, -40, 5, 10, 20, 30, 30, 50, 50, 70]
[70, 50, 50, 30, 30, 20, 10, 5, -40, -100]

The following is the extra output that happens when we
 create a heap that can have 5 children per node. 

It is a largest on top heap:
The size of the heap is 18.
The capacity of the heap is 18.
The elements of the heap are: 
230
100
91
23
70
30
20
20
38
-293
77
-19
-77
-29
10
-230
-48
16

[-293, -230, -77, -48, -29, -19, 10, 16, 20, 20, 23, 30, 38, 70, 77, 91, 100, 230]
It is a largest on top heap:
The size of the heap is 11.
The capacity of the heap is 20.
The elements of the heap are: 
1000
72
99
900
20
-100
54
-10
66
84
40

Output from removeTop():
1000
It is a largest on top heap:
The size of the heap is 10.
The capacity of the heap is 20.
The elements of the heap are: 
900
72
99
40
20
-100
54
-10
66
84

trying heapSort method:
[-1000, -30, 20, 37, 45, 57, 200, 921, 4000]
[4000, 921, 200, 57, 45, 37, 20, -30, -1000]
[Name: David Id: 23 , Name: Joe Id: 99 , Name: Al Id: 110 , Name: Jill Id: 200 , Name: Kent Id: 220 , Name: Walter Id: 3000 ]
[Name: Walter Id: 3000 , Name: Kent Id: 220 , Name: Jill Id: 200 , Name: Al Id: 110 , Name: Joe Id: 99 , Name: David Id: 23 ]

A level by level listing of the heap:
Level 1:
1000

Level 2:
72
99
900

Level 3:
20
-100
54
-10
66
84
40

'''
