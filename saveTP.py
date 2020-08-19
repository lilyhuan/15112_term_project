#file for saving textbox data into a txt file
# datetime module information from https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
def saveFile(thingToSave, listLevel=0):
    result = ""
    if type(thingToSave) == list:
        if listLevel == 1: #1d list, textBoxes
            for elem in thingToSave:
                time = elem.timeStamp
                if len(str(time.minute)) == 1:
                    minute = "0"+str(time.minute)
                else:
                    minute = time.minute
                result += "On %d/%d/%d, at %d:%d, you wrote: \t" %(time.month, time.day, time.year, time.hour, minute)
                result += str(elem.typedText) + "\n"
    return result