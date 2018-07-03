'''
Doxygen Comments Generator
--------------------------
Author  :   Anish Kumar
Date    :   23/06/2018
'''

import time
import re, sys
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import os
import subprocess

Str = '''*********************************************************
*   Program       :   Doxygen Comments Generator          
*   Version         :   1.1                               
*   Developer    :   Anish Kumar                       
*   Date             :   25-June-2018                                           
*********************************************************\
'''
COU_TEST_Count = 0
COU_TEST_Flag, COU_CALL_Flag, Assert_Print_Flag, Event_Print_Flag = 0, 0, 0, 0
ASSERT_Missing = 0
Missed_Asserts = []
Asserts = []
Events = []
Order_Check_Flag = 0  #
COU_SET_Count, COU_CALL_Count, COU_ASSERT_Count, COU_TEST_Count = 0, 0, 0, 0
Num_Lines = 0
Name = " "
Annotation_missing = 0
Annotation_missed_in = []
alph = 98
alph1 = 98
filepath = "NULL"

def event_updater():
    global Event_Print_Flag
    global Events
    if Event_Print_Flag:
        dest.write(" *\n * @events\n *")
        Event_Print_Flag = 0
        Events = set(Events)
        for i in Events:
            dest.write(' ')
            dest.write(i)
            dest.write('\n *')
        Events = []


def results_updater():
    global Assert_Print_Flag
    global Asserts, alph1
    if Assert_Print_Flag:
        dest.write("\n * @results\n * {}:\n * ".format(chr(97)))
        alph1 = 98
        Assert_Print_Flag = 0
        for i in Asserts:
            dest.write(i)
            dest.write(' ')
        Asserts = []


