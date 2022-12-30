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

################################ Page Class ################################
class Page(object):

    bulletJournal = []

    def __init__(self, type, theme=None, year=None, month=None, day=None):
        self.type = type # blank, calendar, weekly, title
        self.theme = theme # None, polar bear
        self.year = year # None, value
        self.month = month # None, value
        self.day = day # None, value
        self.drawings = []
        if (year != None) and (month != None) and (day != None):
            self.date = datetime.datetime(year, month, day)
            self.weeklyDates = self.getWeeklyCalendarDates()
        else:
            self.date = None
            self.weeklyDates = None
        if (len(Page.bulletJournal) >= 2):
            Page.bulletJournal.insert(-1, self)
        else:
            Page.bulletJournal.append(self)
    
    def __repr__(self):
        return f' |Type: {self.type}, Theme: {self.theme}, Date: {self.date}| '
    
    def deletePage(self, app):
        Page.bulletJournal.pop(app.indexPageToDisplay)
    
    def createDrawings(self, app, canvas):
        for drawing in self.drawings:
            if (drawing[0] == 'free draw'):
                if (len(drawing[1]) > 3):
                    canvas.create_line(drawing[1], smooth=True, width=2)
            elif (drawing[0] == 'line'):
                if (len(drawing[1]) == 4):
                    canvas.create_line(drawing[1], width=2)
            elif (drawing[0] == 'rectangle'):
                if (len(drawing[1]) == 4):
                    canvas.create_rectangle(drawing[1], width=2)
            elif (drawing[0] == 'oval'):
                if (len(drawing[1]) == 4):
                    canvas.create_oval(drawing[1], width=2)
            elif (drawing[0] == 'triangle'):
                if (len(drawing[1]) == 6):
                    canvas.create_polygon(drawing[1], outline='black', fill='white', width=2)

    # provided a date of the week which is going to be displayed, it returns a
    # datetime object for each of the days of the week
    def getWeeklyCalendarDates(self):
        year, week, weekday = self.date.isocalendar()
        if (weekday == 7):
            self.date += datetime.timedelta(days=7)
            year, week, weekday = self.date.isocalendar()
        mon = datetime.datetime.fromisocalendar(year, week, 1)
        tue = datetime.datetime.fromisocalendar(year, week, 2)
        wed = datetime.datetime.fromisocalendar(year, week, 3)
        thu = datetime.datetime.fromisocalendar(year, week, 4)
        fri = datetime.datetime.fromisocalendar(year, week, 5)
        sat = datetime.datetime.fromisocalendar(year, week, 6)
        sun = mon - datetime.timedelta(days=1)
        return (sun, mon, tue, wed, thu, fri, sat)

    # returns the formated date to be displayed
    def dateToBeDisplayed(self, date):
        return f'{date.month}/{date.day}/{date.year}'
    
    # draws the labels for each day of the week to be displayed
    def drawWeeklyLabels(self, app, canvas):
        canvas.create_text(app.edgeX + 136, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[0])}', font='Ariel 10')
        canvas.create_text(app.edgeX + 228, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[1])}', font='Ariel 10')
        canvas.create_text(app.edgeX + 325, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[2])}', font='Ariel 10')
        canvas.create_text(app.edgeX + 419, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[3])}', font='Ariel 10')
        canvas.create_text(app.edgeX + 533, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[4])}', font='Ariel 10')
        canvas.create_text(app.edgeX + 630, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[5])}', font='Ariel 10')
        canvas.create_text(app.edgeX + 727, 249, text=f'{self.dateToBeDisplayed(self.weeklyDates[6])}', font='Ariel 10')

    # draws the page of the calendar
    def drawPage(self, app, canvas):
        if (self.type == 'calendar'):
            if (self.theme == 'polar bear'):
                canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.polarBearCalendar[self.month-1]), anchor='sw')
            elif (self.theme == 'blank'):
                canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.blankCalendar[self.month-1]), anchor='sw')
            self.drawCalendarDates(app, canvas)
        elif (self.type == 'weekly'):
            if (self.theme == 'polar bear'):
                canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.polarBearWeekly[self.month-1]), anchor='sw')
            elif (self.theme == 'blank'):
                canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.blankWeekly[self.month-1]), anchor='sw')
            self.drawWeeklyLabels(app, canvas)
            self.drawEvents(app, canvas)
        elif (self.type == 'title'):
            if (self.theme == 'polar bear'):
                canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.polarBearTitle[self.month-1]), anchor='sw')
            elif (self.theme == 'weekly'):
                canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.blankPage), anchor='sw')
        elif (self.type == 'blank'):
            canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.blankPage), anchor='sw')
        elif (self.type == 'front cover'):
            canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.frontCover), anchor='sw')
        elif (self.type == 'back cover'):
            canvas.create_image(app.edgeX, app.height, image=ImageTk.PhotoImage(app.backCover), anchor='sw')

    # Formula to determine if year is leap year is from:
    # https://docs.microsoft.com/en-us/office/troubleshoot/excel/determine-a-leap-year
    def isLeapYear(self, year):
        if (year % 4 != 0): return False
        if (year % 100 != 0): return True
        if (year % 400 != 0): return False
        else: return True
    
    def getDaysInMonth(self, month, year):
        if (month in [4, 6, 9, 11]):
            return 30
        elif (month in [1, 3, 5, 7, 8, 10, 12]):
            return 31
        elif (self.isLeapYear(year)): return 29
        else: return 28

    def drawPreviousMonthDates(self, app, canvas, firstWeekday):
        if (self.month - 1 == 0):
            previousMonth = 12
            previousYear = self.year - 1
        else:
            previousMonth = self.month - 1
            previousYear = self.year
        daysInPreviousMonth = self.getDaysInMonth(previousMonth, previousYear)

        for col in range(firstWeekday-1, -1, -1):
            if (col < 4):
                x = 101 + 93*col
            else:
                x = 505 + 93*(col-4)
            canvas.create_text(app.edgeX + x, 251, text=f'{daysInPreviousMonth}', fill='light grey', font='Arial 12')
            daysInPreviousMonth -= 1

    def drawCurrentAndNextMonthDates(self, app, canvas, firstWeekday):
        daysInMonth = self.getDaysInMonth(self.month, self.year)
        numToPlace = 1
        col = firstWeekday
        color = 'black'
        for row in range(5):
            col %= 7
            while (col < 7):
                if (col < 4):
                    x = 101 + 93*col
                else:
                    x = 505 + 93*(col-4)
                y = 251 + 96*row
                canvas.create_text(app.edgeX + x, y, text=f'{numToPlace}', fill=color, font='Arial 12')
                numToPlace += 1
                col += 1
                if (numToPlace > daysInMonth):
                    numToPlace = 1
                    color = 'light grey'

    def drawCalendarDates(self, app, canvas):
        canvas.create_text(app.edgeX + 895, 115, text=f'{self.year}', font='Arial 20', anchor='ne')
        firstWeekday = self.date.replace(day=1).isoweekday()
        firstWeekday %= 7

        self.drawPreviousMonthDates(app, canvas, firstWeekday)
        self.drawCurrentAndNextMonthDates(app, canvas, firstWeekday)

    def findFirstIndexToDraw(self, i, startTime, endTime):
        if (i == len(Event.allEvents)):
            return None
        elif (startTime <= Event.allEvents[i].startDateAndTime < endTime):
            return i
        else:
            return self.findFirstIndexToDraw(i+1, startTime, endTime)

    def findLastIndexToDraw(self, i, endTime):
        if (i == len(Event.allEvents)):
            return len(Event.allEvents)
        elif (endTime <= Event.allEvents[i].startDateAndTime):
            return i
        else:
            return self.findLastIndexToDraw(i+1, endTime)
    
    def getStartAndEndTimes(self, event):
        eventStartTime = event.startDateAndTime
        eventEndTime = event.endDateAndTime
        startTime = eventStartTime - eventStartTime.replace(hour=0, minute=0)
        endTime = eventEndTime - eventEndTime.replace(hour=0, minute=0)
        return (startTime / datetime.timedelta(hours = 24), endTime / datetime.timedelta(hours = 24))

    def getCoordinatesForSingularEvent(self, eventToDraw):
        startHeight, endHeight = self.getStartAndEndTimes(eventToDraw)
        dayOfWeek = eventToDraw.startDateAndTime.isoweekday() % 7
        if (dayOfWeek < 4):
            x1, y1 = 91 + 93*dayOfWeek, 306 + startHeight*16.125*24 
            x2, y2 = x1 + 93, 306 + endHeight*16.125*24
        else:
            x1, y1 = 493 + 94*(dayOfWeek-4), 306 + startHeight*16.125*24
            x2, y2 = x1 + 94, 306 + endHeight*16.125*24
        return (x1, y1, x2, y2)

    def drawSingularEvent(self, app, canvas, eventToDraw):
        x1, y1, x2, y2 = self.getCoordinatesForSingularEvent(eventToDraw)
        canvas.create_rectangle(app.edgeX + x1, y1, app.edgeX + x2, y2, fill = 'light grey')
        name = ''
        countInLine = 0
        for char in eventToDraw.name:
            if (countInLine == 15):
                name += '\n'
                countInLine = 0
            name += char
            countInLine += 1
        canvas.create_text(app.edgeX + (x1+x2)/2, (y1+y2)/2, text=name, font='Menlo 10')
    
    def drawEvents(self, app, canvas):
        if (app.indexFirstEventToDraw != None):
            for i in range(app.indexFirstEventToDraw, app.indexLastEventToDraw):
                event = Event.allEvents[i]
                self.drawSingularEvent(app, canvas, event)
    
    def drawDeleteExitEditButtons(self, app, canvas):
        deleteWidth, deleteHeight = app.deleteButtonImage.size
        scale = min (30/deleteWidth, 30/deleteHeight)
        deleteScaledImage = app.scaleImage(app.deleteButtonImage, scale)
        canvas.create_image(app.edgeX + 720-5, 6*app.height/7-10, image=ImageTk.PhotoImage(deleteScaledImage), anchor='se')
        
        exitWidth, exitHeight = app.exitButtonImage.size
        scale = min (20/exitWidth, 20/exitHeight)
        exitScaledImage = app.scaleImage(app.exitButtonImage, scale)
        canvas.create_image(app.edgeX + 720-10, app.height/7+10, image=ImageTk.PhotoImage(exitScaledImage), anchor='ne')

    def displayEventInfo(self, app, canvas, event):
        x1, y1, x2, y2 = 240, app.height/7, 720, 6*app.height/7
        canvas.create_rectangle(app.edgeX + x1, y1, app.edgeX + x2, y2, fill='light grey', outline='dark grey', width=3)
        self.drawDeleteExitEditButtons(app, canvas)
        canvas.create_text(app.edgeX + x1+10, y1+10, text=event.name, font='Menlo 30', anchor='nw')
        canvas.create_text(app.edgeX + x1+10, y1+60,
                           text=f'Start Time: {event.startDateAndTime}',
                           font='Menlo 20', anchor='nw')
        canvas.create_text(app.edgeX + x1+10, y1+90, text=f'End Time: {event.endDateAndTime}',
                           font='Menlo 20', anchor='nw')
        canvas.create_text(app.edgeX + x1+10, y1+120, text=f'Location: {event.location}',
                           font='Menlo 20', anchor='nw')
        canvas.create_text(app.edgeX + x1+10, y1+150, text=f'Notes: {event.notes}',
                           font='Menlo 20', anchor='nw')

