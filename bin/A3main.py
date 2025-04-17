# import libvcparser as vcparser
#import the library
from ctypes import *
from functools import partial

import os
import sys
# import mysql.connector
import sqlite3
# import os

import mysql.connector
# import database as db
import datetime
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Print, Background
from asciimatics.renderers import Box, FigletText
from asciimatics.widgets import Text
from asciimatics.widgets import Frame, Button, Layout, Label, Divider
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Print
from asciimatics.renderers import FigletText

from asciimatics.exceptions import ResizeScreenError
from time import sleep


# Define the VCardErrorCode enum as Python constants
OK = 0
INV_FILE = 1
INV_CARD = 2
INV_PROP = 3
INV_DT = 4
WRITE_ERROR = 5
OTHER_ERROR = 6

# /**
#  * Node of a linked list. This list is doubly linked, meaning that it has points to both the node immediately in front 
#  * of it, as well as the node immediately behind it.
#  **/
# typedef struct listNode{
#     void* data;
#     struct listNode* previous;
#     struct listNode* next;
# } Node;

# /**
#  * Metadata head of the list. 
#  * Contains no actual data but contains
#  * information about the list (head and tail) as well as the function pointers
#  * for working with the abstracted list data.
#  **/
# typedef struct listHead{
#     Node* head;
#     Node* tail;
#     int length;
#     void (*deleteData)(void* toBeDeleted);
#     int (*compare)(const void* first,const void* second);
#     char* (*printData)(void* toBePrinted);
# } List;



  


class Node(Structure):
    pass

Node._fields_ = [
        ("data", c_char_p),
        ("previous", POINTER(Node)),
        ("next", POINTER(Node)),
    ]

class ListHead(Structure):
    _fields_ = [
        ("head", POINTER(Node)),
        ("tail", POINTER(Node)),
        ("length", c_int),
        ("deleteData", CFUNCTYPE(None, c_void_p)),
        ("compare", CFUNCTYPE(c_int, c_void_p, c_void_p)),
        ("printData", CFUNCTYPE(c_char_p, c_void_p)),
    ]


class VCardErrorCode(Structure):
    _fields_ = [
        ("OK", c_int),
        ("INV_FILE", c_int),
        ("INV_CARD", c_int),
        ("INV_PROP", c_int),
        ("INV_DT", c_int),
        ("WRITE_ERROR", c_int),
        ("OTHER_ERROR", c_int),
    ]


# Define the DateTime struct
class DateTime(Structure):
    _fields_ = [
        ("UTC", c_bool),
        ("isText", c_bool),
        ("date", c_char_p),
        ("time", c_char_p),
        ("text", c_char_p),
    ]

# Define the Parameter struct
class Parameter(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("value", c_char_p),
    ]

# Define the Property struct
class Property(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("group", c_char_p),
        ("parameters", POINTER(ListHead)),  # Pointer to a List of Parameter
        ("values", POINTER(ListHead)),      # Pointer to a List of char*
    ]

# Define the Card struct
class Card(Structure):
    _fields_ = [
        ("fn", POINTER(Property)),  # Pointer to a Property
        ("optionalProperties", POINTER(ListHead)),  # Pointer to a List of Property
        ("birthday", POINTER(DateTime)),  # Pointer to a DateTime
        ("anniversary", POINTER(DateTime)),  # Pointer to a DateTime
    ]
    

   
libPath = './libvcparser.so'

libvcparser = CDLL(libPath)

errorCode = (POINTER(VCardErrorCode))
generateCard = libvcparser.createCard
generateCard.argtypes = [c_char_p, (POINTER(Card))]
generateCard.restype = c_int       # Returns VCardErrorCode
# libvcparser.createCard.argtypes = [c_char_p, POINTER(POINTER(Card))]
# libvcparser.createCard.restype = c_int  # Returns VCardErrorCode

# # Define the deleteCard function
# libvcparser.deleteCard.argtypes = [POINTER(Card)]
# libvcparser.deleteCard.restype = None
# # Define the cardToString function
# libvcparser.cardToString.argtypes = [POINTER(Card)]
# libvcparser.cardToString.restype = c_char_p
# # Define the errorToString function
# libvcparser.errorToString.argtypes = [c_int]
# libvcparser.errorToString.restype = c_char_p

def dummy_delete_data(to_be_deleted):
    pass

def dummy_compare(first, second):
    return 0

def dummy_print_data(to_be_printed):
    return b""

delete_data_func = CFUNCTYPE(None, c_void_p)(dummy_delete_data)
compare_func = CFUNCTYPE(c_int, c_void_p, c_void_p)(dummy_compare)
print_data_func = CFUNCTYPE(c_char_p, c_void_p)(dummy_print_data)


# Define the writeCard function
writingCard = libvcparser.writeCard
writingCard.argtypes = [ c_char_p, (POINTER(Card))]
writingCard.restype = c_int  # Returns VCardErrorCode

