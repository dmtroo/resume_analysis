from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import os
import re

# converts pdf and returns its text content as a string
from UDPipe import parse


def convert(fileName, pages=None):
    if not pages:
        pageNumbers = set()
    else:
        pageNumbers = set(pages)

    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fileName, 'rb')
    for page in PDFPage.get_pages(infile, pageNumbers):
        interpreter.process_page(page)

    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


# converts all pdfs in directory and saves all resulting to pre-text.txt
def convert_multiple(pdf_dir):
    text_file = open("parsing_processes/pre-text.txt", "w", encoding="utf-8")
    if pdf_dir == "": pdf_dir = os.getcwd() + "\\"  # if no pdfDir passed in
    for pdf in os.listdir(pdf_dir):  # iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdf_dir + pdf
            text = convert(pdfFilename)  # get string of text content of pdf

            text_file.writelines(text)  # write text to text file


# deletes unnecessary strings
def delete_unused_strings(test_file):
    del_strings = ["Кандидат з найбільшої бази резюме України", "Найсвіжішу версію резюме ви зможете скачати тут:",
                   "Ваш надійний партнер в пошуку роботи та підборі персоналу",
                   "Увійдіть або зареєструйтеся на сайті як роботодавець, щоб бачити контактну інформацію.",
                   "https://novarobota.ua/ua/resume/", "https://www.work.ua/resumes/",
                   "Отримати контакти цього кандидата можна на сторінці", "https://rabota.ua/ua/candidates/",
                   "Сайт пошуку роботи №1 в Україні", "Отримати контакти цього кандидата можна на сторінці",
                   "Резюме від"]

    res_line = ""
    with open(test_file, "r", encoding="utf-8") as test_file:
        for line in test_file:
            new_line = line
            if del_strings[0] in line or del_strings[1] in line or del_strings[2] in line or del_strings[3] in line or \
                    del_strings[4] in line or del_strings[5] in line or del_strings[6] in line or del_strings[
                7] in line or del_strings[8] in line or del_strings[9] in line or del_strings[10] in line or line == "\n":
                new_line = line.replace(line, "")
            res_line += new_line

    with open("parsing_processes/text.txt", "w", encoding="utf-8") as test_file:
        test_file.write(res_line)
        test_file.close()


# PROGRAM START
pdfDir = "D:/НаУКМА/Курсова/Base/"
convert_multiple(pdfDir)
delete_unused_strings("parsing_processes/pre-text.txt")

# ANALYSIS
os.system(
    "curl -F model=ukrainian-iu-ud-2.10-220711 -F data=@parsing_processes/text.txt -F tokenizer= -F tagger= -F parser= http://lindat.mff.cuni.cz/services/udpipe/api/process > parsing_processes/out.txt")

lines = parse("parsing_processes/out.txt")

# lemmatization
with open("output/result.txt", 'w', encoding="utf-8") as file:
    for line in lines:
        if len(line) > 2:
            if line[2] != '.' and line[2] != ',' and line[2] != ':' and line[2] != '!' and line[2] != '?' and line[
                3] != "NUM" and line[3] != "PUNCT" and line[3] != "CCONJ" and line[3] != "ADP" and line[2] != '(' and \
                    line[2] != ')' and line[2] != '%' and line[2] != '=' and line[2] != '-' and line[2] != '/' and line[
                2] != ';' and line[2] != '"' and line[2] != '●' and line[2] != '"' and line[2] != '»' and line[
                2] != '«' and line[2] != '+' and line[2] != '|' and line[2] != '⬥' and line[2] != '•' and line[
                2] != '❖' and line[2] != '' and line[2] != '' and not (re.match("[0-9]+", line[2])):
                # file.write(line[1] + "\n")
                file.write(line[2] + "\n")
                # print(line[1])
file.close()