############################## Top Buttons Class ###############################
class Button(object):

    allButtons = []
    numButtons = 0
    diameter = 40

    def __init__(self, name, function, image):
        self.name = name
        self.numInRow = Button.numButtons
        self.function = function
        self.image = image
        Button.allButtons.append(self)
        Button.numButtons += 1
    
    def __repr__(self):
        return str(self.name)
    
    def getCenterCoords(self, app):
        margin = (app.width - (Button.numButtons-1)*65) / 2
        return (margin + self.numInRow*65, 30)
    
    @staticmethod
    def drawAllButtons(app, canvas):
        canvas.create_rectangle(0, 0, app.width, 60, outline='dark grey')
        for button in Button.allButtons:
            buttonWidth, buttonHeight = button.image.size
            scale = min(Button.diameter/buttonWidth, Button.diameter/buttonHeight)
            scaledImage = app.scaleImage(button.image, scale)
            canvas.create_image(button.getCenterCoords(app), image=ImageTk.PhotoImage(scaledImage))

def updateIndexesOfEventsDisplayed(app):
    pageDisplayed = Page.bulletJournal[app.indexPageToDisplay]
    if (pageDisplayed.type == 'weekly'):
        startTime = pageDisplayed.weeklyDates[0]
        endTime = pageDisplayed.weeklyDates[6] + datetime.timedelta(days=1)
        app.indexFirstEventToDraw = pageDisplayed.findFirstIndexToDraw(0, startTime, endTime)
        if (app.indexFirstEventToDraw != None):
            app.indexLastEventToDraw = pageDisplayed.findLastIndexToDraw(app.indexFirstEventToDraw, endTime)
        else: app.indexLastEventToDraw = None
    else:
        app.indexFirstEventToDraw = None
        app.indexLastEventToDraw = None

def createEventButtonFunction(app):
    app.addingNewEvent = not app.addingNewEvent
    if (app.addingNewEvent):
        app.addingNewPage = False

def createEventToBeScheduledButtonFunction(app):
    app.addingEventToBeScheduled = not app.addingEventToBeScheduled

def addPageButtonFunction(app):
    app.addingNewPage = not app.addingNewPage

def nextPageButtonFunction(app):
    if (app.indexPageToDisplay < len(Page.bulletJournal)-1):
        app.indexPageToDisplay += 1
    app.displayEventInfo = None
    updateIndexesOfEventsDisplayed(app)