# Define the validateCard function
validateCard = libvcparser.validateCard
validateCard.argtypes = [POINTER(Card)]
validateCard.restype = c_int  # Returns VCardErrorCode

length_of_optional_properties = libvcparser.getLength
length_of_optional_properties.argtypes = [POINTER(ListHead)]
length_of_optional_properties.restype = c_int


def on_createOk_click(screen, layout, frame, card_ptr, contact_name, filename,cursor,duplicate,connection):
    # Get the updated contact name from the Text widget
    updated_name = contact_name.value  # Retrieve the updated name from the Text widget
    filename = filename.value
    
    if not updated_name or not filename or (not filename.endswith(".vcf") and not filename.endswith(".vcard")):
        layout.add_widget(Label(f"{updated_name}"), 1)
        layout.add_widget(Label(f"{filename}"), 1)
        
        layout.add_widget(Label("Error: Contact name or filename cannot be empty or invalid."), 1)
        screen.refresh()
        frame.fix()  # Fix the layout
        return
    
    card_ptr.contents.fn.contents.name = c_char_p("FN".encode('utf-8'))
    card_ptr.contents.fn.contents.values = POINTER(ListHead)()
    card_ptr.contents.fn.contents.values.contents = ListHead()
    card_ptr.contents.fn.contents.values.contents.head = POINTER(Node)()
    card_ptr.contents.fn.contents.values.contents.head.contents = Node()
    card_ptr.contents.fn.contents.values.contents.head.contents.data = c_char_p(updated_name.encode('utf-8'))
    # card_ptr.contents.fn.contents.values.contents.head.contents.next = None
    # card_ptr.contents.fn.contents.values.contents.head.contents.previous = None
    
    card_ptr.contents.birthday = None
    card_ptr.contents.anniversary = None
    card_ptr.contents.optionalProperties = POINTER(ListHead)()
    card_ptr.contents.optionalProperties.contents = ListHead()
    card_ptr.contents.optionalProperties.contents.head = None
    card_ptr.contents.optionalProperties.contents.tail = None
    card_ptr.contents.optionalProperties.contents.length = 0
    card_ptr.contents.optionalProperties.contents.deleteData = delete_data_func  # Assign the dummy function
    card_ptr.contents.optionalProperties.contents.compare = compare_func  # Assign the dummy function
    card_ptr.contents.optionalProperties.contents.printData = print_data_func  # Assign the dummy function


    file_to_be_changed = f"./cards/{filename}".encode('utf-8')
      # Prepare the file path
    # file_to_be_changed = f"./cards/{filename}".encode('utf-8')
    if os.path.exists(file_to_be_changed.decode('utf-8')):
        layout.add_widget(Label(f"Error: File '{filename}' already exists."), 1)
        screen.refresh()
        frame.fix()
        return
  
     # Write the updated card to the file
    result = writingCard(file_to_be_changed, card_ptr)
    
    if result == OK:
        layout.add_widget(Label("Card written successfully!"), 1)
    else:
        layout.add_widget(Label(f"Error writing card: {result}"), 1)

    # Refresh the screen and fix the frame layout
    screen.refresh()
    frame.fix()  # Fix the frame layout
    List_view(screen, frame, layout,cursor,duplicate,connection)
        # layout.add_widget(Label("Card written successfully!"), 1)
  
       
  



def on_fileOk_click(screen, fileLayout, fileFrame, card_ptr, contact_name, filename,cursor,duplicate, connection):
    # Get the updated contact name from the Text widget
   
    updated_name = contact_name.value  # Retrieve the updated name from the Text widget
    if not updated_name:
        # screen.refresh()
        fileLayout.add_widget(Label("Error: Contact name cannot be empty."), 1)
        screen.clear()
        fileFrame.fix()
        return
    # card_ptr.contents.fn.contents.values = POINTER(ListHead)()
    # card_ptr.contents.fn.contents.values.contents = ListHead()
    # card_ptr.contents.fn.contents.values.contents.head = POINTER(Node)()
    # card_ptr.contents.fn.contents.values.contents.head.contents = Node()
    card_ptr.contents.fn.contents.values.contents.head.contents.data = c_char_p(updated_name.encode('utf-8'))
    # card_ptr.contents.fn.contents.values.contents.head.contents.next = None
    # card_ptr.contents.fn.contents.values.contents.head.contents.previous = None
    
        

    file_to_be_changed = f"./cards/{filename}".encode('utf-8')
    if not os.path.exists(file_to_be_changed.decode('utf-8')):
        print(f"Error: File path does not exist: {file_to_be_changed.decode('utf-8')}")
        return

    # print(f"File name: {file_to_be_changed}".encode('utf-8'))
    # print(f"Card pointer: {card_ptr}")
    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if cursor != None and connection:
        string1 = f"UPDATE FILE SET last_modified = '{currentTime}' WHERE file_name = '{filename}'"
        cursor.execute(string1)    
        string1 = f"select file_id from FILE where file_name = '{filename}'"
        cursor.execute(string1)
        result = cursor.fetchone()
        if not result:
            print("File ID not found")
            return
        file_id = result[0]
        # file_id = cursor.fetchone()[0]
        # fileLayout.add_widget(Label("f{file_id}"), 1)
        if not file_id:
            print("File ID not found")
            return
        string1 = f"update CONTACT set name = '{updated_name}' where file_id = '{file_id}'"        
        cursor.execute(string1)
    result = writingCard(file_to_be_changed, card_ptr)
    # print(f"Updatedsdf name: {updated_name}")
    # result = OK;
    if result == OK:
        screen.refresh()
        fileFrame.fix() # Fix the layout        
        List_view(screen, fileFrame, fileLayout,cursor,duplicate, connection)
    else:
        fileLayout.add_widget(Label(f"Error writing card: {result}"), 1)
        screen.refresh()
        fileFrame.fix() # Fix the layout        
        List_view(screen, fileFrame, fileLayout,cursor,duplicate, connection)
    
    
