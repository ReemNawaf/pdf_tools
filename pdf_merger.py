import os
import shutil
from os import listdir, mkdir
from os.path import isfile, join, exists
from PyPDF2 import PdfFileMerger, PdfFileReader


def mergeFiles(group1_folder_name=os.getcwd() + '\\' + 'group_1', group2_folder_name=os.getcwd() + '\\' + 'group_2',
               merged_folder_path=os.getcwd(), merged_files_naming='', deleted_page_number = 2):
    group1_pdf_files = [f for f in listdir(group1_folder_name) if isfile(join(group1_folder_name, f)) and '.pdf' in f]
    group2_pdf_files = [f for f in listdir(group2_folder_name) if isfile(join(group2_folder_name, f)) and '.pdf' in f]

    if len(group1_pdf_files) != len(group2_pdf_files):
        print(
            'files numbers inside (' + group1_folder_name + ') and (' + group1_folder_name + ')\n doesm\'t match, make sure both files have the same files number')
        return

    has_result_files_naming = merged_files_naming != ''
    merged_folder_name = 'merged_files'

    while True:
        merged_folder_full_name = merged_folder_path + '\\' + merged_folder_name
        if not exists(merged_folder_full_name):
            mkdir(merged_folder_full_name)
            break
        else:
            user_ch = input('there is already a folder named (' + merged_folder_full_name + ')' +
                            '\ndo you want to delete it (Y, n)? '
                            )
            if user_ch == 'Y' or user_ch == 'y':
                shutil.rmtree(merged_folder_full_name)
                continue
            else:
                temp = merged_folder_name
                merged_folder_name = input('Please change output folder name: ')
                if temp != merged_folder_name:
                    print('--------------------------------------------------------------')
                    continue

    #   Append the pdf files
    for i in range(len(group1_pdf_files)):
        # result file name same as group2 file name
        m_files_naming = merged_files_naming + ' ' + str(i) + '.pdf' if has_result_files_naming else group2_pdf_files[i]

        merger = PdfFileMerger()

        # to get number of pages of gourp1 file
        merger.append(group1_folder_name + '\\' + group1_pdf_files[i])
        merger.append(group2_folder_name + '\\' + group2_pdf_files[i])

        #   delete second page
        if deleted_page_number == 0:
            pass
        elif (deleted_page_number - 1) not in range(len(merger.pages)):
            print('the page number you want to delete is larger than the number of pages in merged file')
            return
        else:
            merger.pages.remove(merger.pages[deleted_page_number - 1])

        #   Write the merged result file to the Output directory
        merger.write(merged_folder_full_name + '\\' + m_files_naming)

        merger.close()

    #   Launch the result file
    print('--------------------------------------------------------------\nFiles merged Successfully :)\ninside',
          merged_folder_full_name)


print('-----------------------PDF Special Merger-----------------------' +
      '\nHello, Samer'
      '\nPlease, select the Mode you want: '
      '\n\tF: Fixed Mode, you have to put the:' +
      '\n\t\t- first group of files in folder named (group_1)' +
      '\n\t\t- second group of files in folder named (group_2)'
      '\n\t\tin this exact location ' + os.getcwd() +
      '\n\tD: Dynamic Mode, you will enter the folder path of the first & the second group of files' +
      '\nOr Q:to quit the program'
      )

while True:

    user_choice = input(
        '\nenter F, D or Q (in capital or small case, doesn\'t matter): '
    )

    if user_choice == 'f' or user_choice == 'F':
        mergeFiles()
    elif user_choice == 'd' or user_choice == 'D':
        g1_path, g2_path, re_path = '', '', ''
        #   checking 1st group folder path
        while True:
            g1_path = input('Enter the folder path that contains all 1st group files: ')
            if not exists(g1_path):
                print(g1_path, 'don\'t exist. Please try again with the correct path.')
            else:
                break

        #   checking 2nd group folder path
        while True:
            g2_path = input('Enter the folder path that contains all 2nd group files: ')
            if not exists(g2_path):
                print(g2_path, 'don\'t exist. Please try again with the correct path.')
            else:
                break

        #   checking output folder path
        while True:
            re_path = input('Enter the folder path where you want to save a folder contains all merged: ')
            if not exists(re_path):
                print(re_path, 'don\'t exist. Please try again with the correct path.')
            else:
                break

        while True:
            deleted_p_num = input('Enter the page number you want to delete from the merged file (enter 0 if you '
                                       'don\'t want to delete any page): ')
            if not (deleted_p_num.isnumeric()):
                print('you didn\'t enter a valid int page number (it must be a positive integer)')
            else:
                break

        re_f_naming = input('how do you want merged files named? ')
        mergeFiles(group1_folder_name=g1_path, group2_folder_name=g2_path, merged_folder_path=re_path,
                   merged_files_naming=re_f_naming, deleted_page_number= int(deleted_p_num))

    elif user_choice == 'q' or user_choice == 'Q':
        break

    else:
        print('Please enter a valid choice (F, D, or Q)')