def previousPageButtonFunction(app):
    if (app.indexPageToDisplay > 0):
        app.indexPageToDisplay -= 1
    app.displayEventInfo = None
    updateIndexesOfEventsDisplayed(app)

def selfScheduleButtonFunction(app):
    selfSchedule(AddEvent.allEventsToAdd, len(AddEvent.allEventsToAdd)-1)
    AddEvent.allEventsToAdd = []
    updateIndexesOfEventsDisplayed(app)

def drawingButtonFunction(app):
    app.drawing = not app.drawing
    if (app.drawing):
        app.displayPossibleShapes = False
        app.shapeDrawing = None
        app.erasing = False

def drawingShapeButtonFunction(app):
    app.displayPossibleShapes = not app.displayPossibleShapes
    if (app.displayPossibleShapes):
        app.drawing = False
        app.erasing = False
    app.shapeDrawing = None

def eraseButtonFunction(app):
    app.erasing = not app.erasing
    if (app.erasing):
        app.drawing = False
        app.displayPossibleShapes = False
        app.shapeDrawing = None

############################ AddPage Buttons Class #############################
class AddPageButton(object):
    allAddPageButtons = []

    def __init__(self, name, text, function, x1, y1, x2, y2):
        self.name = name
        self.text = text
        self.color = 'white'
        self.function = function
        self.x1= x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        AddPageButton.allAddPageButtons.append(self)
    
    def editColor(self, newColor):
        self.color = newColor
    
    def pressedInsideButton(self, app, eventX, eventY):
        if (app.edgeX + self.x1 < eventX < app.edgeX + self.x2) and (self.y1 < eventY < self.y2):
            self.function(app, self)
            return True
        else: return False
    
    def drawButton(self, app, canvas):
        canvas.create_rectangle(app.edgeX+self.x1, self.y1, app.edgeX+self.x2, self.y2,
                                fill=self.color, outline='dark grey')
        if (self.name == 'Month'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.apMonth, font='Menlo 20', anchor='nw')
            canvas.create_text(app.edgeX+(self.x1+self.x2)/2, self.y1+30, text=self.text, font='Menlo 15', anchor='n')
        elif (self.name == 'Day'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.apDay, font='Menlo 20', anchor='nw')
            canvas.create_text(app.edgeX+(self.x1+self.x2)/2, self.y1+30, text=self.text, font='Menlo 15', anchor='n')
        elif (self.name == 'Year'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.apYear, font='Menlo 20', anchor='nw')
            canvas.create_text(app.edgeX+(self.x1+self.x2)/2, self.y1+30, text=self.text, font='Menlo 15', anchor='n')
        else:
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=self.text, font='Menlo 20', anchor='nw')

def drawAllAddPageButtons(app, canvas):
    canvas.create_rectangle(app.edgeX+240, 782/7, app.edgeX+720, 782/7+230,
                            fill='light grey', outline='dark grey', width=3)
    canvas.create_text(app.edgeX+240+10, 782/7+15, text='Type:', font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+55, text='Theme:', font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+90, text='Date in week you want to display:',
                       font='Menlo 20', anchor='nw')
    for button in AddPageButton.allAddPageButtons:
        button.drawButton(app, canvas)

def typeBlankAddPageButtonFunction(app, button):
    button.editColor('plum1')
    app.apType = 'blank'

def typeTitleAddPageButtonFunction(app, button):
    button.editColor('plum1')
    app.apType = 'title'

def typeCalendarAddPageButtonFunction(app, button):
    button.editColor('plum1')
    app.apType = 'calendar'

def typeWeeklyAddPageButtonFunction(app, button):
    button.editColor('plum1')
    app.apType = 'weekly'

def themeBlankAddPageButtonFunction(app, button):
    button.editColor('plum1')
    app.apTheme = 'blank'

def themePolarBearAddPageButtonFunction(app, button):
    button.editColor('plum1')
    app.apTheme = 'polar bear'

def monthAddPageButtonFunction(app, button):
    app.apTypingMonth = True
    app.apTypingDay = False
    app.apTypingYear = False

def dayAddPageButtonFunction(app, button):
    app.apTypingMonth = False
    app.apTypingDay = True
    app.apTypingYear = False

def yearAddPageButtonFunction(app, button):
    app.apTypingMonth = False
    app.apTypingDay = False
    app.apTypingYear = True

def enterAddPageButtonFunction(app, button):
    if (app.apYear == app.apMonth == app.apDay == '') and (app.apType == 'blank'):
        Page('blank')
    elif (app.apType == 'title') and (app.apTheme == 'blank'):
        Page('blank')
    elif (app.apYear == app.apDay == '') and (app.apType == 'title') and (app.apTheme != ''):
        try: Page('title', app.apTheme, month=int(app.apMonth))
        except: return
    elif (app.apDay == '') and (app.apType == 'calendar') and (app.apTheme != ''):
        try: Page('calendar', app.apTheme, int(app.apYear), int(app.apMonth), 1)
        except: return
    else:
        try: Page(app.apType, app.apTheme, int(app.apYear), int(app.apMonth), int(app.apDay))
        except: return
    app.apType = app.apTheme = app.apMonth = app.apDay = app.apYear = ''
    app.addingNewPage = app.apTypingMonth = app.apTypingDay = app.apTypingYear = False
    for button in AddPageButton.allAddPageButtons:
        button.color = 'white'

############################ AddEvent Buttons Class ############################
class AddEventButton(object):
    allAddEventButtons = []

    def __init__(self, name, text, x1, y1, x2, y2, function=None):
        self.name = name
        self.text = text
        self.color = 'white'
        self.function = function
        self.x1= x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        AddEventButton.allAddEventButtons.append(self)
    
    def editColor(self, newColor):
        self.color = newColor
    
    def pressedInsideButton(self, app, eventX, eventY):
        if (app.edgeX + self.x1 < eventX < app.edgeX + self.x2) and (self.y1 < eventY < self.y2):
            self.function(app)
            return True
        else: return False
    
    def drawButton(self, app, canvas):
        canvas.create_rectangle(app.edgeX+self.x1, self.y1, app.edgeX+self.x2, self.y2,
                                fill=self.color, outline='dark grey')
        if (self.name != 'Enter'):
            canvas.create_text(app.edgeX+(self.x1+self.x2)/2, self.y2+5, text=self.text, font='Menlo 15', anchor='n')
        if (self.name == 'Name'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeName, font='Menlo 20', anchor='nw')
        elif (self.name == 'Month'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeMonth, font='Menlo 20', anchor='nw')
        elif (self.name == 'Day'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeDay, font='Menlo 20', anchor='nw')
        elif (self.name == 'Year'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeYear, font='Menlo 20', anchor='nw')
        elif (self.name == 'Start time'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeStartTime, font='Menlo 20', anchor='nw')
        elif (self.name == 'End time'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeEndTime, font='Menlo 20', anchor='nw')
        elif (self.name == 'Enter'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=self.text, font='Menlo 20', anchor='nw')
        elif (self.name == 'Location'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeLocation, font='Menlo 20', anchor='nw')
        elif (self.name == 'Notes'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aeNotes, font='Menlo 20', anchor='nw')