def on_create_click(screen, frame, layout, card_ptr,cursor,duplicate,connection):
    screen.clear()
    frame._layouts.clear()
    frame._effects.clear()
    frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="Create Frame")
    layout = Layout([1,1,1,1], fill_frame=True)
    frame.add_layout(layout)

    layout.add_widget(Label(""),0)
    layout.add_widget(Label("Create vCard!"),1)
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    layout.add_widget(Label(""),0)
    layout.add_widget(Label(""),1)
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    layout.add_widget(Label("Enter the file name:"),0)
    new_file = Text("")
    layout.add_widget(new_file,1)
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    layout.add_widget(Label("Enter Contact name:"),0)
    new_name = Text("")
    layout.add_widget(new_name,1)
    
    screen.refresh()


    BoxLayout = Layout([1, 1, 1, 1])
    frame.add_layout(BoxLayout)
    # Initialize the card_ptr
    

    

    # Allocate memory for the values field
   
    BoxLayout.add_widget(Button("OK", partial(on_createOk_click,screen, layout, frame, card_ptr, new_name, new_file, cursor,duplicate,connection )), 0)  # Button with callback
    BoxLayout.add_widget(Button("Cancel", partial(List_view, screen, frame, layout, cursor, duplicate, connection)), 1)  # Button with callback
    screen.refresh()
    frame.fix()
    scene = Scene([frame], duration=-1)
    screen.play([scene])
    screen.refresh()
    




    print("Create button clicked!")

def on_edit_click(cursor):
    # print("Edit button clicked!")
    pass

def display_all_contacts(screen, frame, layout, card_ptr,cursor,duplicate, connection):
    if cursor == None and connection == None:
        return
    
    
    screen.clear()
    # frame._layouts.clear()
    # frame._effects.clear()
    frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="All Contacts Frame")
    layout = Layout([2,2,2,2,2], fill_frame=True)
    frame.add_layout(layout)
    layout.add_widget(Label("All Contacts!"),1)
    layout.add_widget(Label(""),0)
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    layout.add_widget(Label(""),4)
    layout.add_widget(Label(""),0)
    layout.add_widget(Label(""),1)
    
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    layout.add_widget(Label(""),4)
    cursor.execute("SELECT * FROM CONTACT ORDER BY name")
    contacts = cursor.fetchall()
    for contact in contacts:
        contact_id = contact[0]
        contact_name = contact[1]
        birthday = contact[2]
        anniversary = contact[3]
        file_id = contact[4]
        query = f"SELECT file_name FROM FILE WHERE file_id = {file_id} "  # Query to get the file name
        cursor.execute(query)
        file_name = cursor.fetchone()[0]
         # Truncate text if necessary to fit within the Label
        # contact_name = (contact_name[:20] + "...") if len(contact_name) > 20 else contact_name
        # birthday = (birthday[:20] + "...") if birthday and len(birthday) > 20 else birthday
        # anniversary = (anniversary[:20] + "...") if anniversary and len(anniversary) > 20 else anniversary
        # file_name = (file_name[:20] + "...") if len(file_name) > 20 else file_name

        # Add contact details to the layout
        layout.add_widget(Label(f"Contact ID: {contact_id}"), 0)
        layout.add_widget(Label(f"FN: {contact_name}"), 1)
        layout.add_widget(Label(f"BDAY: {birthday}"), 2)
        layout.add_widget(Label(f"ANNIVERSARY: {anniversary}"), 3)
        layout.add_widget(Label(f"File Name: {file_name}"), 4)

    BoxLayout = Layout([1, 1, 1, 1])
    frame.add_layout(BoxLayout)
    BoxLayout.add_widget(Button("OK", partial(List_view,screen, frame, layout, cursor, duplicate,connection)), 0)  # Button with callback
    BoxLayout.add_widget(Button("Cancel", partial(List_view,screen, frame, layout, cursor, duplicate, connection)), 1)  # Button with callback
    screen.refresh()
    frame.fix()
    scene = Scene([frame], duration=-1)
    screen.play([scene])
    screen.refresh()
    # print("Display all button clicked!")
    

