
import time
import re

Str = '''*********************************************************
*   Program         : Doxygen Comments Updater          
*   Version         : 1.1                               
*   Developer       : Anish Kumar                       
*   Date And Time   : {}                                          
*********************************************************\
'''.format(time.asctime())


Sub_Cond = 97
COU_TEST_Count = 0
COU_TEST_Flag, COU_CALL_Flag, Assert_Print_Flag, Event_Print_Flag= 0, 0, 0, 0
ASSERT_Missing = 0
Missed_Asserts = []
Asserts = []
Events = []
Order_Check_Flag = 0  #
COU_SET_Count, COU_CALL_Count, COU_ASSERT_Count, COU_TEST_Count = 0, 0, 0, 0
Num_Lines = 0
# Output File
dest = open("New.txt","w")
# Input File
filepath = 'Test.txt'
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
                Missed_Asserts.append(TEST_CASE_Name)           # Assert missing finding logic

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
            dat = (ch.strip())
            TEST_CASE_Name = (re.search('"(.+?)"', dat)).group(1)
            if Order_Check_Flag == 0:                                       # Order_Check_Flag = zero  Means Executing after COU_ASSERT
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
                Missed_Asserts.append(TEST_CASE_Name)           # Assert missing finding logic
            COU_SET_Count += 1
            if Order_Check_Flag == 0 and COU_TEST_Flag:
                dest.write("\n*")
                Order_Check_Flag = 1
                Asserts.append('\n*')
            dat = (ch.strip())
            dat1 = re.search('"(.+?)"', dat)
            if COU_TEST_Flag:
                found = dat1.group(1)
                print(found)
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
            print('----------------')
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
            print(found)
        else:
            pass

        line = fp.readline()
        Num_Lines += 1
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
======================================================='''.format( fp.name, dest.name, COU_TEST_Count, Num_Lines, COU_ASSERT_Count, ASSERT_Missing,"\n\t\t\t\t\t\t\t\t\t".join(Missed_Asserts))

dest.close()
dest = open("New.txt","r")
contents = dest.readlines()
dest.close()
contents.insert(6, Str1)
dest = open("New.txt","w")
contents = "".join(contents)
dest.write(contents)
dest.close()
fp.close()