def drawAllAddEventButtons(app, canvas):
    canvas.create_rectangle(app.edgeX+240, 782/7, app.edgeX+720, 782/7+600,
                            fill='light grey', outline='dark grey', width=3)
    canvas.create_text(app.edgeX+240+10, 782/7+15, text='Name:', font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+55, text='Date:', font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+110, text='Start Time:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+170, text='End Time:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+235, text='Location:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+275, text='Notes:',
                       font='Menlo 20', anchor='nw')
    for button in AddEventButton.allAddEventButtons:
        button.drawButton(app, canvas)

def enterAddEventButtonFunction(app):
    startMonth, startDay, startYear = int(app.aeMonth), int(app.aeDay), int(app.aeYear)

    startTime = app.aeStartTime.split(':')
    startHour, startMinute = int(startTime[0]), int(startTime[1])

    endTime = app.aeEndTime.split(':')
    endHour, endMinute = int(endTime[0]), int(endTime[1])
    Event(app.aeName, startYear, startMonth, startDay, startHour, startMinute, startYear, startMonth, startDay, endHour, endMinute, app.aeLocation, app.aeNotes)
    updateIndexesOfEventsDisplayed(app)

    app.numInLine = 0
    app.addingNewEvent = False
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False

    app.aeName = ''
    app.aeMonth = ''
    app.aeDay = ''
    app.aeYear = ''
    app.aeStartTime = ''
    app.aeEndTime = ''
    app.aeLocation = ''
    app.aeNotes = ''

def nameAddEventButtonFunction(app):
    app.aeTypingName = True
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False
        
def monthAddEventButtonFunction(app):
    app.aeTypingMonth = True
    app.aeTypingName = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False

def dayAddEventButtonFunction(app):
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = True
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False

def yearAddEventButtonFunction(app):
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = True
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False

def startTimeAddEventButtonFunction(app):
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = True
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False

def endTimeAddEventButtonFunction(app):
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = True
    app.aeTypingLocation = False
    app.aeTypingNotes = False

def locationAddEventButtonFunction(app):
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = True
    app.aeTypingNotes = False

def notesAddEventButtonFunction(app):
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = True

###################### AddEventToBeScheduled Buttons Class #####################
class AddEventToBeScheduledButton(object):
    allAddEventToBeScheduledButtons = []

    def __init__(self, name, text, x1, y1, x2, y2, function=None):
        self.name = name
        self.text = text
        self.color = 'white'
        self.function = function
        self.x1= x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        AddEventToBeScheduledButton.allAddEventToBeScheduledButtons.append(self)
    
    def pressedInsideButton(self, app, eventX, eventY):
        if (app.edgeX + self.x1 < eventX < app.edgeX + self.x2) and (self.y1 < eventY < self.y2):
            self.function(app)
            return True
        else: return False
    
    def drawButton(self, app, canvas):
        canvas.create_rectangle(app.edgeX+self.x1, self.y1, app.edgeX+self.x2, self.y2,
                                fill=self.color, outline='dark grey')
        if (self.name != 'Enter'):
            canvas.create_text(app.edgeX+(self.x1+self.x2)/2, self.y2+5, text=self.text, font='Menlo 15', anchor='n')
        if (self.name == 'Name'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsName, font='Menlo 20', anchor='nw')
        elif (self.name == 'Duration'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsDuration, font='Menlo 20', anchor='nw')
        elif (self.name == 'Start month'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsStartMonth, font='Menlo 20', anchor='nw')
        elif (self.name == 'Start day'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsStartDay, font='Menlo 20', anchor='nw')
        elif (self.name == 'Start year'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsStartYear, font='Menlo 20', anchor='nw')
        elif (self.name == 'End month'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsEndMonth, font='Menlo 20', anchor='nw')
        elif (self.name == 'End day'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsEndDay, font='Menlo 20', anchor='nw')
        elif (self.name == 'End year'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsEndYear, font='Menlo 20', anchor='nw')
        elif (self.name == 'Start time'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsStartTime, font='Menlo 20', anchor='nw')
        elif (self.name == 'End time'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsEndTime, font='Menlo 20', anchor='nw')
        elif (self.name == 'Enter'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=self.text, font='Menlo 20', anchor='nw')
        elif (self.name == 'Location'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsLocation, font='Menlo 20', anchor='nw')
        elif (self.name == 'Notes'):
            canvas.create_text(app.edgeX+self.x1+5, self.y1+5, text=app.aetbsNotes, font='Menlo 20', anchor='nw')

def drawAllAddEventToBeScheduledButtons(app, canvas):
    canvas.create_rectangle(app.edgeX+240, 782/7, app.edgeX+720, 782/7+600,
                            fill='light grey', outline='dark grey', width=3)
    canvas.create_text(app.edgeX+240+10, 782/7+15, text='Name:', font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 782/7+55, text='Duration:', font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 220, text='Start Date:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 275, text='End Date:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 332, text='Start Time:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 390, text='End Time:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 447, text='Location:',
                       font='Menlo 20', anchor='nw')
    canvas.create_text(app.edgeX+240+10, 486, text='Notes:',
                       font='Menlo 20', anchor='nw')
    for button in AddEventToBeScheduledButton.allAddEventToBeScheduledButtons:
        button.drawButton(app, canvas)

def enterAETBSButtonFunction(app):
    duration = app.aetbsDuration.split(':')
    durationHours, durationMinutes = int(duration[0]), int(duration[1])

    startMonth, startDay, startYear = int(app.aetbsStartMonth), int(app.aetbsStartDay), int(app.aetbsStartYear)
    endMonth, endDay, endYear = int(app.aetbsEndMonth), int(app.aetbsEndDay), int(app.aetbsEndYear)

    startTime = app.aetbsStartTime.split(':')
    startHour, startMinute = int(startTime[0]), int(startTime[1])

    endTime = app.aetbsEndTime.split(':')
    endHour, endMinute = int(endTime[0]), int(endTime[1])
    
    AddEvent(app.aetbsName, datetime.timedelta(hours=durationHours, minutes=durationMinutes),
             startYear, startMonth, startDay, 0, 0, endYear, endMonth, endDay,
             23, 59, startHour, startMinute, endHour, endMinute,
             location=app.aetbsLocation, notes=app.aetbsNotes)

    app.addingEventToBeScheduled = False
    app.aetbsNumInLine = 0
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

    app.aetbsName = ''
    app.aetbsDuration = ''
    app.aetbsStartMonth = ''
    app.aetbsStartDay = ''
    app.aetbsStartYear = ''
    app.aetbsEndMonth = ''
    app.aetbsEndDay = ''
    app.aetbsEndYear = ''
    app.aetbsStartTime = ''
    app.aetbsEndTime = ''
    app.aetbsLocation = ''
    app.aetbsNotes = ''