def born_in_june(screen, frame, layout, card_ptr,cursor,duplicate, connection):
    if cursor == None and connection == None:
        return
    
    screen.clear()
    # frame._layouts.clear()
    # frame._effects.clear()
    frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="Born in June Frame")
    layout = Layout([1,1,1,1], fill_frame=True)
    frame.add_layout(layout)
    layout.add_widget(Label("Contacts born in June!"),1)
    layout.add_widget(Label(""),0)
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    layout.add_widget(Label(""),0)
    layout.add_widget(Label(""),1)
    
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)
    # layout.add_widget(Label(""),4)
    cursor.execute("SELECT * FROM CONTACT WHERE MONTH(birthday) = 6 ORDER BY birthday")
    contacts = cursor.fetchall()
    for contact in contacts:
        
        contact_name = contact[1]
        birthday = contact[2]
         # Truncate text if necessary to fit within the Label
        # contact_name = (contact_name[:20] + "...") if len(contact_name) > 20 else contact_name
        # birthday = (birthday[:20] + "...") if birthday and len(birthday) > 20 else birthday
        # anniversary = (anniversary[:20] + "...") if anniversary and len(anniversary) > 20 else anniversary
        # file_name = (file_name[:20] + "...") if len(file_name) > 20 else file_name

        # Add contact details to the layout
        # layout.add_widget(Label(f"Contact ID: {contact_id}"), 0)
        layout.add_widget(Label(f"FN: {contact_name}"), 1)
        layout.add_widget(Label(f"BDAY: {birthday}"), 2)
        # layout.add_widget(Label(f"ANNIVERSARY: {anniversary}"), 3)
        # layout.add_widget(Label(f"File Name: {file_name}"), 4)
        
    BoxLayout = Layout([1, 1, 1, 1])
    frame.add_layout(BoxLayout)
    BoxLayout.add_widget(Button("OK", partial(List_view,screen, frame, layout, cursor, duplicate, connection)), 0)  # Button with callback
    BoxLayout.add_widget(Button("Cancel", partial(List_view,screen, frame, layout, cursor, duplicate, connection)), 1)  # Button with callback
    screen.refresh()
    frame.fix()
    scene = Scene([frame], duration=-1)
    screen.play([scene])
    screen.refresh()
    # print("Born in June button clicked!")

def on_db_queries_click(screen, frame, layout, card_ptr,cursor, duplicate, connection):
    if cursor == None and  not connection :
        return
    screen.clear()
    
    frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="DB Queries Frame")
    layout = Layout([1,1,1], fill_frame=True)
    frame.add_layout(layout)
    box_layout = Layout([1,1,1,1])
    frame.add_layout(box_layout)
    box_layout.add_widget(Button("Display all contacts", partial(display_all_contacts, screen, frame, layout, card_ptr,cursor, duplicate, connection)), 0)
    box_layout.add_widget(Button("Find contacts born in June", partial(born_in_june, screen, frame, layout, card_ptr,cursor, duplicate, connection)), 1)
    box_layout.add_widget(Button("Cancel", partial(List_view,screen, frame, layout, cursor, duplicate, connection )), 2)
    # print("DB Queries button clicked!")
    screen.refresh()
    frame.fix()
    scene = Scene([frame], duration=-1)
    screen.play([scene])
    
    

def on_exit_click(cursor):
    if cursor:
        cursor.execute("DROP TABLE IF EXISTS CONTACT")
        cursor.execute("DROP TABLE IF EXISTS FILE")
        cursor.close()
    sys.exit()
def on_file_click(file, screen, fileFrame, fileLayout,card_ptr,cursor,duplicate, connection):
        screen.clear()
        fileLayout.clear_widgets()
        fileFrame._layouts.clear()
        fileFrame._effects.clear()
        fileFrame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="File Frame")
        fileLayout = Layout([1,1,1], fill_frame=True)
        fileFrame.add_layout(fileLayout)
        fileLayout.add_widget(Label("vCard details!"),1)
        fileLayout.add_widget(Label(""),1)
        fileLayout.add_widget(Label(""),0)
        fileLayout.add_widget(Label(""),0)
        fileLayout.add_widget(Label(""),2)
        fileLayout.add_widget(Label(""),2)
