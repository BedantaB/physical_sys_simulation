def heapify(arr,i,length,dicti):
    smallest = i
    left = 2*i
    right = 2*i + 1

    if(left <= length):
        if arr[left][1] < arr[smallest][1]:
            smallest = left
        elif arr[left][1] == arr[smallest][1] and arr[left][0] < arr[smallest][0]:
            smallest = left
    
    if(right <= length):
        if arr[right][1] < arr[smallest][1]:
            smallest = right
        elif arr[right][1] == arr[smallest][1] and arr[right][0] < arr[smallest][0]:
            smallest = right


    if i != smallest:
        a = arr[smallest]
        arr[smallest] = arr[i]
        arr[i] = a

        theta = dicti[arr[smallest][0]]
        dicti[arr[smallest][0]] = dicti[arr[i][0]]
        dicti[arr[i][0]] = theta


        heapify(arr,smallest,length,dicti)


def buildHeap(arr,length,dicti):
    i = length//2
    while(i > 0):
        heapify(arr,i,length,dicti)
        i -= 1


class heap:

    def __init__(self,arr,length):

        #arr has elements of type tuple (index , time)
        self.heapList = arr

        self.dicti = []
        for i in range(0,length + 1):
            self.dicti.append(i)

        #length of arr - 1
        self.heapLength = length

        buildHeap(self.heapList,length,self.dicti)



    def heapUp(self,i):
        me = self.dicti[i]
        while(me > 1):
            parent = me//2
            if self.heapList[me][1] < self.heapList[parent][1] or ((self.heapList[me][1] == self.heapList[parent][1])and(self.heapList[me][0] < self.heapList[parent][0])):
                a = self.heapList[me]
                self.heapList[me] = self.heapList[parent]
                self.heapList[parent] = a

                theta = self.dicti[self.heapList[me][0]]
                self.dicti[self.heapList[me][0]] = self.dicti[self.heapList[parent][0]]
                self.dicti[self.heapList[parent][0]] = theta

                me = me//2
            else:
                break

    def changeTime(self,i,newt,loc):
        location = self.dicti[i]
        self.heapList[location] = (i,newt,loc)


    def heapDown(self,i):
        heapify(self.heapList,self.dicti[i],self.heapLength,self.dicti)

    def extractMean(self):
        minTup = self.heapList[1]

        theta = self.dicti[minTup[0]]
        self.dicti[minTup[0]] = self.dicti[self.heapList[self.heapLength][0]]
        self.dicti[self.heapList[self.heapLength][0]] = theta

        self.heapList[1] = self.heapList[self.heapLength]
        self.heapList[self.heapLength] = (minTup[0],float("inf"),float("inf"))

        heapify(self.heapList,1,self.heapLength,self.dicti)
        return minTup

    def printHeap(self):
        print(self.heapList)

    def printdicti(self):
        print(self.dicti)

# ar = [-1,(1,5),(2,3),(3,6),(4,3),(5,9),(6,2),(7,1)]
# myh = heap(ar,7)
# # myh.printHeap()
# # print(myh.dicti[7])
# # myh.changeTime(7,100)
# # myh.heapDown(7)
# # print(myh.dicti[7])
# print(myh.extractMean())
# myh.printHeap()
# myh.printdicti()


def listCollisions(M,X,V,m,T):
    collisions = []
    totalT = 0
    heapln = len(M) - 1
    arr = [-1]
    for i in range(1,heapln+1):
        try:
            time = ((X[i] - X[i-1])/(V[i-1] - V[i]))
        except:
            time = float("inf")

        if time > 0:
            try:
                arr.append((i,time,(X[i-1]+(V[i-1])*abs(((X[i] - X[i-1])/(V[i] - V[i-1]))))))
            except:
                arr.append((i,time,float("inf")))
        else:
            try:
                arr.append((i,float("inf"),(X[i-1]+(V[i-1])*abs(((X[i] - X[i-1])/(V[i] - V[i-1]))))))
            except:
                arr.append(i,float("inf"),float("inf"))


    myHeap = heap(arr,heapln)
    # print(myHeap.heapList)
    timels = [0]*(heapln+1)


    while(len(collisions)<m and totalT < T):
        # print(myHeap.heapList)
        # print(timels)
        # print(X)
        coll = myHeap.extractMean()
        totalT = coll[1]
        index = coll[0]
        timels[index] = totalT
        timels[index - 1] = totalT

        location = coll[2]
        X[index - 1] = location
        X[index] = location

        u1 = V[index-1]
        u2 = V[index]
        V[index - 1] = ((M[index-1]-M[index])*u1 + 2*M[index]*u2)/(M[index-1] + M[index])
        V[index] = ((M[index]-M[index-1])*u2 + 2*M[index-1]*u1)/(M[index-1] + M[index])

        if index - 1 > 0:
            newX = X[index - 2] + V[index - 2]*(totalT - timels[index - 2])
            try:
                newT = (X[index - 1] - newX)/(V[index-2] - V[index - 1])
            except:
                newT = float("inf")

            if newT < 0:
                newT = float("inf")

            newL = newX + V[index -2]*(newT)

            myHeap.changeTime(index - 1,newT + totalT,newL)
            myHeap.heapUp(index - 1)

        if index + 1 <= heapln:
            newX = X[index + 1] + V[index + 1]*(totalT - timels[index + 1])

            try:
                newT = (newX - X[index])/(V[index] - V[index+1])
            except:
                newT = float("inf")

            if newT < 0:
                newT = float("inf")

            newL = newX + V[index+1]*(newT)

            myHeap.changeTime(index + 1,newT + totalT,newL)
            myHeap.heapUp(index + 1)


        if totalT > T or (totalT == float("inf")):
            break
        collisions.append((round(totalT,4),index-1,round(location,4)))

    return collisions

# print(listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5,
# 5.0))