def nameAETBSButtonFunction(app):
    app.aetbsTypingName = True
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def durationAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = True
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def startMonthAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = True
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def startDayAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = True
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def startYearAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = True
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def endMonthAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = True
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def endDayAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = True
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def endYearAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = True
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def startTimeAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = True
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def endTimeAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = True
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

def locationAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = True
    app.aetbsTypingNotes = False

def notesAETBSButtonFunction(app):
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = True

################################################################################
def createButtons(app):
    app.addEventButton = Button('Add Event', createEventButtonFunction, app.addEventButtonImage)
    app.scheduleEventButton = Button('Schdule Event', createEventToBeScheduledButtonFunction, app.scheduleEventButtonImage)
    app.selfScheduleButton = Button('Self Schedule', selfScheduleButtonFunction, app.selfScheduleButtonImage)
    app.addPage = Button('Add Page', addPageButtonFunction, app.addPageImage)
    app.drawingButton = Button('Drawing', drawingButtonFunction, app.freeDrawButtonImage)
    app.shapeButton = Button('Rectangle', drawingShapeButtonFunction, app.shapesButtonImage)
    app.eraseButton = Button('Erase', eraseButtonFunction, app.eraseButtonImage)
    app.previousPageButton = Button('Previous Page', previousPageButtonFunction, app.previousPageButtonImage)
    app.nextPageButton = Button('Next Page', nextPageButtonFunction, app.nextPageButtonImage)

def createAddPageButtons(app):
    AddPageButton('Type: Blank', 'Blank', typeBlankAddPageButtonFunction, 315, 782/7+10, 240+145, 782/7+40)
    AddPageButton('Type: Title', 'Title', typeTitleAddPageButtonFunction, 240+155, 782/7+10, 240+225, 782/7+40)
    AddPageButton('Type: Calendar', 'Calendar', typeCalendarAddPageButtonFunction, 240+235, 782/7+10, 240+341, 782/7+40)
    AddPageButton('Type: Weekly', 'Weekly', typeWeeklyAddPageButtonFunction, 240+351, 782/7+10, 240+433, 782/7+40)
    AddPageButton('Theme: Blank', 'Blank', themeBlankAddPageButtonFunction, 240+95, 782/7+50, 240+165, 782/7+80)
    AddPageButton('Theme: Polar Bear', 'Polar Bear', themePolarBearAddPageButtonFunction, 240+195, 782/7+50, 240+325, 782/7+80)
    AddPageButton('Month', 'MM', monthAddPageButtonFunction, 240+10, 782/7+115, 240+44, 782/7+145)
    AddPageButton('Day', 'DD', dayAddPageButtonFunction, 240+50, 782/7+115, 240+85, 782/7+145)
    AddPageButton('Year', 'YYYY', yearAddPageButtonFunction, 240+91, 782/7+115, 240+148, 782/7+145)
    AddPageButton('Enter', 'Enter', enterAddPageButtonFunction, 630, 782/7+180, 700, 782/7+210)

def createAddEventButtons(app):
    AddEventButton('Name', '', 315, 782/7+10, 700, 782/7+40, nameAddEventButtonFunction)
    AddEventButton('Month', 'MM', 240+75, 782/7+50, 240+109, 782/7+80, monthAddEventButtonFunction)
    AddEventButton('Day', 'DD', 240+115, 782/7+50, 240+150, 782/7+80, dayAddEventButtonFunction)
    AddEventButton('Year', 'YYYY', 240+156, 782/7+50, 240+213, 782/7+80, yearAddEventButtonFunction)
    AddEventButton('Start time', 'HH:MM', 240+150, 782/7+105, 240+219, 782/7+135, startTimeAddEventButtonFunction)
    AddEventButton('End time', 'HH:MM', 240+150, 782/7+170, 240+219, 782/7+200, endTimeAddEventButtonFunction)
    AddEventButton('Location', '', 240+120, 782/7+230, 700, 782/7+260, locationAddEventButtonFunction)
    AddEventButton('Notes', '', 330, 782/7+270, 700, 782/7+540, notesAddEventButtonFunction)
    AddEventButton('Enter', 'Enter', 630, 782/7+550, 700, 782/7+580, enterAddEventButtonFunction)

def createAddEventToBeScheduledButtons(app):
    AddEventToBeScheduledButton('Name', '', 315, 782/7+10, 700, 782/7+40, nameAETBSButtonFunction)
    AddEventToBeScheduledButton('Duration', 'HH:MM', 372, 782/7+50, 441, 782/7+80, durationAETBSButtonFunction)
    AddEventToBeScheduledButton('Start month', 'MM', 394, 220, 428, 250, startMonthAETBSButtonFunction)
    AddEventToBeScheduledButton('Start day', 'DD', 433, 220, 467, 250, startDayAETBSButtonFunction)
    AddEventToBeScheduledButton('Start year', 'YYYY', 472, 220, 529, 250, startYearAETBSButtonFunction)
    AddEventToBeScheduledButton('End month', 'MM', 394, 275, 428, 305, endMonthAETBSButtonFunction)
    AddEventToBeScheduledButton('End day', 'DD', 433, 275, 467, 305, endDayAETBSButtonFunction)
    AddEventToBeScheduledButton('End year', 'YYYY', 472, 275, 529, 305, endYearAETBSButtonFunction)
    AddEventToBeScheduledButton('Start time', 'HH:MM', 240+150, 330, 240+219, 360, startTimeAETBSButtonFunction)
    AddEventToBeScheduledButton('End time', 'HH:MM', 240+150, 388, 240+219, 418, endTimeAETBSButtonFunction)
    AddEventToBeScheduledButton('Location', '', 240+125, 445, 700, 475, locationAETBSButtonFunction)
    AddEventToBeScheduledButton('Notes', '', 330, 484, 700, 782/7+540, notesAETBSButtonFunction)
    AddEventToBeScheduledButton('Enter', 'Enter', 630, 782/7+550, 700, 782/7+580, enterAETBSButtonFunction)

def loadButtonImages(app):
    app.addEventButtonImage = app.loadImage('add event button.png')
    app.scheduleEventButtonImage = app.loadImage('add event to be scheduled button.png')
    app.selfScheduleButtonImage = app.loadImage('schedule button.png')
    app.addPageImage = app.loadImage('add page button.png')
    app.previousPageButtonImage = app.loadImage('previous page button.png')
    app.nextPageButtonImage = app.loadImage('next page button.png')
    app.deleteButtonImage = app.loadImage('delete button.png')
    app.exitButtonImage = app.loadImage('exit button.png')
    app.freeDrawButtonImage = app.loadImage('free draw button.png')
    app.shapesButtonImage = app.loadImage('shapes button.png')
    app.eraseButtonImage = app.loadImage('erase button.png')

def loadBlankTheme(app):
    app.blankPage = app.loadImage('blank page.jpg')
    app.blankCalendar = []
    app.blankWeekly = []
    for month in ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec']:
        app.blankCalendar.append(app.loadImage(f'blank calendar - {month}.jpg'))
        app.blankWeekly.append(app.loadImage(f'blank weekly - {month}.jpg'))