#    card_ptr = POINTER(Card)()  # Correctly initialize as a pointer to a Card object
#    card_ptr.contents = Card()  # Allocate memory for the Card structure
#    filename = f"../bin/cards/{file}"
#    # Call the createCard function
#    result = generateCard(c_char_p(filename.encode('utf-8')), POINTER(Card)(card_ptr))
#    # # Call the validateCard function
#    result = validateCard(card_ptr)
# #    fileLayout.add_widget(Label(f"File name: {file.encode('utf-8')}"),0)
#    # Check the result of generateCard
#    if result == OK:
        fileLayout.add_widget(Label("File name:"), 0)
        fileLayout.add_widget(Label(f"{file}"), 1)
        # print("Card created successfully!")
        property = POINTER(Property)()
        # values = POINTER(ListHead)()
        # Access the FN property
        property = card_ptr.contents.fn
        # print(f"fn: {property.contents.name.decode('utf-8')}")
        data = (property.contents.values.contents.head.contents.data)
        fileLayout.add_widget(Label("Contact:" ), 0)
        # Decode the C string to a Python string
        contact_name_value = cast(data, c_char_p).value.decode('utf-8')

# Create a Text widget and set its value
        contact_name = Text()
        contact_name.value = contact_name_value

        # Add the Text widget to the layout
        fileLayout.add_widget(contact_name, 1)

      

        # Check if the BDAY property is valid
        if card_ptr.contents.birthday:
            bday_property = card_ptr.contents.birthday.contents
            if bday_property.text:
                bday_text = bday_property.text.decode('utf-8')
                fileLayout.add_widget(Label(f"Birthday: "), 0)
                fileLayout.add_widget(Label(f"{bday_text}"), 1)
            elif bday_property.date and bday_property.time:
                bday_time = bday_property.time.decode('utf-8')
                bday_date = bday_property.date.decode('utf-8')
                fileLayout.add_widget(Label(f"Birthday:"), 0)
                fileLayout.add_widget(Label(f"Date:{bday_date} Time:{bday_time}"), 1)
            elif bday_property.date and not bday_property.time:
                bday_date = bday_property.date.decode('utf-8')
                fileLayout.add_widget(Label(f"Birthday:"), 0)
                fileLayout.add_widget(Label(f"{bday_date}"), 1)
            elif bday_property.time and not bday_property.date:
                bday_time = bday_property.time.decode('utf-8')
                fileLayout.add_widget(Label(f"Birthday:"), 0)
                fileLayout.add_widget(Label(f"{bday_time}"), 1)
                
            elif bday_property.UTC:                
                fileLayout.add_widget(Label("Birthday: "), 0)
                fileLayout.add_widget(Label(" "), 1)
                            
        else:
            fileLayout.add_widget(Label("Birthday: "), 0)
            fileLayout.add_widget(Label(""), 1)
        
        # Check if the ANNIVERSARY property is valid
        if card_ptr.contents.anniversary:
            anniversary_property = card_ptr.contents.anniversary.contents
            if anniversary_property.text:
                annv_text = anniversary_property.text.decode('utf-8')
                fileLayout.add_widget(Label(f"Anniversary: "), 0)
                fileLayout.add_widget(Label(f"{annv_text}"), 1)
            elif anniversary_property.date and anniversary_property.time:
                annv_time = anniversary_property.time.decode('utf-8')
                annv_date = anniversary_property.date.decode('utf-8')
                fileLayout.add_widget(Label(f"Anniversary:"), 0)
                fileLayout.add_widget(Label(f"Date:{annv_date} Time:{annv_time}"), 1)
            elif anniversary_property.date and not anniversary_property.time:
                fileLayout.add_widget(Label(f"Anniversary:"), 0)
                fileLayout.add_widget(Label(f"{annv_date}"), 1)
            elif anniversary_property.time and not anniversary_property.date:
                annv_time = anniversary_property.time.decode('utf-8')
                fileLayout.add_widget(Label(f"Anniversary:"), 0)
                fileLayout.add_widget(Label(f"{annv_time}"), 1)
                
            elif anniversary_property.UTC:                
                fileLayout.add_widget(Label("Anniversary: "), 0)
                fileLayout.add_widget(Label(" "), 1)
                            
        else:
            fileLayout.add_widget(Label("Anniversary: "), 0)
            fileLayout.add_widget(Label(""), 1)
            

        #Check if there are optional properties
        
        if card_ptr.contents.optionalProperties:
        # count the number of optional properties
            optional_properties = card_ptr.contents.optionalProperties
            # fileLayout.add_widget(Label(f"Optional properties:{optional_properties.contents}"), 0)
            count = length_of_optional_properties(optional_properties.contents)
            # while optional_properties[count]:
            #     count += 1
            fileLayout.add_widget(Label("Optional properties:"), 0)  
            fileLayout.add_widget(Label(f"{count}"), 1)       
            
            
               
        screen.refresh()
        BoxLayout = Layout([2,2])
       
        # fileLayout.add_widget(Label(""), 1)
        
        fileFrame.add_layout(BoxLayout)
        BoxLayout.add_widget(Button("OK", partial (on_fileOk_click, screen, fileLayout, fileFrame, card_ptr, contact_name, file,cursor,duplicate, connection)), 0)  # Button with callback
        BoxLayout.add_widget(Button("Cancel", partial(List_view, screen, fileFrame, fileLayout, cursor,duplicate, connection)), 1)  # Button with callback
        BoxLayout.add_widget(Divider(),0)
        BoxLayout.add_widget(Divider(),1)
        screen.refresh()
    
    #    if result == OK:
    #        print("Card is valid!")
    #    else:
    #        print(f"Error validating card: {result}")
    # screen.refresh();
        fileFrame.fix()
        scene = Scene([fileFrame], duration=-1)

    # Play the scene
        screen.play([scene])
   
