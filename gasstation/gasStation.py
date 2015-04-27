#during my solution, is used static methods,
#because i wouldn't need of an object instance of "Gas Station" class.
#I broke this problem in small methods for to be possible easy change
#in future, and for exists an easy read.
#i used "try" and "except" on the danger parts of my code, for to treat user errors or errors in the file.
#In my solution i use two pointers, one is the current position, and another is  the next position. First i add the
#'g'(amount of gallons in the station) and the amount of gallons that i have, after i subtract the 'c'(amount of gallons
#for to go to this state) of 'g', and i verify if this is more then 0, if true, i can to continue, if false, i increment
#1 for each pointer and i repeat the test. During my tests i use one counter, it help me for to know if in the end the route
#is completed. For simulate the circular route, i use a schema where, if my current pointer is the last position in array, the
#next pointer will be the first position in array.
#---------------------------------------------------------------This class get the file and make a array with the possible routes and return the result
class GasStation(object):
    minRouteLength = 2#minimum size for the routes
    errors = {"wrongRoute":"This rounte is wrong","emptyLine":"This line is Empty","indexError":"This route contains a wrong information! it should be like this (g:c)!","emptyFile":"The file is empty!","numberError":"The route not should contains letters!","ioErrorMensage" : "Error reading file! Try again, and check if the file is correct!", "lengthError" : "This array has a wrong length! Or a length smallest of the permitted."}
    #-----------------------------------------------------------This method get the request of page and it make the result using another class methods
    @staticmethod
    def putFile(request):
        try:
            input_file = request.POST['gasFile'].file
            lines = input_file.readlines()
        except IOError:#------------------------------------------If the imput file to has a error, my code returns a mensage with an information about the error
            return GasStation.errors["ioErrorMensage"]
        if(len(lines) <= 0 ):#--------------------------------If the file is empty my code returns this information for to be displayed on the page
            return GasStation.errors["emptyFile"]
        result = GasStation.makeResult(lines)
        return result
    #------------------------------------------------------------This method mounts the string result for be displayed in the page
    @staticmethod
    def makeResult(lines):
        separator = ','
        result = []
        for line in lines:
            if(separator not in line):
                result.append(GasStation.errors["wrongRoute"])
            else:
                info = line.split(',')
                sizeOfEmptyLine = 1
                if(info == []):
                    result.append(GasStation.errors["emptyLine"])
                else:
                    gasStationReturn = GasStation.gasStation(info)
                    result.append(gasStationReturn)
        if(not GasStation.isWrongFile(result)):
            return GasStation.makeHTMLResult(result)
        return GasStation.errors["ioErrorMensage"]
    #----------------------------------------------------------------This method mounts HTML string result for be displayed in the page
    @staticmethod
    def makeHTMLResult(array):
        result = ''
        for element in array:
            result += element+"<br>"
        return result
    #----------------------------------------------------------------This method verifies if all results are wrong, if true, it returns a message with this information
    @staticmethod
    def isWrongFile(array):
        for element in array:
            if(element not in GasStation.errors.values()):
                return False
        return True
    #-------------------------------------------------------------This method receives one string array and processes
    @staticmethod
    def gasStation(strArr):
        if(strArr[0] == ""):
            return GasStation.errors["lengthError"]
        try:
            length = int(strArr[0])
        except ValueError:
            return GasStation.errors["wrongRoute"]
        if(length < GasStation.minRouteLength or length != (len(strArr)-1)):
            return GasStation.errors["lengthError"]
        routes = []
        for i in range(1,length+1):
            try:
                resultOfRoute = GasStation.process(strArr,length,i)
            except IndexError:
                return GasStation.errors["indexError"]
            if(resultOfRoute != 0):
                routes.append(resultOfRoute)
        if(len(routes) > 0):
            return(str(min(routes)))
        return "impossible"
    #--------------------------------------------------------------------This method receives one state ['g','c'] and return one state [x,y] where x,y are numbers
    @staticmethod
    def castState(state):
    	array = []
	for i in state:
            array.append(int(i))
        return array
    #----------------------------------------------------------------------This method return the smallest index for a circular route
    @staticmethod
    def process(strArr,length,currentIndex):
        rounds = length
        currentIndex = currentIndex
        if(currentIndex == length):
            nextIndex = 1
        else:
            nextIndex = currentIndex+1
        gallons = 0
        while(rounds > 0):
            try:
                currentStation = GasStation.castState(strArr[currentIndex].split(':'))
                nextStation = GasStation.castState(strArr[nextIndex].split(':'))
            except ValueError:
                return GasStation.errors["numberError"]
            if((currentStation[0]+gallons)- currentStation[1]>=0):
                gallons+=currentStation[0]-currentStation[1]
                if(gallons+nextStation[0] >= nextStation[1]):
                    if(currentIndex >= length):
                        currentIndex = 1
                        nextIndex = currentIndex+1
                    elif(nextIndex >= length):
                        nextIndex = 1
                        currentIndex += 1
                    else:
                        currentIndex += 1
                        nextIndex = currentIndex+1
                else:
                    return 0
            else:
                return 0
            rounds-=1
	return currentIndex