# Images were drawn by myself but I got inspiration from the following images:
# https://www.reddit.com/r/bulletjournal/comments/ekw8jn/polar_bears_for_january/
# https://inprint.xyz/product/polar-bear-with-flowers-calendar-print/
def loadPolarBearTheme(app):
    app.polarBearTitle = []
    app.polarBearCalendar = []
    app.polarBearWeekly = []
    for month in ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec']:
        app.polarBearTitle.append(app.loadImage(f'polar bear title - {month}.jpg'))
        app.polarBearCalendar.append(app.loadImage(f'polar bear calendar - {month}.jpg'))
        app.polarBearWeekly.append(app.loadImage(f'polar bear weekly - {month}.jpg'))

def initialAddPageValues(app):
    app.addingNewPage = False
    app.apTypingMonth = False
    app.apTypingDay = False
    app.apTypingYear = False

    app.apType = ''
    app.apTheme = ''
    app.apMonth = ''
    app.apDay = ''
    app.apYear = ''

def initialAddEventValues(app):
    app.numInLine = 0
    app.addingNewEvent = False
    app.aeTypingName = False
    app.aeTypingMonth = False
    app.aeTypingDay = False
    app.aeTypingYear = False
    app.aeTypingStartTime = False
    app.aeTypingEndTime = False
    app.aeTypingLocation = False
    app.aeTypingNotes = False

    app.aeName = ''
    app.aeMonth = ''
    app.aeDay = ''
    app.aeYear = ''
    app.aeStartTime = ''
    app.aeEndTime = ''
    app.aeLocation = ''
    app.aeNotes = ''

def inititalAddEventToBeScheduledValues(app):
    app.addingEventToBeScheduled = False
    app.aetbsNumInLine = 0
    app.aetbsTypingName = False
    app.aetbsTypingDuration = False
    app.aetbsTypingStartMonth = False
    app.aetbsTypingStartDay = False
    app.aetbsTypingStartYear = False
    app.aetbsTypingEndMonth = False
    app.aetbsTypingEndDay = False
    app.aetbsTypingEndYear = False
    app.aetbsTypingStartTime = False
    app.aetbsTypingEndTime = False
    app.aetbsTypingLocation = False
    app.aetbsTypingNotes = False

    app.aetbsName = ''
    app.aetbsDuration = ''
    app.aetbsStartMonth = ''
    app.aetbsStartDay = ''
    app.aetbsStartYear = ''
    app.aetbsEndMonth = ''
    app.aetbsEndDay = ''
    app.aetbsEndYear = ''
    app.aetbsStartTime = ''
    app.aetbsEndTime = ''
    app.aetbsLocation = ''
    app.aetbsNotes = ''

def initialDrawingValues(app):
    app.erasing = False
    app.drawing = False
    app.displayPossibleShapes = False
    app.shapeDrawing = None
    app.drawingCoords = []

def appStarted(app):
    loadButtonImages(app)
    createButtons(app)
    createAddPageButtons(app)
    createAddEventButtons(app)
    createAddEventToBeScheduledButtons(app)
    app.indexFirstEventToDraw = None
    app.indexLastEventToDraw = None
    app.displayEventInfo = None

    app.frontCover = app.loadImage('Bullet Journal Front Cover.png')
    app.backCover = app.loadImage('Bullet Journal Back Cover.png')
    loadBlankTheme(app)
    loadPolarBearTheme(app)
    initialDrawingValues(app)
    initialAddPageValues(app)
    initialAddEventValues(app)
    inititalAddEventToBeScheduledValues(app)
    app.indexPageToDisplay = 0
    app.edgeX = 0

    Page('front cover')
    Page('back cover')

def timerFired(app):
    app.edgeX = (app.width - 960) / 2

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def intersectLine(x1, y1, x2, y2, eventX, eventY):
    if (min(x1, x2)-5 < eventX < max(x1, x2)+5) and (min(y1, y2)-5 < eventY < max(y1, y2)+5):
        try:
            slope = (y2-y1)/(x2-x1)
            if (abs(eventY - y1 - (slope * (eventX - x1))) < 5):
                return True
        except:
            if (abs(x1 - eventX) < 5) and (min(y1, y2) < eventY < max((y1, y2))):
                return True
    return False

def eraseShape(app, eventX, eventY):
    page = Page.bulletJournal[app.indexPageToDisplay]
    for drawing in page.drawings:
        if (drawing[0] == 'free draw') or (drawing[0] == 'line'):
            for i in range(0, len(drawing[1])-2, 2):
                x1, y1 = drawing[1][i], drawing[1][i+1]
                x2, y2 = drawing[1][i+2], drawing[1][i+3]
                if (intersectLine(x1, y1, x2, y2, eventX, eventY)):
                    page.drawings.remove(drawing)
                    return
        elif (drawing[0] == 'triangle'):
            x1, y1, x2, y2, x3, y3 = drawing[1]
            if (intersectLine(x1, y1, x2, y2, eventX, eventY) or
                intersectLine(x2, y2, x3, y3, eventX, eventY) or
                intersectLine(x3, y3, x1, y1, eventX, eventY)):
                page.drawings.remove(drawing)
        elif (drawing[0] == 'rectangle'):
            x1, y1, x2, y2 = drawing[1]
            if (intersectLine(x1, y1, x2, y1, eventX, eventY) or
                intersectLine(x2, y1, x2, y2, eventX, eventY) or
                intersectLine(x2, y2, x1, y2, eventX, eventY) or
                intersectLine(x1, y2, x1, y1, eventX, eventY)):
                page.drawings.remove(drawing)
        elif (drawing[0] == 'oval'):
            x1, y1, x2, y2 = drawing[1]
            cx, cy = (x1+x2)/2, (y1+y2)/2
            a, b = abs(cx - x1), abs(cy - y1)
            try:
                if (abs(((eventX - cx)**2)/(a**2) + ((eventY - cy)**2)/(b**2) - 1) < 0.15):
                    page.drawings.remove(drawing)
            except:
                if (x1 - eventX < 5) and (y1 - eventY < 5):
                    page.drawings.remove(drawing)

def pressedInsideButton(app, x, y):
    if ((app.displayEventInfo != None) and
        (Page.bulletJournal[app.indexPageToDisplay].type == 'weekly')):
        # pressed inside delete button
        if (app.edgeX+720-35 < x < app.edgeX+720-5) and (6*app.height/7-40 < y < 6*app.height/7-10):
            app.displayEventInfo.deleteEvent()
            updateIndexesOfEventsDisplayed(app)
            app.displayEventInfo = None
            return
        # pressed inside exit button
        elif (app.edgeX+720-40 < x < app.edgeX+720-10) and (app.height/7+10 < y < app.height/7+40):
            app.displayEventInfo = None
            return
    for button in Button.allButtons:
        centerX, centerY = button.getCenterCoords(app)
        if (distance(centerX, centerY, x, y) < Button.diameter/2):
            button.function(app)
            return