def List_view(screen, frame, layout, cursor,duplicate, connection):
    screen.clear()
  
   
    # dir_list = os.listdir("./cards")
    frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="Main Frame")
    layout = Layout([2,2,2,2], fill_frame=True)
    frame.add_layout(layout)
    layout.add_widget(Label("vCard List view!"),1)
    layout.add_widget(Label(""),0)
        # layout.add_widget(Label(""))
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),3)


    layout.add_widget(Divider(),0)
    layout.add_widget(Divider(),1)
    layout.add_widget(Divider(),2)
    layout.add_widget(Divider(),3)

    dir_list = os.listdir("./cards")
    if not dir_list:
                # layout.add_widget(Label("No vCard files found!"), 1)
                card_ptr = None
                card_ptr = POINTER(Card)()
                card_ptr.contents = Card()  # Allocate memory for the Card structure

                # # Allocate memory for the fn field
                card_ptr.contents.fn = POINTER(Property)()
                card_ptr.contents.fn.contents = Property()  # Allocate memory for the Property structure

                card_ptr.contents.fn.contents.values = POINTER(ListHead)()
                card_ptr.contents.fn.contents.values.contents = ListHead()
                card_ptr.contents.fn.contents.values.contents.head = POINTER(Node)()
                card_ptr.contents.fn.contents.values.contents.head.contents = Node()
                card_ptr.contents.fn.contents.values.contents.head.contents.data = c_char_p("".encode('utf-8'))
                card_ptr.contents.fn.contents.values.contents.head.contents.next = None
                card_ptr.contents.fn.contents.values.contents.head.contents.previous = None
                card_ptr.contents.birthday = None
                card_ptr.contents.anniversary = None
                card_ptr.contents.optionalProperties = POINTER(ListHead)()
                card_ptr.contents.optionalProperties.contents = ListHead()
                card_ptr.contents.optionalProperties.contents.head = None
                card_ptr.contents.optionalProperties.contents.tail = None
                card_ptr.contents.optionalProperties.contents.length = 0
                card_ptr.contents.optionalProperties.contents.deleteData = delete_data_func  # Assign the dummy function
                card_ptr.contents.optionalProperties.contents.compare = compare_func  # Assign the dummy function
                card_ptr.contents.optionalProperties.contents.printData = print_data_func  # Assign the dummy function

                

    
    else:
        # if not duplicate:
        for file in dir_list:
                fname = f"{file}" 
                # Check if the file already exists in the FILE table
                card_ptr = None
                card_ptr = POINTER(Card)()
                card_ptr.contents = Card()  # Allocate memory for the Card structure

                # # Allocate memory for the fn field
                card_ptr.contents.fn = POINTER(Property)()
                card_ptr.contents.fn.contents = Property()  # Allocate memory for the Property structure

                card_ptr.contents.fn.contents.values = POINTER(ListHead)()
                card_ptr.contents.fn.contents.values.contents = ListHead()
                card_ptr.contents.fn.contents.values.contents.head = POINTER(Node)()
                card_ptr.contents.fn.contents.values.contents.head.contents = Node()
                card_ptr.contents.fn.contents.values.contents.head.contents.data = c_char_p("".encode('utf-8'))
                card_ptr.contents.fn.contents.values.contents.head.contents.next = None
                card_ptr.contents.fn.contents.values.contents.head.contents.previous = None
                card_ptr.contents.birthday = None
                card_ptr.contents.anniversary = None
                card_ptr.contents.optionalProperties = POINTER(ListHead)()
                card_ptr.contents.optionalProperties.contents = ListHead()
                card_ptr.contents.optionalProperties.contents.head = None
                card_ptr.contents.optionalProperties.contents.tail = None
                card_ptr.contents.optionalProperties.contents.length = 0
                card_ptr.contents.optionalProperties.contents.deleteData = delete_data_func  # Assign the dummy function
                card_ptr.contents.optionalProperties.contents.compare = compare_func  # Assign the dummy function
                card_ptr.contents.optionalProperties.contents.printData = print_data_func  # Assign the dummy function

                
                # Check the result of generateCard
                filename = f"../bin/cards/{file}"
                # Call the createCard function
                result = generateCard(c_char_p(filename.encode('utf-8')), POINTER(Card)(card_ptr))
                # # Call the validateCard function
                result = validateCard(card_ptr)
                #    fileLayout.add_widget(Label(f"File name: {file.encode('utf-8')}"),0)
                
                last_modified = datetime.datetime.fromtimestamp(os.path.getctime(f"./cards/{file}"))
                creation_time = datetime.datetime.fromtimestamp(os.path.getctime(f"./cards/{file}"))
                
                if result==OK and connection and cursor != None:
                    # File already exists, get its file_id
                    
                    # File does not exist, insert it into the FILE table
                    checkFile = f"SELECT file_name FROM FILE WHERE file_name = '{fname}'"
                    cursor.execute(checkFile)
                    if cursor.fetchone():
                        # print(f"File '{fname}' already exists in the database.")
                        pass
                    else:
                        insert_file_query = "INSERT INTO FILE (file_name, last_modified, creation_time) VALUES (%s, %s, %s)"
                        cursor.execute(insert_file_query, (fname, last_modified, creation_time))
                        file_id = cursor.lastrowid  # Get the newly inserted file_id
                        # print(f"File '{fname}' inserted into the database with file_id {file_id}.")
                        
                        # Initialize birthday and anniversary as None
                        birthday = None
                        anniversary = None

                        # Check if the birthday property exists and is valid
                        if card_ptr.contents.birthday:
                            bday_property = card_ptr.contents.birthday.contents
                            if bday_property.date and bday_property.time:
                                bday_date = bday_property.date.decode('utf-8')
                                bday_date = datetime.datetime.strptime(bday_date, '%Y%m%d').strftime('%Y-%m-%d')
                                bday_time = bday_property.time.decode('utf-8')
                                bday_time = datetime.datetime.strptime(bday_time, '%H%M%S').strftime('%H:%M:%S')
                                birthday = f"{bday_date} {bday_time}"  # Combine date and time into DATETIME format
                            

                        # Check if the anniversary property exists and is valid
                        if card_ptr.contents.anniversary:
                            annv_property = card_ptr.contents.anniversary.contents
                            if annv_property.date and annv_property.time:
                                    annv_date = annv_property.date.decode('utf-8')
                                    annv_date = datetime.datetime.strptime(annv_date, '%Y%m%d').strftime('%Y-%m-%d')  # Convert to 'YYYY-MM-DD'

                                    # Decode and handle the time in 'HHMMSS' format
                                    annv_time = annv_property.time.decode('utf-8')
                                    annv_time = datetime.datetime.strptime(annv_time, '%H%M%S').strftime('%H:%M:%S')  # Convert to 'HH:MM:SS'

                                    # Combine date and time into a single DATETIME string
                                    anniversary = f"{annv_date} {annv_time}"  # Combine date and time into DATETIME format
                        
                        insert_contact_query = "INSERT INTO CONTACT (name, birthday, anniversary, file_id) VALUES (%s, %s, %s, %s)"
                        cursor.execute(insert_contact_query, (card_ptr.contents.fn.contents.values.contents.head.contents.data.decode('utf-8') , birthday, anniversary, file_id))
                        
                
                        
                layout.add_widget(Button(f"{file}", partial(on_file_click, file, screen, frame, layout, card_ptr, cursor,duplicate, connection)))  # Use partial to pass arguments
            # print(f"File name: {file}")
            # print(f"Last modified: {last_modified}")
            # print(f"Creation time: {creation_time}")
        duplicate = True
        
        
    BoxLayout = Layout([1, 1, 1, 1])
    frame.add_layout(BoxLayout)
    BoxLayout.add_widget(Button("Create", partial(on_create_click, screen, frame, layout, card_ptr,cursor, duplicate, connection) ), 0)  # Button with callback
    BoxLayout.add_widget(Button("Edit", partial(on_edit_click,cursor)),1)      # Button with callback
    BoxLayout.add_widget(Button("DB Queries", partial(on_db_queries_click,screen, frame, layout, card_ptr,cursor, duplicate, connection)),2)  # Button with callback
    BoxLayout.add_widget(Button("Exit", partial(on_exit_click,cursor)),3)      # Button with callback
    BoxLayout.add_widget(Divider(),0)
    BoxLayout.add_widget(Divider(),1)
    BoxLayout.add_widget(Divider(),2)
    BoxLayout.add_widget(Divider(),3)
    frame.fix()
    scene = Scene([frame], duration=-1)
    screen.play([scene])
    screen.refresh()
  
