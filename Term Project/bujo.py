from cmu_112_graphics import *
from event import *
from datetime import timedelta
import datetime
import math

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