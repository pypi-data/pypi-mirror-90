import xml.etree.ElementTree as ET
import tkinter as tk
from enum import Enum

class WrongTypeError(Exception):
    pass

class MissingXMLError(Exception):
    pass

class UndefinedError(Exception):
    pass

class ArgumentError(Exception):
    pass

class Event(Enum):
    ON_WINDOW_LOADED = "ON_WINDOW_LOADED"

loaded = []
loaded_paths = []
loaded_tks = []

loaded_wiids = []
loaded_widgets = []

events_windows = []

def add_event_to(windowId,event,function):
    if windowId in loaded:
        if isinstance(windowId,str):
            if isinstance(event,Event):
                if callable(function):
                    events_windows.append({
                        "window": windowId,
                        "event": event,
                        "function": function
                    })
                else:
                    raise ArgumentError("Argument 'function' must be a function")
            else:
                raise WrongTypeError("Argument 'event' must be type of Event, not " + str(type(event).__name__))
        else:
            raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId).__name__))
    else:
        raise UndefinedError("There is no such window with id: '" + str(windowId) + "'")

def change_value_of(windowId,widgetId,item,value):
    if windowId in loaded:
        if isinstance(windowId,str):
            if isinstance(widgetId,str):
                if isinstance(item,str):
                    widget = loaded_widgets[loaded_wiids.index(widgetId)]
                    widget[item] = value
                else:
                    raise WrongTypeError("Argument 'item' must be type of str, not " + str(type(item).__name__))
            else:
                raise WrongTypeError("Argument 'widgetId' must be type of str, not " + str(type(widgetId).__name__))
        else:
            raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId).__name__))
    else:
        raise UndefinedError("There is no such window with id: '" + str(windowId) + "'")

def bind(windowId,widgetId,event,function):
    if windowId in loaded:
        if isinstance(windowId,str):
            if isinstance(widgetId,str):
                if isinstance(event,str):
                    if callable(function):
                        widget = loaded_widgets[loaded_wiids.index(widgetId)]
                        widget.bind(event,function)
                    else:
                        raise ArgumentError("Argument 'function' must be a function")
                else:
                    raise WrongTypeError("Argument 'event' must be type of str, not " + str(type(event).__name__))
            else:
                raise WrongTypeError("Argument 'widgetId' must be type of str, not " + str(type(widgetId).__name__))
        else:
            raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId).__name__))
    else:
        raise UndefinedError("There is no such window with id: '" + str(windowId) + "'")

def add_command_to(windowId,widgetId,function):
    if windowId in loaded:
        if isinstance(windowId,str):
            if isinstance(widgetId,str):
                if callable(function):
                    widget = loaded_widgets[loaded_wiids.index(widgetId)]
                    widget["command"] = function
                else:
                    raise ArgumentError("Argument 'function' must be a function")
            else:
                raise WrongTypeError("Argument 'widgetId' must be type of str, not " + str(type(widgetId).__name__))
        else:
            raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId).__name__))
    else:
        raise UndefinedError("There is no such window with id: '" + str(windowId) + "'")

def hide(windowId):
    if windowId in loaded:
        if isinstance(windowId,str):
            loaded_tks[loaded.index(windowId)].destroy()
        else:
            raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId).__name__))
    else:
        raise UndefinedError("There is no such window with id: '" + str(windowId) + "'")

def load(path):
    if isinstance(path,str):
        tree = ET.parse(path)
        root = tree.getroot()

        try:
            wid = root.attrib["id"]
        except:
            wid = False

        if wid != False:
            loaded.append(wid)
            loaded_paths.append(path)
        else:
            raise MissingXMLError("Tag 'window' is missing attribute 'id'")
    else:
        raise WrongTypeError("Argument 'path' must be type of str, not " + str(type(path).__name__))