def vcardDetails(uName, passwd, dbName, screen, frame, layout):
    
        # Get the updated values from the Text widgets
        uName = uName.value.strip()
        passwd = passwd.value.strip()
        dbName = dbName.value.strip()
    
   
        # if dbName == "dkumar07" and uName== "dkumar07" and passwd == "1306900":
        # screen.clear()
        # frame._layouts.clear()
        # frame.layout.clear_widgets()
        # frame._effects.clear()
        # screen.clear()
        # dbName = "dkumar07"
        # uName = "dkumar07"
        # passwd = "1306900"

        try:
            conn = mysql.connector.connect(host="dursley.socs.uoguelph.ca", database=dbName, user=uName, password=passwd)
        except mysql.connector.Error as err:
            screen.clear()
            frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="Alert Frame")
            layout = Layout([1], fill_frame=True)
            frame.add_layout(layout)

            # Add an alert message
            layout.add_widget(Label("Invalid login credentials! Please try again."))

            # Add a "Try Again" button
            layout.add_widget(Button("Try Again", partial(demo, screen)))

            frame.fix()
            scene = Scene([frame], duration=-1)

            # Play the scene
            screen.play([scene])

        # Configure SQL to automatically commit every change (insert/update/delete)
        conn.autocommit = True

        # Prepare a cursor object using cursor() method
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS CONTACT")
        cursor.execute("DROP TABLE IF EXISTS FILE")
    
        create_file_table = "CREATE TABLE IF NOT EXISTS FILE (file_id INT AUTO_INCREMENT PRIMARY KEY,file_name VARCHAR(60) NOT NULL,last_modified DATETIME,creation_time DATETIME NOT NULL)"
        cursor.execute(create_file_table) 
        
        # Create the CONTACT table
        create_contact_table = """
        CREATE TABLE IF NOT EXISTS CONTACT (contact_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(256) NOT NULL,birthday VARCHAR(256),anniversary VARCHAR(256),file_id INT NOT NULL,FOREIGN KEY (file_id) REFERENCES FILE(file_id) ON DELETE CASCADE );
        """
        cursor.execute(create_contact_table)
        connection  = True
        duplicate = False
        List_view(screen, frame, layout, cursor,duplicate, connection)
        

        

