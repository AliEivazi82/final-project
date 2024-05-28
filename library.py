
import pymysql
from colorama import init, Fore

init(autoreset=True)


config = {
    'user': 'Ali',
    'password': '1234',
    'host': 'localhost',
    'database': 'library_db'
}

class Library:
    def __init__(self):
        print("Welcome to the Library...\n")
        self.conn = pymysql.connect(**config)
        self.create_table()
    
    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
    
    def create_table(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255) NOT NULL,
                        category VARCHAR(255) NOT NULL,
                        pages INT
                    )
                """)
                self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")
    
    
    def __execute_query(self, sql, params=None, commit=False):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                if commit:
                    self.conn.commit()
                return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    
    def __insert(self, sql, params):
        return self.__execute_query(sql, params, commit=True)
        
    def __delete(self, sql, params):
        return self.__execute_query(sql, params, commit=True)

    def __select(self, sql, params=None):
        return self.__execute_query(sql, params)

    def __update(self, sql, params):
        return self.__execute_query(sql, params, commit=True)
      
    def add_book(self, title, author, category, pages):
        sql = "INSERT INTO books (title, author, category, pages) VALUES (%s, %s, %s, %s)"
        self.__insert(sql, (title, author, category, pages))
        return True
    
    def delete_book(self, book_id):
        books = self.__select("SELECT id FROM books WHERE id = %s", (book_id,))
        if books:
            self.__delete("DELETE FROM books WHERE id = %s", (book_id,))
            return True
        else:
            return False


    def find_book(self, search_term):
        sql = ("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR category LIKE %s")
        result = self.__select(sql, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        if result:
            books_info = []
            for book in result:
                books_info.append(f"Book ID: {book[0]},\n Title: {book[1]},\n Author: {book[2]},\n Category: {book[3]},\n Pages: {book[4]}\n")
            return "\n".join(books_info)
        else:
            return "No books found."


    def select_book(self, book_id, columns=True):
        if columns is True:
            columns = "*"
        else:
            columns = ", ".join(columns)
        sql = f"SELECT {columns} FROM books WHERE id = %s"
        result = self.__select(sql, (book_id,))
        if result:
            result = result[0]
            return f"Result with book_id = {result[0]} :\nBook title: {result[1]} \nBook author: {result[2]} \nBook category : {result[3]}\nBook pages: {result[4]}"
        else:
            return "Book Not found."
        
   
    def edit_book(self, book_id, title=None, author=None, category=None, pages=None):
        fields = []
        params = []
        
        if title is not None:
            fields.append("title = %s")
            params.append(title)
        if author is not None:
            fields.append("author = %s")
            params.append(author)
        if category is not None:
            fields.append("category = %s")
            params.append(category)
        if pages is not None:
            fields.append("pages = %s")
            params.append(pages)
        
        if fields:
            params.append(book_id)
            sql = f"UPDATE books SET {', '.join(fields)} WHERE id = %s"
            self.__update(sql, params)
            return True
        else:
            return False


# ==============================================================================================================
# ==============================================================================================================
# ==============================================================================================================
# ==============================================================================================================
# ==============================================================================================================


library = Library()
while(True):
    input1 = int(input(f"{Fore.RED}\nwhat do you want?! (send the number)\n {Fore.GREEN}1. add book\n 2. edit book\n 3. find book\n 4. delete book\n 5. exit\n => "+ Fore.RED))
    
    if input1 not in range(1, 6):
                print("\nsend a number from 1 to 5 :\n")
                continue
            
    if input1 == 5 :
        print(Fore.LIGHTRED_EX+"\nBye..")
        break
    
    if(input1 == 1):
        title = input(Fore.YELLOW+"\nAdding Book.. \nSend the title : ")
        author = input("Send the author : ")
        category = input("Send the category : ")
        pages = int(input("Send the pages in number : "))
        if(library.add_book(title, author, category, pages)):
            print(Fore.BLUE+"Book added successfully")
        else:
            print(Fore.RED+"Error while adding book")
    
    elif(input1 == 2):
        input2 = int(input(Fore.CYAN+"\nEditing book..\nSend book ID : "))
        changes = {}
        while True:
            input21 = int(input(f"what do you want to edit?! (send the number)\n {Fore.GREEN}1. title\n 2. author\n 3. category\n 4. pages\n 5. done\n => "))
            if input21 == 5:
                break
        
            if input21 not in range(1, 5):
                print("\nsend a number from 1 to 4 :")
                continue
            
            column_name = None
            new_value = None
            
            if input21 == 1:
                column_name = "title"
                new_value = input("what is the new title? => ")
            elif input21 == 2:
                column_name = "author"
                new_value = input("what is the new author? => ")
            elif input21 == 3:
                column_name = "category"
                new_value = input("what is the new category? => ")
            elif input21 == 4:
                column_name = "pages"
                new_value = input("what is the new number of pages? => ")
            
            if column_name and new_value:
                changes[column_name] = new_value
    
        if(library.edit_book(input2, **changes)):
            print(Fore.BLUE+"edited successfully..")
        else:
            print(Fore.RED+"Error while editing book")
            
    elif(input1 == 3):
        input3 = input(Fore.GREEN+"Enter search term: "+Fore.MAGENTA)
        print(library.find_book(input3))
        
    elif input1 == 4:
        book_id = int(input(Fore.CYAN+"\nDeleting book..\nSend book ID : "))
        
        book_info = library.select_book(book_id)
        print(Fore.YELLOW + "Book information:")
        print(book_info)
        
        confirm = input(Fore.RED + "Are you sure you want to delete this book? (yes/no): ")
        
        if confirm.lower() == "yes":
            if library.delete_book(book_id):
                print(Fore.BLUE + "Book deleted successfully.")
            else:
                print(Fore.RED + "Error while deleting book.")
        else:
            print(Fore.GREEN + "Delete operation canceled.")