def pressedInsideEvent(app, x, y):
    pageDisplayed = Page.bulletJournal[app.indexPageToDisplay]
    if ((pageDisplayed.type == 'weekly') and
        (app.indexFirstEventToDraw != None) and (app.indexLastEventToDraw != None)):
        for i in range(app.indexFirstEventToDraw, app.indexLastEventToDraw):
            event = Event.allEvents[i]
            x1, y1, x2, y2 = pageDisplayed.getCoordinatesForSingularEvent(event)
            x1, x2 = x1+app.edgeX, x2+app.edgeX
            if (x1 < x < x2) and (y1 < y < y2):
                app.displayEventInfo = event
                return

def pressedInsidePossibleShape(app, eventX, eventY):
    x, y = app.shapeButton.getCenterCoords(app)
    if (distance(eventX, eventY, x+30, 90) < 10):
        app.shapeDrawing = 'line'
        app.displayPossibleShapes = False
    elif (distance(eventX, eventY, x+80, 90) < 10):
        app.shapeDrawing = 'rectangle'
        app.displayPossibleShapes = False
    elif (distance(eventX, eventY, x+30, 130) < 10):
        app.shapeDrawing = 'oval'
        app.displayPossibleShapes = False
    elif (distance(eventX, eventY, x+80, 130) < 10):
        app.shapeDrawing = 'triangle'
        app.displayPossibleShapes = False

def mousePressed(app, event):
    if (app.displayPossibleShapes):
        pressedInsidePossibleShape(app, event.x, event.y)
    elif (app.addingNewPage):
        for singleButton in AddPageButton.allAddPageButtons:
            singleButton.pressedInsideButton(app, event.x, event.y)
    elif (app.addingNewEvent):
        for button in AddEventButton.allAddEventButtons:
            button.pressedInsideButton(app, event.x, event.y)
    elif (app.addingEventToBeScheduled):
        for button in AddEventToBeScheduledButton.allAddEventToBeScheduledButtons:
            button.pressedInsideButton(app, event.x, event.y)
    elif (app.edgeX + 35 < event.x < app.edgeX + 920) and (95 < event.y < 745):
        if (app.drawing == True) or (app.shapeDrawing != None):
            app.drawingCoords.extend((event.x, event.y))
            if (app.shapeDrawing == 'triangle') and (len(app.drawingCoords) == 6):
                page = Page.bulletJournal[app.indexPageToDisplay]
                page.drawings.append(['triangle', copy.copy(app.drawingCoords)])
                app.drawingCoords = []
        elif (app.erasing):
            eraseShape(app, event.x, event.y)
    pressedInsideButton(app, event.x, event.y)
    pressedInsideEvent(app, event.x, event.y)

def keyPressedAddingEvent(app, key):
    if (key == 'Space'):
        charToAdd = ' '
        app.numInLine += 1
    elif (key == 'Enter'):
        charToAdd = '\n'
        app.numInLine = 1
    elif (key == 'Delete'):
        if (app.aeTypingName): app.aeName = app.aeName[:-1]
        elif (app.aeTypingMonth): app.aeMonth = app.aeMonth[:-1]
        elif (app.aeTypingDay): app.aeDay = app.aeDay[:-1]
        elif (app.aeTypingYear): app.aeYear = app.aeYear[:-1]
        elif (app.aeTypingStartTime): app.aeStartTime = app.aeStartTime[:-1]
        elif (app.aeTypingEndTime): app.aeEndTime = app.aeEndTime[:-1]
        elif (app.aeTypingLocation): app.aeLocation = app.aeLocation[:-1]
        elif (app.aeTypingNotes):
            app.aeNotes = app.aeNotes[:-1]
            app.numInLine -= 1
    else:
        if (app.aeTypingNotes) and (app.numInLine >= 30):
            charToAdd = '\n' + key
            app.numInLine = 1
        else:
            charToAdd = key
            if (app.aeTypingNotes): app.numInLine += 1
    
    if (key != 'Delete'):
        if (app.aeTypingName):
            app.aeName += charToAdd
        elif (app.aeTypingMonth):
            if (len(app.aeMonth) == 2):
                app.aeMonth = app.aeMonth[1] + charToAdd
            else:
                app.aeMonth += charToAdd
        elif (app.aeTypingDay):
            if (len(app.aeDay) == 2):
                app.aeDay = app.aeDay[1] + charToAdd
            else:
                app.aeDay += charToAdd
        elif (app.aeTypingYear):
            if (len(app.apYear) == 4):
                app.aeYear = app.aeYear[1:] + charToAdd
            else:
                app.aeYear += charToAdd
        elif (app.aeTypingStartTime):
            app.aeStartTime += charToAdd
        elif (app.aeTypingEndTime):
            app.aeEndTime += charToAdd
        elif (app.aeTypingLocation):
            app.aeLocation += charToAdd
        elif (app.aeTypingNotes):
            app.aeNotes += charToAdd

def keyPressedAddingPage(app, key):
    if (key == 'Space'):
        charToAdd = ' '
    elif (key == 'Enter'):
        charToAdd = '\n'
    elif (key == 'Delete'):
        if (app.apTypingMonth): app.apMonth = app.apMonth[:-1]
        elif (app.apTypingDay): app.apDay = app.apDay[:-1]
        elif (app.apTypingYear): app.apYear = app.apYear[:-1]
    else:
        charToAdd = key
    
    if (key != 'Delete'):
        if (app.apTypingMonth):
            if (len(app.apMonth) == 2):
                app.apMonth = app.apMonth[1] + charToAdd
            else:
                app.apMonth += charToAdd
        elif (app.apTypingDay):
            if (len(app.apDay) == 2):
                app.apDay = app.apDay[1] + charToAdd
            else:
                app.apDay += charToAdd
        elif (app.apTypingYear):
            if (len(app.apYear) == 4):
                app.apYear = app.apYear[1:] + charToAdd
            else:
                app.apYear += charToAdd

