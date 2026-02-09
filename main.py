def BubbleSort(x):
    n = len(x)
    for i in range(n-1):
        for j in range(n-i-1):
            if x[j] > x[j+1]:
                x[j], x[j+1] = x[j+1],x[j]
    return x

def InsertionSort(x):
    n = len(x)
    for i in range(1,n):
        insertIndex = i
        currentValue = x.pop(i)
        for j in range(i-1,-1,-1):
            if x[j] > currentValue:
                insertIndex = j
        x.insert(insertIndex, currentValue)
    return x

def SelectionSort(x):
    n = len(x)
    for i in range(n-1):
        minIndex = i
        for j in range(i+1,n):
            if x[j] < x[minIndex]:
                minIndex = j
        minValue = x.pop(minIndex)
        x.insert(i,minValue)
    return x

def MergeSort(x):
    def merge(left, right):  # This is part of the merge sort algorithm
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result
    if len(x) <= 1:
        return x

    mid = len(x) //2
    leftHalf = x[:mid]
    rightHalf = x[mid:]

    sortedLeft = MergeSort(leftHalf)
    sortedRight = MergeSort(rightHalf)

    return merge(sortedLeft,sortedRight)

def QuickSort(x,low=0,high=None):
    def partition(x, low, high):
        pivot = x[high]
        i = low - 1

        for j in range(low, high):
            if x[j] <= pivot:
                i += 1
                x[i], x[j] = x[j], x[i]
        x[i + 1], x[high] = x[high], x[i + 1]
        return i + 1
    if high is None:
        high = len(x) -1

    if low<high:
        pivotIndex = partition(x,low,high)
        QuickSort(x,low,pivotIndex-1)
        QuickSort(x,pivotIndex+1,high)
    return x

print("---List Sorter---")
lst = list(map(int, input("Enter all values in the list separated by spaces: ").split()))

print()
print("Which sorting algorithm do you want to use?")
print("1. Bubble Sort")
print("2. Insertion Sort")
print("3. Selection Sort")
print("4. Merge Sort")
print("5. Quick Sort")
print()
choice = int(input("Enter the number of your choice:  "))

sortingMethod = ""

if(choice == 1):
    sortingMethod = "Bubble Sort"
else:
    if(choice == 2):
        sortingMethod = "Insertion Sort"
    else:
        if(choice == 3):
            sortingMethod = "Selection Sort"
        else:
            if(choice == 4):
                sortingMethod = "Merge Sort"
            else:
                if(choice == 5):
                    sortingMethod = "Quick Sort"

print()
print("Please confirm you want to sort: ")
print("Values: " , lst)
print("Method: " , sortingMethod)
confirmation = input("Enter Y/N to proceed/cancel.")

if confirmation.lower() == "y":
    if(choice == 1):
        print(BubbleSort(lst))
    if (choice == 2):
        print(InsertionSort(lst))
    if (choice == 3):
        print(SelectionSort(lst))
    if (choice == 4):
        print(MergeSort(lst))
    if (choice == 5):
        print(QuickSort(lst))
else:
    raise Exception("Sorting Cancelled.")





