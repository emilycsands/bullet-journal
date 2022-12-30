from cmu_112_graphics import *
from bujo import *
from schedule import *
from event import *
from datetime import timedelta
import datetime
import math

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