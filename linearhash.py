'''
  File: linearhash.py (As saved from linearhash.shell.)
  Author: Steve Hubbard and 
  Date: 10/2/14
  Description: This file defines a class, LinearHashTable, which 
    implements linear probing.  Instances of any class may be elements 
    of such a hash table if hash(anObject) and anObject == otherObject make
    sense.  If a == b, then it must be true that hash(a) == hash(b).
'''

from copy import deepcopy
from person import Person, Student

class LinearHashTable:
   def __init__(self, tableSize = 10, empty = -1, deleted = -2):
      self.tableSize = tableSize
      self.table = [empty]*tableSize
      self.empty = empty
      self.deleted = deleted


   def __str__(self):
      me = 'The size of the hash table is ' + \
             str(self.tableSize) + '\n'
      for index in range(len(self.table)):
          if self.table[index] != self.empty:
              me += str(index) + ': ' + \
                    str(self.table[index])+ '\n'
      return me

   def hash(self, anObject):
      return hash(anObject) % self.tableSize

   def _isPrime_(self, anInt):
      '''Answer True iff anInt is a prime integer.'''
      prime = True
      for x in range(2, anInt // 2 + 1):
         if (anInt % x == 0):
            prime = False
      return prime
    

   def search(self, item):
      '''
        This method returns a tuple (a,b).
        Case 1:  If we find a match, a is True and b is
          the index of the matching item.
        Case 2: If we do not find a match for item, a is False.
          If we encounter a deleted slot, b is the index of the
          first deleted slot. If we do not encounter a deleted slot
          but do encounter an empty slot, b is the index of the
          first emtpy slot. If we have a full table with no empty
          or deleted slots, b is negative.  In case 2, location (b) is
          the index of the slot where the object belongs, if there
          is room.
      '''
      #print(self.tableSize)
      found=False;
      count=0
      firstDeletedIndex=None
      deletedSlotFound=False
      location=None
      #print("check")
      #print(item)
      
      for i in range(0,self.tableSize,1):
         if (self.table[i]==item): #and hash(self.table[i])==hash(item)):
            #print("tableContent")
            #print(self.table[i])
            #print(hash(self.table[i]))
            #print("check checl")
            #print(item)
            #print(hash(item))
            found = True
            location = i
            break
      
      for i in range(0,self.tableSize,1):#loop for counting the number of free slots
         if (self.table[i]== self.empty or self.table[i]== self.deleted):#replaced == -1 to self.empty and -2 to self.deleted, works!
            count+=1
      
      if count>0:
         if not found:
            location= self.hash(item)
            
            if (self.table[location] == self.empty):
              # print("checking if empty is working")
              # print(self.table[location] == -1)#gives correct answer of true once only before 11
               location= location
            
               
            elif (location !=(self.tableSize-1)):#for the item not in the last index
               #print("location")
               #print(self.hash(item))
               #print(self.tableSize-1)
               location+=1
               for i in range(location,self.tableSize,1):
                  if (self.table[i] == self.empty): #checking if there is an empty slot
                     location = i
                                   
                     break
                  elif (self.table[i] == self.deleted):#cheking if there is any deleted slot
                     firstDeletedIndex=i
                     deletedSlotFound=True
                     location = i                 
                     break 
                  if(location == self.hash(item)):#to see if circular search is required since location did not changed after searching for free or deleted slot till the end of table index
                     for i in range(0,location,1):#looking for an empty slot and deleted slot simultaneously
                        if self.table[i] == self.empty:
                           location = i                       
                           break               
                        if (self.table[i] == self.deleted):
                           firstDeletedIndex=i
                           deletedSlotFound=True
                           location=i                       
                           break
                                 
            elif (location == (self.tableSize-1) and self.table[location]!= self.empty):#cheking if an item has location of an end of index and is not free
               for i in range(0,self.tableSize,1):#looking for an empty slot and deleted slot simultaneously
                  if self.table[i] == self.empty:
                     location = i                  
                     break  
                  elif (self.table[i] == self.deleted):
                     firstDeletedIndex=i
                     deletedSlotFound=True
                     location =i
                     break
            #else:
               #location= -1
      if(count==0 and found==False):#special case for table being full and not finding the item
         location = -1
      return(found,location)
   
   def inc(self,item):
      
      add=(hash(item)//self.tableSize)%self.tableSize
      #print("checkPls")
      #print(add)
      #print("check check")
      if (add >0):
         return add
      else:
         return 1
   def getNext(self,increment,item):
      found=False
      newLocation=None
      #print("hello")
      #print(increment)
      #print(item) # prints correctly
      location=self.hash(item)
      #print(location)prints 3s 3 times correct
      while not found:
         newLocation=location+increment
         location=(newLocation)%self.tableSize
         if((self.table[location]==self.empty)or(self.table[location]==self.deleted)):
            location=location
            found=True
         else:
            location=newLocation
            #print("check")
            #print(location)
      return location
            
         
      
   def insert(self, item):
      ''' Answer None if the method fails.  Otherwise we inserted
          a deep copy of item in the correct location and answer item.
      '''
      #print("tableSize for LinearQHashTable")
      #print(self.tableSize)
      #print("checking")
      count=0
      for i in range(0,self.tableSize,1):#to see that more item is not inserted then the tableSize
         if((self.table[i] == self.empty) or (self.table[i]==self.deleted)):
            count+=1;
            
         
         
      if(count>0):      
         location=self.hash(item)
         if ((self.table[location]==self.empty) or (self.table[location]==self.deleted)):
            self.table[location]= deepcopy(item)
            
         else:
            increment =self.inc(item)
            #print("hello")
            #print(increment)prints correctly
            nextInputSlot=self.getNext(increment,item)
            self.table[nextInputSlot]=deepcopy(item)
            
         
                      
         
         
      
            
      
   def delete(self, item):
      ''' Answer None if the method fails.  Otherwise we answer the
           corresponding entry in the hash table, and mark the slot as
           deleted.
      '''
      itemDeleteIndex=self.search(item)
      
      #print(itemDeleteIndex) #prints correct :-)
      if (itemDeleteIndex[0] == True):
         self.table[itemDeleteIndex[1]]=self.deleted
         return self.table[itemDeleteIndex[1]]
      else:
         return None
         
      
      

   def retrieve(self, item):
      ''' Answer None if the method fails.  Otherwise answer a deep
            copy of the corresponding entry of the table.
      '''
      #print("check")
      #print(item)
      location=self.hash(item)
      if(self.table[location]==item):#may require search if not found in the home address
         return self.table[location]
      else:
         return None
      
            
            

   def update(self, newItem):
      ''' Answer None if the method fails.  Otherwise we inserted
          a deep copy of item in the correct location and answer newItem.
      '''
      #print("check")
      #print(newItem)
      presence=self.search(newItem)
      #print(presence) correct
      if (presence[0]==True):
         self.table[presence[1]]= deepcopy(newItem)
         return self.table[presence[1]]
      else:
         return None

      ''' I used two more methods. '''
class LinearQHashTable(LinearHashTable):
   def __init__(self,tableSize=10,empty=-1,deleted=-2):
      LinearHashTable.__init__(self,tableSize,empty,deleted)
      self.tableSize=tableSize
      
      prime=True
      for x in range(2,self.tableSize//2+1):
         if(self.tableSize%x==0):
            prime =False
            print("Invalid table  size of "+str(self.tableSize)+" -- not a prime")
            break
   
   
      

class ExtendedQHashTable(LinearQHashTable):
   def __init__(self,tableSize,empty=-1,deleted=-2):
      LinearHashTable.__init__(self,tableSize,empty,deleted)
      self.tableSize=tableSize
      for k in range(0,(self.tableSize)):# for finding max k size
         if ((4*k)+3 ==self.tableSize):
            break
      else:
         print("Need a prime table size of the form 4*k+3, not "+str(self.tableSize))
   def incNewLoc(self,item):
      i=1 #for increment in square form ofIntegers 
      #print(item)
      location=self.hash(item)
      found=False
      while not found:
         nextStep= (((i+1)//2)**2)*(-1)**(i+1)
         #print("nextStep")
         #print(nextStep)
         nextLocation=(location+nextStep)%self.tableSize
         #print(nextLocation)
         
         if ((self.table[nextLocation]==self.empty) or self.table[nextLocation]==self.deleted):#or (self.table[nextLocation]==self.deleted)
            location = nextLocation
            #print("check")
            #print(location)
            found=True
         else:
            i+=1
            found=False
            location=location
      return location
         
         
   def insert(self,item):
      ''' Answer None if the method fails. Otherwise we inserted a deep copy of item in the correct location and answer item'''
      #print("item for EQHT")
      #print(item) prints in the format Name:x Id:y gpa:z 
      count=0
      for i in range(0,self.tableSize,1):#to see that more item is not inserted then the tableSize
         if((self.table[i] == self.empty) or (self.table[i]==self.deleted)):
            count+=1;
            
         
         
      if(count>0):   
         location=self.hash(item)
         #print(location)
         newInsertedItem=None
         if self.table[location]==self.empty:
            self.table[location]=deepcopy(item)
         else:
            newLoc= self.incNewLoc(item)
            #print("check new Location")
            #print(newLoc)
            self.table[newLoc]=deepcopy(item)
            newInsertedItem=self.table[newLoc]
         return newInsertedItem
         #print(self.table[newLoc])
   #def search(self,item):
      #for i in range
      
        
         
   def delete(self, item):
         ''' Answer None if the method fails.  Otherwise we answer the
              #corresponding entry in the hash table, and mark the slot as
              #deleted.
         '''
         #print(item)
         itemDeleteIndex=self.search(item)
         #print("hello check")
         #print(itemDeleteIndex) #prints correct :-)
         if (itemDeleteIndex[0] == True):
            originalEntry=self.table[itemDeleteIndex[1]]
            self.table[itemDeleteIndex[1]]=self.deleted
            #return self.table[itemDeleteIndex[1]]
            return originalEntry
         else:
            return None 
         
         
   
def main():
    print("My name is Dichha Rai")
    print("Linear hashing:")
    h = LinearHashTable(5)
    h.table[0] = h.deleted
    h.table[2] = 7
    h.table[3] = h.deleted
    h.table[4] = 17
    print( h.search(17) ) # Should be (True, 4)
    print( h.search(22) ) # Should be (False, 3)
    print( h.search(11) ) # Should be (False, 1)
    print( h.search(19) ) # Should be (False, 0)
    h.table[0] =  19
    h.table[1] =  11
    h.table[3] =  22
    #print("hello")
    #print(h) #prints the hash table
    print( h.search(72) ) # Should be something like (False, -1)
    print( h )
    
    print("Run 1:")
    print("Linear quotient hashing:")
    h = LinearQHashTable(7)
    h.insert(10)
    h.insert(12)
    h.insert(17)
    h.insert(24)
    h.insert(18)
    h.insert(31)
    h.insert(38)
    h.insert(45)
    h.insert(52)
    print(h)
    h.delete(24)
    print(h)
    h.insert(5)
    print(h)
    h = LinearQHashTable(70, -3)
    print("Run 2:")
    table = LinearQHashTable(5, empty = 'Nothing!', deleted = 'Gone!')
    table.insert(Person('Joe', 15))
    table.insert(Person('Jill', 3))
    table.insert(Person('Bill', 1))
    table.insert(Person('Maude', 19))
    table.delete(Person(" ", 3))
    print (table)
    #print("checking for Friend Lennie")
    table.insert(Person('Lennie', 23))
    print (table)
    print (table.retrieve(Person(" ",19)))
    print (table.retrieve(Person(" ",45)))
    #print("checking for Billy Joe Bob")
    print (table.update(Person('Billy Joe Bob', 1)))
    print (table.update(Person('Susie', 45)))
    print (table)
    
    print("Run 3:")
    table = ExtendedQHashTable(7)
    table.insert(Student('Joe', 15, 3.3))
    table.insert(Student('Jill', 3, 4.0))
    table.insert(Student('Bill', 1,2.99))
    table.insert(Student('Maude', 19, 0))
    #print("insert check")
    #print(table) #prints correct
    print (table.delete(Student(" ",3,0)))
    print (table.insert(Student('Lennie', 23, 3.87)))
    print (table)
    print (table.retrieve(Student(" ",19, 2.0)))
    print (table.retrieve(Student(" ",45, 5)))
    print (table.update(Student('Billy Joe Bob', 1, 3)))
    print (table.update(Student('Susie', 45, 3.13)))
    print (table.delete(Student(" ",33, 4)))
    print (table.delete(Student(" ", 1, 5)))
    print (table)

    print("Run 4:")
    print("Extended quadratic hashing:")
    h = ExtendedQHashTable(7)
    #print("hello!")
    h.insert(10)
    h.insert(12)
    h.insert(17)
    h.insert(24)
    h.insert(18)
    h.insert(31)
    h.insert(38)
    h.insert(45)
    h.insert(52)
    print (h)    
    h.delete(24)
    print (h)
    h.insert(5)
    print (h)
    h = ExtendedQHashTable(8)
    h = ExtendedQHashTable(17)
    print("Run 5:")
    table = ExtendedQHashTable(7)
    table.insert(Person('Joe', 15))
    table.insert(Person('Jill', 3))
    table.insert(Person('Bill', 1))
    table.insert(Person('Maude', 19))
    print (table.delete(Person(" ",3)))
    print (table.insert(Person('Lennie', 23)))
    print (table)
    print (table.retrieve(Person(" ",19)))
    print (table.retrieve(Person(" ",45)))
    print (table.update(Person('Billy Joe Bob', 1)))
    print (table.update(Person('Susie', 45)))
    print (table.delete(Person(" ",33)))
    print (table.delete(Person(" ", 1)))
    print (table)
    
if __name__ == '__main__': main()
'''
[evaluate linearhash.py]
My name is Dichha Rai
Linear hashing:
(True, 4)
(False, 3)
(False, 1)
(False, 0)
(False, -1)
The size of the hash table is 5
0: 19
1: 11
2: 7
3: 22
4: 17

Linear quotient hashing:
The size of the hash table is 7
0: 17
1: 31
3: 10
4: 18
5: 12
6: 24

The size of the hash table is 7
0: 17
1: 31
3: 10
4: 18
5: 12
6: -2

The size of the hash table is 7
0: 17
1: 31
3: 10
4: 18
5: 12
6: 5

Invalid table size of 70 -- not a prime.
The size of the hash table is 5
0: Name: Joe Id: 15 
1: Name: Bill Id: 1 
3: Gone!
4: Name: Maude Id: 19 

The size of the hash table is 5
0: Name: Joe Id: 15 
1: Name: Bill Id: 1 
3: Name: Lennie Id: 23 
4: Name: Maude Id: 19 

Name: Maude Id: 19 
None
Name: Billy Joe Bob Id: 1 
None
The size of the hash table is 5
0: Name: Joe Id: 15 
1: Name: Billy Joe Bob Id: 1 
3: Name: Lennie Id: 23 
4: Name: Maude Id: 19 

None
Name: Lennie Id: 23 gpa: 3.87
The size of the hash table is 7
1: Name: Joe Id: 15 gpa: 3.3
2: Name: Bill Id: 1 gpa: 2.99
3: Name: Jill Id: 3 gpa: 4.0
5: Name: Maude Id: 19 gpa: 0
6: Name: Lennie Id: 23 gpa: 3.87

None
None
None
None
None
None
The size of the hash table is 7
1: Name: Joe Id: 15 gpa: 3.3
2: Name: Bill Id: 1 gpa: 2.99
3: Name: Jill Id: 3 gpa: 4.0
5: Name: Maude Id: 19 gpa: 0
6: Name: Lennie Id: 23 gpa: 3.87

Extended quadratic hashing:
The size of the hash table is 70
3: 3
10: 10
11: 11
17: 17
24: 24
31: 31

The size of the hash table is 70
3: 3
10: 10
11: 11
17: 17
24: -2
31: 31

The size of the hash table is 70
3: 3
10: 10
11: 11
17: 17
24: -2
31: 31
38: 38

Need a prime table size of the form 4*k + 3, not 8.
Need a prime table size of the form 4*k + 3, not 17.
Name: Jill Id: 3 
Name: Lennie Id: 23 
The size of the hash table is 7
1: Name: Joe Id: 15 
2: Name: Bill Id: 1 
3: Name: Lennie Id: 23 
5: Name: Maude Id: 19 

Name: Maude Id: 19 
None
Name: Billy Joe Bob Id: 1 
None
None
Name: Billy Joe Bob Id: 1 
The size of the hash table is 7
1: Name: Joe Id: 15 
2: -2
3: Name: Lennie Id: 23 
5: Name: Maude Id: 19 
'''