def generator():
    global COU_TEST_Count, ASSERT_Missing, Missed_Asserts, Order_Check_Flag, TEST_CASE_Name, COU_ASSERT_Count
    global dest, COU_CALL_Flag, COU_TEST_Flag, COU_SET_Count, COU_CALL_Count, Event_Print_Flag, Assert_Print_Flag
    global Num_Lines, Name
    global Name, E1, Annotation_missing, alph, alph1, found, filepath
    First_Time = 0
    Name = E1.get()
    dest = open("Doxygen_Gen.txt", "w")

    # Loop Starts here
    with open(filepath) as fp:
        # Reading Line by Line
        # dest.write(Str)
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
                alph = 98
                if COU_CALL_Flag:
                    COU_CALL_Flag = 0
                    ASSERT_Missing += 1
                    Missed_Asserts.append(TEST_CASE_Name)  # Assert missing finding logic

                event_updater()

                results_updater()
                if First_Time:
                    dest.write("\n * @type\n * Elementary Comparison Test (ECT)\n *\n * @regression\n * No\n *\n * @integration\n * No\n *\n * @validates\n *\n *")
                First_Time = 1
                dat = (ch.strip())
                dat1 = (re.search('"(.+?)"', dat))
                if dat1:
                    TEST_CASE_Name = dat1.group(1)
                else:
                    Annotation_missing += 1
                    Annotation_missed_in.append(Num_Lines+1)
                if Order_Check_Flag == 0:  # Order_Check_Flag = zero  Means Executing after COU_ASSERT
                    dest.write("\n**/\n\n\n ")
                    dest.write(TEST_CASE_Name)
                    dest.write("\n============================================================\n")
                    Order_Check_Flag = 1
                    dest.write("/**\n")
                    dest.write(" * @brief\n *\n *")
                    dest.write(" @description\n *\n *")
                    dest.write(" @author\n * ")
                    dest.write(Name)
                    dest.write("\n *\n")
                    dest.write(" * @preconditions\n * {}:\n".format(chr(97)))
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

                    dest.write(" * \n * {}:\n".format(chr(alph)))
                    alph += 1
                    Order_Check_Flag = 1
                    Asserts.append('\n * {}:\n *'.format(chr(alph1)))
                    alph1 += 1
                dat = (ch.strip())
                dat1 = re.search('"(.+?)"', dat)
                if COU_TEST_Flag:                   # Omiting checking SET before starting Test cases
                    if dat1:
                        found = dat1.group(1)
                    else:
                        Annotation_missing += 1
                        Annotation_missed_in.append(Num_Lines+1)
                    dest.write(' * ')
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
                if dat1:
                    found = dat1.group(1)
                else:
                    Annotation_missing += 1
                    Annotation_missed_in.append(Num_Lines+1)
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
                # current_assert_list = set(Asserts)
                if dat1:
                    found = dat1.group(1)
                else:
                    Annotation_missing += 1
                    Annotation_missed_in.append(Num_Lines+1)
                # if found not in current_assert_list:
                Asserts.append(found)
                Asserts.append('\n *')
                Assert_Print_Flag = 1
            else:
                pass

            line = fp.readline()
            Num_Lines += 1
    event_updater()
    results_updater()

    Missed_Asserts = set(Missed_Asserts)
    if Annotation_missing > 0:
        error("Annotation Missing\nPlease Update Annotations properly\n{}\nOutput may incomplete..!!".format(Annotation_missed_in))


    ''' 
    ==============================================================================
                        SUMMARIZED RESULT
    ==============================================================================
    '''
    # print "Test Cases = ", COU_TEST_Count, "\nTotal SET = ", COU_SET_Count, "\nTotal CALL = ", COU_CALL_Count, \
    #     "\nTotal ASSERT = ", COU_ASSERT_Count, "\nTotal Line Num = ", Num_Lines, "\nAssert Missing : ", ASSERT_Missing, \
    #     "\nMissed in : ", "\n".join(Missed_Asserts)
    Str1 = '''
                                  
========================================================
*                   SUMMARY                            *        
========================================================
*   Date and Time               : {}
*   Input File                  : {}                                
*   Output File                 : {}
*   Number Of Test Cases        : {}
*   Number Of Lines             : {}
*   Number Of Asserts           : {}
*   Number of Annotations Missed: {}
*   Where You Missed Annotation : Line Numbers:\n                                   {}
*   Number Of Asserts Missed    : {}
*   Where You Missed            : {}
======================================================='''.format(time.asctime(), fp.name, dest.name, COU_TEST_Count, Num_Lines,
                                                                  COU_ASSERT_Count,Annotation_missing, Annotation_missed_in, ASSERT_Missing,
                                                                  "\n\t\t\t\t\t\t\t\t\t".join(Missed_Asserts))

    dest.write(''' 
    
    ==============================================================================
                                        EOF
    ==============================================================================
    ''')
    dest.close()
    dest = open("Doxygen_Gen.txt", "r")
    contents = dest.readlines()
    dest.close()
    contents.insert(0, Str1)
    dest = open("Doxygen_Gen.txt", "w")
    contents = "".join(contents)
    dest.write(contents)
    fp.close()
    dest.close()
    # T = Text(root, height=2, width=30)
    # T.pack(pady = 20)
    # T.insert(END, "Generation Finished !\nPlease close this window !")
    #

# def quit():
#     sys.exit()
#

def gui_main():
    global root, FileChoose, Name, E1, filepath
    root = Tk()
    root.title('Doxygen Generator')
    root.resizable(0, 0)
    w = 500  # width for the Tk root
    h = 100 # height for the Tk root

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


    ''' 
    ==============================================================================
                        CHOOSE FILE BUTTON
    ==============================================================================
    '''
    FileChoose = Button(frame,
                        text="Choose File",
                        command=choose_file)
    FileChoose.pack(side=LEFT, padx = 20)

    ''' 
    ==============================================================================
                        INFO BUTTON
    ==============================================================================
    '''
    button_info = Button(frame,
                    text="Info",
                    fg="blue",
                    command=info)
    button_info.pack(side=RIGHT)

    L1 = Label(root, text="Author Name")
    L1.pack(side=LEFT, fill = X, padx = 20, pady = 0)

    E1 = Entry(root, bd=5)
    E1.pack(side=LEFT)
    root.mainloop()


def info():
    tkMessageBox.showinfo("Doxygen Generator", Str)


def error(str):
    tkMessageBox.showerror("Doxygen Generator", str)


def choose_file():
    global filepath , root, dest

    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.c"), ("all files", "*.*")))
    filepath = root.filename
    generator()
    root.destroy()


if __name__ == '__main__':
    gui_main()
    if filepath != "NULL":
        osCommandString = "notepad.exe Doxygen_Gen.txt"
        subprocess.call(osCommandString, shell=False)