def show(windowId):
    if isinstance(windowId,str):
        wid = windowId

        if wid in loaded:
            path = loaded_paths[loaded.index(wid)]

            tree = ET.parse(path)
            root = tree.getroot()

            event_onWindowLoaded = None

            for event in events_windows:
                if event["window"] == wid:
                    if event["event"] == Event.ON_WINDOW_LOADED:
                        event_onWindowLoaded = event["function"]

            exec("global " + wid)
            exec(wid + " = tk.Tk()")
            exec("loaded_tks.append(" + wid + ")")
            try:
                exec(wid + ".title(\"" + root.attrib["title"] + "\")")
            except:
                pass
            try:
                exec(wid + ".geometry(\"" + root.attrib["width"] + "x" + root.attrib["height"] + "\")")
            except:
                pass
            try:
                exec(wid + ".iconbitmap(\"" + root.attrib["icon"] + "\")")
            except:
                pass

            for a in root.attrib:
                if a == "center":
                    exec("width = " + wid + ".winfo_width()")
                    exec("height = " + wid + ".winfo_height()")
                    exec("x = (" + wid + ".winfo_screenwidth() // 2) - (width // 2)")
                    exec("y = (" + wid + ".winfo_screenheight() // 2) - (height // 2)")
                    exec(wid + ".geometry('{}x{}+{}+{}'.format(width, height, x, y))")

            for child in root:
                if child.tag == "config":
                    for con in child:
                        exec(wid + ".config(" + con.tag + "=\"" + con.text + "\")")
                elif child.tag == "overrideredirect":
                    exec(wid + ".overrideredirect(" + child.text + ")")
                elif child.tag == "center":
                    exec("width = " + wid + ".winfo_width()")
                    exec("height = " + wid + ".winfo_height()")
                    exec("x = (" + wid + ".winfo_screenwidth() // 2) - (width // 2)")
                    exec("y = (" + wid + ".winfo_screenheight() // 2) - (height // 2)")
                    exec(wid + ".geometry('{}x{}+{}+{}'.format(width, height, x, y))")
                elif child.tag == "widget":
                    try:
                        name = child.attrib["name"]
                    except:
                        name = False

                    if name != False:
                        try:
                            wiid = child.attrib["id"]
                        except:
                            wiid = False

                        if wiid != False:
                            exec("global " + wiid)

                            args = ""

                            for a in child:
                                if a.tag not in ["grid","command","place"]:
                                    args += a.tag + "=\"" + a.text + "\","

                            args = args[:-1]

                            exec(wiid + " = tk." + name + "(" + args + ")")
                            
                            try:
                                gargs = ""

                                for child2 in child:
                                    if child2.tag == "grid":
                                        grid = child2

                                for a in grid.attrib:
                                    gargs += a + "=\"" + grid.attrib[a] + "\","

                                gargs = gargs[:-1]

                                exec(wiid + ".grid(" + gargs + ")")
                            except:
                                pass

                            try:
                                pargs = ""

                                for child2 in child:
                                    if child2.tag == "place":
                                        place = child2

                                for a in place.attrib:
                                    pargs += a + "=" + place.attrib[a] + ","

                                pargs = pargs[:-1]

                                exec(wiid + ".place(" + pargs + ")")
                            except:
                                pass

                            loaded_wiids.append(wiid)
                            exec("loaded_widgets.append(" + wiid + ")")
                        else:
                            raise MissingXMLError("Tag 'widget' is missing attribute 'id'")
                    else:
                        raise MissingXMLError("Tag 'widget' is missing attribute 'name'")
            
            if event_onWindowLoaded != None:
                event_onWindowLoaded()

            try:
                exec(wid + ".mainloop()")
            except:
                pass
        else:
            raise UndefinedError("There is no such window with the id: '" + wid + "'")
    else:
        raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId).__name__))

class Window:
    def __init__(self,windowId,ignoreUndefined=False):
        if windowId in loaded or ignoreUndefined == True:
            if isinstance(windowId,str):
                self.windowId = windowId
            else:
                raise WrongTypeError("Argument 'windowId' must be type of str, not " + str(type(windowId)).__name__)
        else:
            raise UndefinedError("There is no such window with the id: '" + str(windowId) + "'")

    def get(self):
        return self.windowId

    def hide(self):
        hide(self.windowId)

    def show(self):
        show(self.windowId)

    def add_event(self,event,function):
        add_event_to(self.windowId,event,function)

class Widget:
    def __init__(self,widgetId,ignoreUndefined=False):
        if widgetId in loaded_wiids or ignoreUndefined == True:
            if isinstance(widgetId,str):
                self.widgetId = widgetId
            else:
                raise WrongTypeError("Argument 'widgetId' must be type of str, not " + str(type(widgetId).__name__))
        else:
            raise UndefinedError("There is no such widget with the id: '" + str(widgetId) + "'")
    
    def get(self):
        return self.windowId

    def change_value(self,windowId,item,value):
        change_value_of(windowId,self.widgetId,item,value)

    def bind(self,windowId,event,function):
        bind(windowId,self.widgetId,event,function)

    def add_command(self,windowId,function):
        add_command_to(windowId,self.widgetId,function)