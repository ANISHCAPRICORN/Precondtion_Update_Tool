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
import subprocess
from collections import Counter

Str = '''*********************************************************
*   Program       :   Doxygen Comments Generator          
*   Version         :   1.3                               
*   Developer    :   Anish Kumar                       
*   Date             :   08-Jul-2018                                           
*********************************************************\
'''
StrA = '''*********************************************************
*   Program       :   Doxygen Comments Generator        *
*   Version       :   1.3                               *
*   Developer     :   Anish Kumar                       *
*   Date          :   08-Jul-2018                       *          
*********************************************************        
'''
COU_TEST_Count = 0
COU_TEST_Flag, COU_CALL_Flag, Assert_Print_Flag, Event_Print_Flag = 0, 0, 0, 0
ASSERT_Missing = 0
COU_LOG_Count = 0
Missed_Asserts = []
Missed_Asserts_Final = []
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
error_1 = 0
COU_LOG = {}
COU_LOG_List = []
Missed_Asserts_Dict = {}
Precondn_Str = ""
Updat_Flag = 0
Submit_Flag = 0


def event_updater():
    global Event_Print_Flag, Precondn_Str
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
    global Assert_Print_Flag, Precondn_Str
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
    global Num_Lines, Name, COU_LOG, COU_LOG_Count, COU_LOG_List, Missed_Asserts_Dict, Missed_Asserts_Final
    global Name, E1, Annotation_missing, alph, alph1, found, filepath, error_1, Precondn_Str, StrA
    First_Time = 0
    Name = E1.get()
    dest = open("Doxygen_Gen.txt", "w")
    dest.write(StrA)
    try:
        # Loop Starts here
        with open(filepath, 'r+') as fp:
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
                        Order_Check_Flag = 0
                        Assert_Print_Flag = 1
                    event_updater()
                    results_updater()
                    if First_Time:
                        dest.write("\n * @type\n * Elementary Comparison Test (ECT)\n *\n * @regression\n * No\n *\n * @integration\n * No\n *\n * @validates\n *\n **/\n")
                    First_Time = 1
                    dat = (ch.strip())
                    dat1 = (re.search('\((.+?),', dat))
                    dat3 = re.search('"(.+?)"', dat)
                    if dat1:
                        TEST_CASE_Name = dat1.group(1)
                        # print(TEST_CASE_Name)
                    else:
                        pass
                    if dat3:
                        pass
                    else:
                        Annotation_missing += 1
                        Annotation_missed_in.append(Num_Lines + 1)
                    if Order_Check_Flag == 0:  # Order_Check_Flag = zero  Means Executing after COU_ASSERT
                        dest.write("\n\n ")
                        dest.write('< ')
                        dest.write(TEST_CASE_Name)
                        dest.write(' >')
                        dest.write("\n============================================================\n")
                        Order_Check_Flag = 1
                        dest.write("/**\n")
                        dest.write(" * @brief\n * Test case {}\n *\n *".format(TEST_CASE_Name))
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
                        # print(COU_LOG_List)
                        Missed_Asserts.append(TEST_CASE_Name)  # Assert missing finding logic
                    COU_SET_Count += 1
                    if Order_Check_Flag == 0 and COU_TEST_Flag:

                        dest.write(" * \n * {}:\n".format(chr(alph)))
                        alph += 1
                        Order_Check_Flag = 1
                        Asserts.append('\n * {}:\n *'.format(chr(alph1)))
                        alph1 += 1
                    dat = (ch.strip())
                    dat1 = re.search('\((.+?),', dat)
                    dat2 = re.search(',(.+?),',dat)
                    dat3 = re.search('"(.+?)"', dat)
                    if COU_TEST_Flag:                   # Omiting checking SET before starting Test cases
                        if dat1:
                            found = dat1.group(1)
                            found += " set to " + dat2.group(1)
                        else:
                            pass
                        if dat3:
                            pass
                        else:
                            Annotation_missing += 1
                            Annotation_missed_in.append(Num_Lines + 1)
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
                    dat1 = re.search('\((.+?)"', dat)
                    dat3 = re.search('"(.+?)"', dat)
                    if dat1:
                        found = "Calling Function "
                        found += dat1.group(1)
                    else:
                        pass
                    if dat3:
                        pass
                    else:
                        Annotation_missing += 1
                        Annotation_missed_in.append(Num_Lines + 1)
                    Events.append(found)
                    ''' 
                    ==============================================================================
                                        COU_ASSERT_EQUAL IDENTIFICATION
                    ==============================================================================
                    '''
                elif ch.find("COU_ASSERT_EQUAL") == 0:
                    COU_ASSERT_Count += 1
                    Order_Check_Flag = 0
                    COU_CALL_Flag = 0

                    dat = (ch.strip())
                    dat1 = re.search('\((.+?),', dat)
                    dat2 = re.search(',(.+?)"', dat)
                    dat3 = re.search('"(.+?)"', dat)
                    # print(dat3)
                    # current_assert_list = set(Asserts)
                    if dat1:
                        found = "Check whether the value of "
                        found += dat1.group(1)
                        found += " is equal to " + dat2.group(1)
                    else:
                        pass
                    if dat3:
                        pass
                    else:
                        Annotation_missing += 1
                        Annotation_missed_in.append(Num_Lines+1)
                    # if found not in current_assert_list:
                    Asserts.append(found)
                    Asserts.append('\n *')
                    Assert_Print_Flag = 1
                    ''' 
                    ==============================================================================
                                        COU_ASSERT_NOT_EQUAL IDENTIFICATION
                    ==============================================================================
                    '''
                elif ch.find("COU_ASSERT_NOT_EQUAL") == 0:
                    COU_ASSERT_Count += 1
                    Order_Check_Flag = 0
                    COU_CALL_Flag = 0

                    dat = (ch.strip())
                    dat1 = re.search('\((.+?),', dat)
                    dat2 = re.search(',(.+?)"', dat)
                    dat3 = re.search('"(.+?)"', dat)
                    if dat1:
                        found = "Check whether the value of "
                        found += dat1.group(1)
                        found += " is not equal to " + dat2.group(1)
                    else:
                        pass
                    if dat3:
                        pass
                    else:
                        Annotation_missing += 1
                        Annotation_missed_in.append(Num_Lines + 1)
                    Asserts.append(found)
                    Asserts.append('\n *')
                    Assert_Print_Flag = 1

                    ''' 
                    ==============================================================================
                                        COU_LOG IDENTIFICATION
                    ==============================================================================
                    '''
                elif ch.find("COU_LOG") == 0 or ch.find("COU_PROPERTY") == 0:
                    COU_LOG_Count += 1
                    Order_Check_Flag = 0
                    Assert_Print_Flag = 1
                    dat = (ch.strip())
                    dat1 = re.search('"(.+?)"', dat)
                    dat3 = re.search('"(.+?)"', dat)
                    if dat1:
                        found = dat1.group(1)
                    else:
                        pass
                    if dat3:
                        pass
                    else:
                        Annotation_missing += 1
                        Annotation_missed_in.append(Num_Lines + 1)
                    COU_LOG_List.append("{}                         {}".format(TEST_CASE_Name, found))
                    Asserts.append(' ')
                    Asserts.append('\n *')

                else:
                    pass
                line = fp.readline()
                Num_Lines += 1
                error_1 = 0
    except IOError:
        error_1 = 1
    if COU_CALL_Flag:
        COU_CALL_Flag = 0
        ASSERT_Missing += 1
        Assert_Print_Flag = 1
        Missed_Asserts.append(TEST_CASE_Name)  # Assert missing finding logic

    event_updater()
    results_updater()

    Missed_Asserts_Dict = dict((Counter(Missed_Asserts)))
    # print(Missed_Asserts_Dict.keys())
    # print(Missed_Asserts_Dict.values())
    for i in Missed_Asserts_Dict:
        s = "{}         ---->   {}".format(i, Missed_Asserts_Dict[i])
        Missed_Asserts_Final.append(s)
    # if Annotation_missing > 0:
    #     error("Annotation Missing\nPlease Update Annotations properly\n{}".format(Annotation_missed_in))

    Str1 = '''
                                  
=====================================================================================================
*                                   SUMMARY                                                                
*                            {}                                                
=====================================================================================================

*   Input File                          : {}                                
*   Output File                         : {}
*   Number Of Test Cases                : {}
*   Number Of Lines                     : {}
*   Number Of Asserts                   : {}
*   Justifications(COU_LOG/COU_PROPERTY): {}
*   Number Of Asserts Missed            : {}
*   Where You Missed Asserts            :\n
=====================================================================================================
Test Case                                               Num of Asserts  Missed                                                   
=====================================================================================================
{} 
                                            

====================================== E n d  O f  S u m m a r y ====================================\n'''.format(time.asctime(), fp.name, dest.name, COU_TEST_Count, Num_Lines,
                                                                  COU_ASSERT_Count, COU_LOG_Count, ASSERT_Missing,
                                                                                                    "\n".join(Missed_Asserts_Final))
    # if Annotation_missing == 0:
    dest.write("\n * @type\n * Elementary Comparison Test (ECT)\n *\n * @regression\n * No\n *\n * @integration\n * No\n *\n * @validates\n *\n **/")
    dest.write(''' 
    
    =====================================================================================================
                                                    EOF
    =====================================================================================================
    ''')
    dest.close()
    dest = open("Doxygen_Gen.txt", "r")
    contents = dest.readlines()
    dest.close()
    contents.insert(6, Str1)
    dest = open("Doxygen_Gen.txt", "w")
    contents = "".join(contents)
    dest.write(contents)
    fp.close()
    dest.close()
    root.destroy()


