from book import Books,Book
from Students import Students,Student
from datetime import datetime


_INFO={
    "title": lambda b: b.name,
    "author": lambda b: b.author,
    "ID": lambda b: b.Book_ID,
}


class Library:

    def __init__(self,books_List:Books=None,Students_List:Students=None):
        try:
            self.SHELF=books_List if len(books_List) else Books()
            self.students=Students_List if len(Students_List) else Students()
            self.lend=[]
            self.All_Books=Books(list(self.SHELF.books))
            self.activity_log=[]

        except TypeError as e:
            raise TypeError(f"{e} error one of atte are none please fill it !!!")

    def lend_book(self,Target_Student:Student,target_book:Book)->None:
        if target_book not in self.SHELF.books:
            raise ValueError("book is not available!")

        if target_book.borrowed :
            raise ValueError("book already taken!")

        if Target_Student not in self.students.Students:
            raise ValueError("student couldnt found!")

        Target_Student.lend_books.append(target_book)
        target_book.borrowed=True
        target_book.borrowed_by=Target_Student

        self.lend.append(target_book)

        self.SHELF.books.remove(target_book)
        return

    def search(self,Key:str,Intel:str)->Book:
        func=_INFO[Key]
        for Bk in self.SHELF.books:
            if func(Bk).lower()==Intel.lower():
                return Bk

        return None

    def Return_book(self,tg_student:Student,tg_book:Book)->None:
        if tg_book not in self.lend:
            raise ValueError("book is not in lend")
        if not tg_book.borrowed:
            raise ValueError("BOOK already available!")

        if tg_book not in self.All_Books:
            raise ValueError("book doesnt belong in this library!")

        if tg_student not in self.students:
            raise ValueError(" Student iis not in our database!")

        tg_student.lend_books.remove(tg_book)
        tg_book.borrowed=False
        tg_book.borrowed_by=None
        self.SHELF.books.append(tg_book)
        self.lend.remove(tg_book)
        return None

    def available_books(self)->list[Book]:
        return self.SHELF.books

    def borrowed_books(self)->list[Book]:
        return self.lend

    def log(self,message:str)->None:
        timestamp=datetime.now().strftime("%H:%M")
        self.activity_log.insert(0,f"[{timestamp}] {message}")