def keyPressedAddingEventToBeScheduled(app, key):
    if (key == 'Space'):
        charToAdd = ' '
        app.aetbsNumInLine += 1
    elif (key == 'Enter'):
        charToAdd = '\n'
        app.aetbsNumInLine = 1
    elif (key == 'Delete'):
        if (app.aetbsTypingName): app.aetbsName = app.aetbsName[:-1]
        elif (app.aetbsTypingDuration): app.aetbsTypingDuration = app.aetbsTypingDuration[:-1]
        elif (app.aetbsTypingStartMonth): app.aetbsStartMonth = app.aetbsStartMonth[:-1]
        elif (app.aetbsTypingStartDay): app.aetbsStartDay = app.aetbsStartDay[:-1]
        elif (app.aetbsTypingStartYear): app.aetbsStartYear = app.aetbsStartYear[:-1]
        elif (app.aetbsTypingEndMonth): app.aetbsEndMonth = app.aetbsEndMonth[:-1]
        elif (app.aetbsTypingEndDay): app.aetbsEndDay = app.aetbsEndDay[:-1]
        elif (app.aetbsTypingEndYear): app.aetbsEndYear = app.aetbsEndYear[:-1]
        elif (app.aetbsTypingStartTime): app.aetbsStartTime = app.aetbsStartTime[:-1]
        elif (app.aetbsTypingEndTime): app.aetbsEndTime = app.aetbsEndTime[:-1]
        elif (app.aetbsTypingLocation): app.aetbsLocation = app.aetbsLocation[:-1]
        elif (app.aetbsTypingNotes):
            app.aetbsNotes = app.aetbsNotes[:-1]
            app.aetbsNumInLine -= 1
    else:
        if (app.aetbsTypingNotes) and (app.aetbsNumInLine >= 30):
            charToAdd = '\n' + key
            app.aetbsNumInLine = 1
        else:
            charToAdd = key
            if (app.aetbsTypingNotes): app.aetbsNumInLine += 1
    
    if (key != 'Delete'):
        if (app.aetbsTypingName):
            app.aetbsName += charToAdd
        elif (app.aetbsTypingDuration):
            app.aetbsDuration += charToAdd
        elif (app.aetbsTypingStartMonth):
            if (len(app.aetbsStartMonth) == 2):
                app.aetbsStartMonth = app.aetbsStartMonth[1] + charToAdd
            else:
                app.aetbsStartMonth += charToAdd
        elif (app.aetbsTypingStartDay):
            if (len(app.aetbsStartDay) == 2):
                app.aetbsStartDay = app.aetbsStartDay[1] + charToAdd
            else:
                app.aetbsStartDay += charToAdd
        elif (app.aetbsTypingStartYear):
            if (len(app.aetbsStartYear) == 4):
                app.aetbsStartYear = app.aetbsStartYear[1:] + charToAdd
            else:
                app.aetbsStartYear += charToAdd
        elif (app.aetbsTypingEndMonth):
            if (len(app.aetbsEndMonth) == 2):
                app.aetbsEndMonth = app.aetbsEndMonth[1] + charToAdd
            else:
                app.aetbsEndMonth += charToAdd
        elif (app.aetbsTypingEndDay):
            if (len(app.aetbsEndDay) == 2):
                app.aetbsEndDay = app.aetbsEndDay[1] + charToAdd
            else:
                app.aetbsEndDay += charToAdd
        elif (app.aetbsTypingEndYear):
            if (len(app.aetbsEndYear) == 4):
                app.aetbsEndYear = app.aetbsEndYear[1:] + charToAdd
            else:
                app.aetbsEndYear += charToAdd
        elif (app.aetbsTypingStartTime):
            app.aetbsStartTime += charToAdd
        elif (app.aetbsTypingEndTime):
            app.aetbsEndTime += charToAdd
        elif (app.aetbsTypingLocation):
            app.aetbsLocation += charToAdd
        elif (app.aetbsTypingNotes):
            app.aetbsNotes += charToAdd

def keyPressed(app, event):
    if (app.addingNewPage): keyPressedAddingPage(app, event.key)
    elif (app.addingNewEvent): keyPressedAddingEvent(app, event.key)
    elif (app.addingEventToBeScheduled): keyPressedAddingEventToBeScheduled(app, event.key)

def mouseDragged(app, event):
    if (app.edgeX + 35 < event.x < app.edgeX + 920) and (95 < event.y < 745):
        if (app.drawing):
            app.drawingCoords.extend((event.x, event.y))
        elif (app.shapeDrawing != 'triangle') and (app.shapeDrawing != None):
            if (len(app.drawingCoords) < 4):
                app.drawingCoords.extend((event.x, event.y))
            else:
                app.drawingCoords.pop(-1)
                app.drawingCoords.pop(-1)
                app.drawingCoords.extend((event.x, event.y))
        elif (app.erasing):
            eraseShape(app, event.x, event.y)

def mouseReleased(app, event):
    page = Page.bulletJournal[app.indexPageToDisplay]
    if ((app.edgeX + 35 < event.x < app.edgeX + 920) and (95 < event.y < 745) and 
        (app.shapeDrawing != 'triangle') and (len(app.drawingCoords) > 1)):
        if (app.drawing == True):
            app.drawingCoords.extend((event.x, event.y))
            page.drawings.append(['free draw', copy.copy(app.drawingCoords)])
        elif (app.shapeDrawing != None):
            if (len(app.drawingCoords) == 4):
                app.drawingCoords.pop(-1)
                app.drawingCoords.pop(-1)
            app.drawingCoords.extend((event.x, event.y))
            page.drawings.append([app.shapeDrawing, copy.copy(app.drawingCoords)])
        app.drawingCoords = []

def displayPossibleShapesToDraw(app, canvas):
    x, y = app.shapeButton.getCenterCoords(app)
    canvas.create_rectangle(x, 60, x+110, 160, fill='white')
    canvas.create_line(x+20, 80, x+40, 100)
    canvas.create_rectangle(x+70, 80, x+90, 100)
    canvas.create_oval(x+20, 120, x+40, 140)
    canvas.create_polygon(x+80, 120, x+70, 140, x+90, 140, outline='black', fill='white')

def displayCurrentDrawing(app, canvas):
    if (app.drawing):
        if (len(app.drawingCoords) > 3):
            canvas.create_line(app.drawingCoords, smooth=True, width=2)
    elif (app.shapeDrawing == 'line') and (len(app.drawingCoords) > 3):
        canvas.create_line(app.drawingCoords, width=2)
    elif (app.shapeDrawing == 'rectangle') and (len(app.drawingCoords) > 3):
        canvas.create_rectangle(app.drawingCoords, width=2)
    elif (app.shapeDrawing == 'oval') and (len(app.drawingCoords) > 3):
        canvas.create_oval(app.drawingCoords, width=2)
    elif (app.shapeDrawing == 'triangle'):
        for i in range(0, len(app.drawingCoords), 2):
            x, y = app.drawingCoords[i], app.drawingCoords[i+1]
            canvas.create_oval(x-2, y-2, x+2, y+2, fill='black')
        
def redrawAll(app, canvas):
    Button.drawAllButtons(app, canvas)
    pageToDisplay = Page.bulletJournal[app.indexPageToDisplay]
    pageToDisplay.drawPage(app, canvas)
    if (pageToDisplay.type == 'weekly') and (app.displayEventInfo != None):
        pageToDisplay.displayEventInfo(app, canvas, app.displayEventInfo)
    
    pageToDisplay.createDrawings(app, canvas)
    if (app.drawing) or (app.shapeDrawing != None): displayCurrentDrawing(app, canvas)
    elif (app.displayPossibleShapes): displayPossibleShapesToDraw(app, canvas)

    if (app.addingNewPage): drawAllAddPageButtons(app, canvas)
    elif (app.addingNewEvent): drawAllAddEventButtons(app, canvas)
    elif (app.addingEventToBeScheduled): drawAllAddEventToBeScheduledButtons(app, canvas)

################################################################################
runApp(width=960, height=782)