def gui_main():
    global root, FileChoose, Name, E1, filepath, checked
    root = Tk()
    checked = IntVar()
    # root.configure(background='black')
    root.title('Doxygen Generator')
    root.resizable(0, 0)
    w = 450  # width for the Tk root
    h = 150  # height for the Tk root

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
    frame.grid()
    ''' 
    ==============================================================================
                        CHOOSE FILE BUTTON
    ==============================================================================
    '''
    FileChoose = Button(frame,
                        text="Choose File",
                        command=choose_file)
    # FileChoose.pack(side=LEFT, padx = 20)


    ''' 
    ==============================================================================
                        INFO BUTTON
    ==============================================================================
    '''
    button_info = Button(frame,
                    text="Info",
                    fg="blue",
                    command=info)
    # button_info.pack(side=RIGHT)

    L1 = Label(root, text="Author Name")
    # L1.pack(side=LEFT, fill = X, padx = 20, pady = 0)

    E1 = Entry(root, bd=5)
    # E1.pack(side=LEFT)

    ''' 
    ==============================================================================
                        SUBMIT BUTTON
    ==============================================================================
    '''
    button_ok = Button(frame,
                    text="SUBMIT",
                    fg="black",
                    command=submit, width=10)

    ''' 
    ==============================================================================
                        CHECK BUTTON
    ==============================================================================
    '''
    checked = IntVar()
    update_en_den = Checkbutton(root,
                              text="Update to Source file",
                              variable=checked,
                              command=update_enable_or_disable)

    FileChoose.grid(row=2, column=3, padx= 10, pady= 0)

    button_info.grid(row=0, column=0, padx=10, pady=0)
    L1.grid(row=1, column=0, padx= 10, pady= 20)
    E1.grid(row=1, column=1, padx= 10, pady= 20)
    # update_en_den.grid(row=2, column=0, padx= 10, pady= 0)
    button_ok.grid(row=2, column=1, padx= 10, pady= 0)

    root.mainloop()


