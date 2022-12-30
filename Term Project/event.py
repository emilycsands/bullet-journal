from cmu_112_graphics import *
from datetime import timedelta
import datetime
import math

################################# Event Class ##################################
class Event(object):

    allEvents = []
    freeTimeBlocks = [(None, None)]

    def __init__(self, name, startYear, startMonth, startDay, startHr, startMin,
                 endYear, endMonth, endDay, endHr, endMin, location=None, notes=None):
        self.name = name
        self.startDateAndTime = datetime.datetime(startYear, startMonth, startDay, startHr, startMin)
        self.endDateAndTime = datetime.datetime(endYear, endMonth, endDay, endHr, endMin)
        self.location = location
        self.notes = notes
        self.addEventToAllEvents(len(Event.allEvents)//2)

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return (isinstance(other, Event) and
                (self.name == other.name) and 
                (self.startDateAndTime == other.startDateAndTime) and 
                (self.endDateAndTime == other.endDateAndTime) and
                (self.location == other.location) and
                (self.notes == other.notes))

    def __lt__(self, other):
        return self.startDateAndTime < other.startDateAndTime

    def __gt__(self, other):
        return self.startDateAndTime > other.startDateAndTime
    
    def editName(self, newName):
        self.name = newName

    def editStartDateAndTime(self, newStartYear, newStartMonth, newStartDay, newStartHr, newStartMin):
        self.startDateAndTime = datetime.datetime(newStartYear, newStartMonth, newStartDay, newStartHr, newStartMin)

    def editEndDateAndTime(self, newEndYear, newEndMonth, newEndDay, newEndHr, newEndMin):
        self.endDateAndTime = datetime.datetime(newEndYear, newEndMonth, newEndDay, newEndHr, newEndMin)

    def editLocation(self, newLocation):
        self.location = newLocation

    def editNotes(self, newNotes):
        self.notes = newNotes
    
    def deleteEvent(self):
        indexInAllEvents = Event.allEvents.index(self)
        Event.allEvents.pop(indexInAllEvents)
        start1, end1 = Event.freeTimeBlocks.pop(indexInAllEvents)
        start2, end2 = Event.freeTimeBlocks.pop(indexInAllEvents)
        Event.freeTimeBlocks.insert(indexInAllEvents, (start1, end2))
    
    # Updates the free block intervals when a new event is added
    def createNewFreeBlocks(self, i, previous):
        if (len(Event.allEvents) <= i):
            newFreeBlock1Start = previous[0]
            newFreeBlock2End = previous[1]
        elif (i <= 0):
            newFreeBlock1Start = previous[0]
            newFreeBlock2End = previous[1]
        else:
            newFreeBlock1Start = previous[0]
            newFreeBlock2End = previous[1]
        newFreeBlock1End = self.startDateAndTime
        newFreeBlock2Start = self.endDateAndTime

        newFreeBlock1 = (newFreeBlock1Start, newFreeBlock1End)
        newFreeBlock2 = (newFreeBlock2Start, newFreeBlock2End)
        Event.freeTimeBlocks.insert(i, newFreeBlock1)
        Event.freeTimeBlocks.insert(i+1, newFreeBlock2)
    
    # adds the new event to it's appropriate location in allEvents based on
    # event's start times
    def addEventToAllEvents(self, i):
        Event.allEvents.append(self)
        Event.allEvents.sort()
        i = Event.allEvents.index(self)
        previous = Event.freeTimeBlocks.pop(i)
        self.createNewFreeBlocks(i, previous)

############################### Add Event Class ################################
class AddEvent(object):
    allEventsToAdd = []

    def __init__(self, name, duration,
                 startYear, startMonth, startDay, startHr, startMin,
                 endYear, endMonth, endDay, endHr, endMin,
                 timeOfDayStartHr=0, timeOfDayStartMin=0,
                 timeOfDayEndHr=11, timeOfDayEndMin=59, location=None, notes=None):
        self.name = name
        self.duration = duration
        self.start = datetime.datetime(startYear, startMonth, startDay, startHr, startMin)
        self.end = datetime.datetime(endYear, endMonth, endDay, endHr, endMin)
        self.timeOfDayStart = datetime.time(timeOfDayStartHr, timeOfDayStartMin)
        self.timeOfDayEnd = datetime.time(timeOfDayEndHr, timeOfDayEndMin)
        self.possibleBlocks = []
        self.location = location
        self.notes = notes
        self.createAllBlocks()
        self.addEventToAllEventsToAdd(len(AddEvent.allEventsToAdd)//2)
    
    def __lt__(self, other):
        return self.duration < other.duration

    def __gt__(self, other):
        return self.duration > other.duration
    
    def __repr__(self):
        return self.name
    
    # adds tuples of start and end times for each day which the event can be
    # scheduled in to the list of possibleBlocks
    def createAllBlocks(self):
        start = self.start
        end = self.end
        while (start.date() <= end.date()):
            self.possibleBlocks.append((datetime.datetime.combine(start, self.timeOfDayStart), 
                                        datetime.datetime.combine(start, self.timeOfDayEnd)))
            start += datetime.timedelta(days=1)

    # adds the new event to its appropriate location in allEventsToAdd
    # based on event's duration
    def addEventToAllEventsToAdd(self, i):
        AddEvent.allEventsToAdd.append(self)
        AddEvent.allEventsToAdd.sort()