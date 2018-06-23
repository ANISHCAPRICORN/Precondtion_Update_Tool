'''
Doxygen Comments Generator
--------------------------
Author  :   Anish Kumar
Date    :   23/06/2018
'''

import time
import re
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox


Str = '''*********************************************************
*   Program         : Doxygen Comments Generator          
*   Version         : 1.1                               
*   Developer       : Anish Kumar                       
*   Date And Time   : {}                                          
*********************************************************\
'''.format(time.asctime())
COU_TEST_Count = 0
COU_TEST_Flag, COU_CALL_Flag, Assert_Print_Flag, Event_Print_Flag = 0, 0, 0, 0
ASSERT_Missing = 0
Missed_Asserts = []
Asserts = []
Events = []
Order_Check_Flag = 0  #
COU_SET_Count, COU_CALL_Count, COU_ASSERT_Count, COU_TEST_Count = 0, 0, 0, 0
Num_Lines = 0


def event_updater():
    global Event_Print_Flag
    global Events
    if Event_Print_Flag:
        dest.write("\n@events\n")
        Event_Print_Flag = 0
        Events = set(Events)
        for i in Events:
            print(i)
            dest.write('\t')
            dest.write(i)
            dest.write('\n')
        Events = []


def results_updater():
    global Assert_Print_Flag
    global Asserts
    if Assert_Print_Flag:
        dest.write("\n@results\n")
        Assert_Print_Flag = 0
        Asserts = set(Asserts)
        for i in Asserts:
            print(i)
            if i != '\n*':
                dest.write('\t')
            dest.write(i)
            if i != '\n*':
                dest.write('\n')
        Asserts = []


def generator():
    global COU_TEST_Count, ASSERT_Missing, Missed_Asserts, Order_Check_Flag, TEST_CASE_Name, COU_ASSERT_Count
    global dest, COU_CALL_Flag, COU_TEST_Flag, COU_SET_Count, COU_CALL_Count, Event_Print_Flag, Assert_Print_Flag
    global Num_Lines
    # Loop Starts here
    with open(filepath) as fp:
        # Reading Line by Line
        dest.write(Str)
        line = fp.readline()
        while line:
            ch = (line.strip())
            ''' 
            ==============================================================================
                                COU_TEST IDENTIFICATION
            ==============================================================================
            '''
            while ch.find("COU_TEST") == 0:
                COU_TEST_Count += 1
                COU_TEST_Flag = 1

                if COU_CALL_Flag:
                    COU_CALL_Flag = 0
                    ASSERT_Missing += 1
                    Missed_Asserts.append(TEST_CASE_Name)  # Assert missing finding logic

                event_updater()

                results_updater()

                dat = (ch.strip())
                TEST_CASE_Name = (re.search('"(.+?)"', dat)).group(1)
                if Order_Check_Flag == 0:  # Order_Check_Flag = zero  Means Executing after COU_ASSERT
                    dest.write("\n\n\n")
                    dest.write(TEST_CASE_Name)
                    dest.write("\n============================================================\n")
                    Order_Check_Flag = 1
                    dest.write("@preconditions\n")
                break
            else:
                pass
            ''' 
            ==============================================================================
                                COU_SET IDENTIFICATION
            ==============================================================================
            '''
            if ch.find("COU_SET") == 0:
                if COU_CALL_Flag:
                    COU_CALL_Flag = 0
                    ASSERT_Missing += 1
                    Missed_Asserts.append(TEST_CASE_Name)  # Assert missing finding logic
                COU_SET_Count += 1
                if Order_Check_Flag == 0 and COU_TEST_Flag:
                    dest.write("\n*")
                    Order_Check_Flag = 1
                    Asserts.append('\n*')
                dat = (ch.strip())
                dat1 = re.search('"(.+?)"', dat)
                if COU_TEST_Flag:
                    found = dat1.group(1)
                    dest.write('\t')
                    dest.write(found)
                    dest.write('\n')
                    ''' 
                    ==============================================================================
                                        COU_CALL IDENTIFICATION
                    ==============================================================================
                    '''
            elif ch.find("COU_CALL") == 0:
                COU_CALL_Count += 1
                Order_Check_Flag = 1
                COU_CALL_Flag = 1
                Event_Print_Flag = 1
                dat = (ch.strip())
                dat1 = re.search('"(.+?)"', dat)
                found = dat1.group(1)
                Events.append(found)
                ''' 
                ==============================================================================
                                    COU_ASSERT IDENTIFICATION
                ==============================================================================
                '''
            elif ch.find("COU_ASSERT") == 0:
                COU_ASSERT_Count += 1
                Order_Check_Flag = 0
                COU_CALL_Flag = 0

                dat = (ch.strip())
                dat1 = re.search('"(.+?)"', dat)
                found = dat1.group(1)
                Asserts.append(found)
                Assert_Print_Flag = 1
            else:
                pass

            line = fp.readline()
            Num_Lines += 1
    event_updater()
    results_updater()

    Missed_Asserts = set(Missed_Asserts)

    ''' 
    ==============================================================================
                        SUMMARIZED RESULT
    ==============================================================================
    '''
    print "Test Cases = ", COU_TEST_Count, "\nTotal SET = ", COU_SET_Count, "\nTotal CALL = ", COU_CALL_Count, \
        "\nTotal ASSERT = ", COU_ASSERT_Count, "\nTotal Line Num = ", Num_Lines, "\nAssert Missing : ", ASSERT_Missing, \
        "\nMissed in : ", "\n".join(Missed_Asserts)
    Str1 = '''
                                  
========================================================
*                   SUMMARY                            *        
========================================================
*   Input File                  : {}                                
*   Output File                 : {}
*   Number Of Test Cases        : {}
*   Number Of Lines             : {}
*   Number Of Asserts           : {}
*   Number Of Asserts Missed    : {}
*   Where You Missed            :  {}
======================================================='''.format(fp.name, dest.name, COU_TEST_Count, Num_Lines,
                                                                  COU_ASSERT_Count, ASSERT_Missing,
                                                                  "\n\t\t\t\t\t\t\t\t\t".join(Missed_Asserts))

    dest.close()
    dest = open("Doxygen_Gen.txt", "r")
    contents = dest.readlines()
    dest.close()
    contents.insert(6, Str1)
    dest = open("Doxygen_Gen.txt", "w")
    contents = "".join(contents)
    dest.write(contents)
    fp.close()
    T = Text(root, height=15, width=300)
    T.pack()
    T.insert(END, Str1)


def gui_main():
    global root, FileChoose
    root = Tk()
    root.title('Doxygen Generator')

    w = 800  # width for the Tk root
    h = 600 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    frame = Frame(root)
    frame.pack()
    button = Button(frame,
                    text="QUIT",
                    fg="red",
                    command=quit)
    button.pack(side=LEFT)
    FileChoose = Button(frame,
                        text="Choose File",
                        command=choose_file)
    FileChoose.pack(side=LEFT)

    root.mainloop()


def choose_file():
    global filepath, root, dest

    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.*"), ("all files", "*.*")))
    filepath = root.filename
    generator()


if __name__ == '__main__':
    dest = open("Doxygen_Gen.txt", "w")
    gui_main()
    dest.close()