
import time
import re

Sub_Cond = 97
COU_TEST_Count = 0
COU_TEST_Flag, COU_CALL_Flag = 0, 0
ASSERT_Missing = 0
Missed_Asserts = []
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
            Sub_Cond = 97
            dat = (ch.strip())
            TEST_CASE_Name = (re.search('"(.+?)"', dat)).group(1)
            if Order_Check_Flag == 0:                                       # Order_Check_Flag = zero  Means Executing after COU_ASSERT
                dest.write("\n\n\n")
                dest.write(TEST_CASE_Name)
                dest.write("\n============================================================\n")
                Order_Check_Flag = 1
                dest.write("@precondition\n")

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
        else:
            pass

        line = fp.readline()
        Num_Lines += 1


''' 
==============================================================================
                    SUMMARIZED RESULT
==============================================================================
'''
print "Test Cases = ", COU_TEST_Count, "\nTotal SET = ", COU_SET_Count, "\nTotal CALL = ", COU_CALL_Count, \
    "\nTotal ASSERT = ", COU_ASSERT_Count, "\nTotal Line Num = ", Num_Lines, "\nAssert Missing : ", ASSERT_Missing, \
    "\nMissed in : ", Missed_Asserts