def demo(screen):
   
    # frame.layout.clear_widgets()
    # frame._layouts.clear()
    # frame._effects.clear()
    # screen.clear()
    
       
    
    effect = [
    Background(screen, bg=7),  # Use 'bg' instead of 'colour'
    ]
    
    
    
    frame = Frame(screen, height=screen.height, width=screen.width, has_border=True, name="Main Frame")
    layout = Layout([1,1,1], fill_frame=True)
    frame.add_layout(layout)
    layout.add_widget(Label("Login Page"),1)
    
    # layout.add_widget(Divider(),0)
    # layout.add_widget(Divider(),1)
    # # layout.add_widget(Divider(),2)
    # layout.add_widget(Divider(),3)

    
    layout.add_widget(Label(""),0)
    # layout.add_widget(Label(""),1)
    layout.add_widget(Label(""),2)
    layout.add_widget(Label(""),0)
    layout.add_widget(Label(""),1)
    
    layout.add_widget(Label(""),2)
    # layout.add_widget(Label(""),3)
    
    layout.add_widget(Label("Username: "),0)
    uName = Text("")
    layout.add_widget(uName,1)
    layout.add_widget(Label(""),2)
    # layout.add_widget(Label(""),3)
    
    layout.add_widget(Label("Password: "),0)
    passwd = Text("")
    layout.add_widget(passwd,1)
    layout.add_widget(Label(""),2)
    # layout.add_widget(Label(""),3)
    
    layout.add_widget(Label("DbName: "),0)
    dbName = Text("")
    layout.add_widget(dbName,1)
    # layout.add_widget(Label(""),1)
    layout.add_widget(Label(""),2)
    # layout.add_widget(Label(""),3)
    
    BoxLayout = Layout([1, 1])

    frame.add_layout(BoxLayout)
    
  

   
    BoxLayout.add_widget(Button("OK", partial(vcardDetails, uName, passwd, dbName, screen, frame, layout) ), 0)

    # BoxLayout.add_widget(Button("OK", partial(on_exit_click), 0))  # Button with callback
    BoxLayout.add_widget(Button("Cancel", partial(List_view ,screen, frame, layout, cursor=None,duplicate=None, connection=False)),1)      # Button with callback
   
    BoxLayout.add_widget(Divider(),0)
    BoxLayout.add_widget(Divider(),1)
   
    
    frame.fix()
    scene = Scene([frame], duration=-1)

    # Play the scene
    screen.play([scene])
    
    
    


if __name__ == "__main__":
    Screen.wrapper(demo)
    # demo(Screen)
# demo(Screen)