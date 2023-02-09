import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys
import codecs

def chap2text(chap):
    # since epub is primarily a zip file containing several xml and html files
    removelist = ['[document]','noscript','header','html','meta','head','input','script']
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in removelist:
            output += '{} '.format(t)
    return output


def getBook(bookname, outputname):
    outputfile=codecs.open(outputname,"w",encoding="utf-8")
    book = epub.read_epub(bookname)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())

    for chapter in chapters:
        text=chap2text(chapter)
        outputfile.write(text+"\n")

getBook("MichaelSandel_JusticeWhatSTheRightThingToDo.epub", "test.txt")