def submit():
    global filepath, error_1, Updat_Flag, Submit_Flag
    Submit_Flag = 1
    if filepath != "NULL" and error_1 == 0:
        res = tkMessageBox.askquestion("Updating Source File", "Do you Want to Update Selected File With \n Doxygen Comments ?", icon='info')
        if res == 'yes':
            Updat_Flag = 1
            generator()
        elif res == "no":
            Updat_Flag = 0
            generator()
        else:
            pass
    else:
        error_1 = 0
        error("Please Choose File")


def info():
    tkMessageBox.showinfo("Doxygen Generator", Str)


def warn(msg):
    tkMessageBox.showwarning("Doxygen Generator", msg)


def error(msg):
    tkMessageBox.showerror("Doxygen Generator", msg)


def choose_file():
    global filepath , root, dest, Precondn_Str

    root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                 filetypes=(("text files", "*.c"), ("all files", "*.*")))
    filepath = root.filename


def update_enable_or_disable():
    global  checked, Updat_Flag
    if checked.get() == 1:
        Updat_Flag = 1
        # print("checked")
    elif checked.get() == 0:
        Updat_Flag = 0
        # print("Not checked")


def update():
    Str2 = ""
    L_num = 0
    with open("Doxygen_Gen.txt") as f:
        for line in f:
            if "<" in line:
                dat = (line.strip())
                dat1 = re.search('< (.+?) >', dat)
                if dat1:
                    lookup = dat1.group(1)
            if "/**" in line:
                start = 1
                while start:
                    # f1.write(line)
                    Str2 += line
                    for line in f:
                        # f1.write(line)
                        Str2 += line
                        if "**/" in line:
                            start = 0
                            with open(filepath) as myFile:
                                for line1 in myFile:
                                    L_num += 1
                                    if line1.find(lookup) >= 0:
                                        # print 'found at line:', lookup, L_num
                                        L = L_num
                                        break
                            fp1 = open(filepath, "r")
                            contents = fp1.readlines()
                            fp1.close()
                            contents.insert(L - 1, Str2)
                            fp1 = open(filepath, "w")
                            contents = "".join(contents)
                            fp1.write(contents)
                            fp1.close()
                            Str2 = ""
                            L_num = 0
                            L = 0
                            break


def remove():
    pass


if __name__ == '__main__':
    test_case_names_list = []
    gui_main()

    if filepath != "NULL" and error_1 == 0 and Submit_Flag:
        if Updat_Flag:
            update()
        osCommandString = "notepad.exe Doxygen_Gen.txt"
        subprocess.call(osCommandString, shell=False)
    else:
        error_1 = 0


