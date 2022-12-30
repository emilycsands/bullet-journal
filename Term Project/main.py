from cmu_112_graphics import *
from event import *
from schedule import *
from bujo import *
from buttons import *
from datetime import timedelta
import datetime
import math


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