global_id = 10000
class Book:

    global global_id
    global_id=10000

    def __init__(self,name:str=None,author=None,year:int=None,ID:int=None,**Hashmap):
        self.name=name
        self.author=author
        self.year=year
        self.Book_ID=ID if ID is not None else self.generate_id()
        self.borrowed=False
        self.borrowed_by=None

        if Hashmap:
            for key , value in Hashmap.items():
                setattr(self, key, value)
    
    def change_name(self,NEW_name:str)->None: 
        self.name=NEW_name
        return
    
    def generate_id(self):
        global global_id
        temp=global_id
        global_id+=1
        return temp

class Books:

    def __init__(self,books:list[Book]=None)->None:
        self.books=books if books is not None else []

    def __len__(self)->int:
        return len(self.books)

    def __getitem__(self, key)-> object:
        return self.books[key]

    def add_book(self,new_book:Book)->None:
        self.books.append(new_book)
