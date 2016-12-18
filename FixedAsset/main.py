import time
from FixedAsset import FixedAssets

def main():

    print "step"
    streetBinsClassInstance = FixedAssets()

    print "step2"
    streetBinsClassInstance.generateToken()

    print "step3"
    numberOfAssets = streetBinsClassInstance.returnAllObjectId()
    streetBinsClassInstance.resetFixedAsset(numberOfAssets)

    dayInt = time.strftime("%w")
    print "Setting the next day using {0} value".format(dayInt)
    streetBinsClassInstance.prepDay(dayInt)
    print("helloWorld - well done")
    
    
if __name__ == "__main__":
    main()
