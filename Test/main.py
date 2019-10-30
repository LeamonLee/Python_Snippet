def Func1(sidebar_list=list()):
    sidebar_list.append("test")
    sidebar_list.append("test")
    return sidebar_list

def Func2():
    myList = list()
    myList = Func1()
    # myList = Func1(myList)      # different result
    print(len(myList))

if __name__ == "__main__":
    
    # Func2()
    # Func2()
    # Func2()
    myList = list()
    myList = Func1()
    print(len(myList))

    myList = list()
    myList = Func1()
    print(len(myList))

    myList = list()
    myList = Func1()
    print(len(myList))
