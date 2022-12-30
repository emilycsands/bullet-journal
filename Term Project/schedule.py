from cmu_112_graphics import *
from event import *
from datetime import timedelta
import datetime
import math

################################ Self Scheduler ################################
# returns True if the date of date1 and date2 are equal and False otherwise
def datesAreEqual(date1, date2):
    if (date1.year == date2.year) and (date1.month == date2.month) and (date1.day == date2.day):
        return True
    else: return False

# returns False if the possible time block and the free time blocks don't
# overlap and returns a tuple of the time bounds for the free time block 
def isWithinStartAndEndDate(freeTimeStart, freeTimeEnd, possBlockStart, possBlockEnd):
    if (freeTimeStart == None) and (freeTimeEnd == None):
        return (None, None)
    elif (freeTimeStart == None):
        if (freeTimeEnd <= possBlockStart):
            return False
        elif (datesAreEqual(freeTimeEnd, possBlockStart)):
            newStart = freeTimeEnd.replace(hour=0, minute=0)
            return (newStart, freeTimeEnd)
        else:
            return (possBlockStart, possBlockEnd)
    elif (freeTimeEnd == None):
        if (possBlockEnd <= freeTimeStart):
            return False
        elif (datesAreEqual(possBlockEnd, freeTimeStart)):
            newEnd = freeTimeStart + datetime.timedelta(days=1)
            newEnd = newEnd.replace(hour=0, minute=0)
            return (freeTimeStart, newEnd)
        else:
            return (possBlockStart, possBlockEnd)
    else:
        if (possBlockEnd <= freeTimeStart) or (freeTimeEnd <= possBlockStart):
            return False
        elif (datesAreEqual(freeTimeStart, freeTimeEnd)) and (datesAreEqual(freeTimeStart, possBlockStart)):
            return (freeTimeStart, freeTimeEnd)
        elif (datesAreEqual(freeTimeEnd, possBlockStart)):
            newStart = freeTimeEnd.replace(hour=0, minute=0)
            return (newStart, freeTimeEnd)
        elif (datesAreEqual(possBlockEnd, freeTimeStart)):
            newEnd = freeTimeStart + datetime.timedelta(days=1)
            newEnd = newEnd.replace(hour=0, minute=0)
            return (freeTimeStart, newEnd)
        else:
            return (possBlockStart, possBlockEnd)
    
# returns False if the event to add cannot be scheduled within the given free
# time and possible time block. Otherwise, it returns a tuple of the start and
# end time in which the event could be scheduled.
def isLegal(eventToAdd, freeTimeStart, freeTimeEnd, possBlockStart, possBlockEnd):
    bounds = isWithinStartAndEndDate(freeTimeStart, freeTimeEnd, possBlockStart, possBlockEnd)
    if (bounds == False):
        return False
    start, end = bounds

    duration = eventToAdd.duration
    if (start == None) and (end == None):
        return (possBlockStart, possBlockEnd)

    elif (start <= possBlockStart < possBlockEnd <= end):
        return (possBlockStart, possBlockEnd)

    elif (possBlockStart <= start <= end <= possBlockEnd):
        if (duration <= end-start):
            return (start, end)
        else: return False

    elif (possBlockStart <= start <= possBlockEnd <= end):
        if (duration <= possBlockEnd - start):
            return (start, possBlockEnd)
        else: return False

    elif (start <= possBlockStart <= end <= possBlockEnd):
        if (duration <= end - possBlockStart):
            return (possBlockStart, end)
        else: return False

    else:
        return False

# uses back tracking to try and schedule all the events which need to be added
def selfSchedule(allEventsToAdd, iInNumEventsAdded):
    if (iInNumEventsAdded < 0):
        return 'Found Solution'
    else:
        eventToAdd = allEventsToAdd[iInNumEventsAdded]
        for (freeTimeStart, freeTimeEnd) in Event.freeTimeBlocks:
            for (possBlockStart, possBlockEnd) in eventToAdd.possibleBlocks:
                legal = isLegal(eventToAdd, freeTimeStart, freeTimeEnd, possBlockStart, possBlockEnd)
                if (legal != False):
                    oldFreeTimBlocks = copy.copy(Event.freeTimeBlocks)
                    start, end = legal
                    newStart, newEnd = start, start + eventToAdd.duration
                    eventAdded = Event(eventToAdd.name, newStart.year,
                                    newStart.month, newStart.day,
                                    newStart.hour, newStart.minute, newEnd.year,
                                    newEnd.month, newEnd.day, newEnd.hour, newEnd.minute,
                                    location=eventToAdd.location, notes=eventToAdd.notes)
                    solution = selfSchedule(allEventsToAdd, iInNumEventsAdded-1)
                    if (solution != None):
                        return solution
                    else:
                        Event.allEvents.remove(eventAdded)
                        Event.freeTimeBlocks = copy.copy(oldFreeTimBlocks)
        return None