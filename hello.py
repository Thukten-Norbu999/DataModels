
import os, sqlite3, uuid, getpass, bcrypt, datetime

class User:
    def __init__(self, Name, Email, DOB):
        self.id = str(uuid.uuid4())
        self.Name = Name.title()
        self.DOB = DOB
        # self.age = DOB[-1]
        self.Email = Email
        

    def validate(self):
        pw1 = getpass.getpass("Enter your password: ")
        pw2 = getpass.getpass("Confirm your password: ")
        if len(pw1) >= 8:
            if pw1 != pw2:
            
                return False,'Does not Match the first one'
            else:
                return True, bcrypt.hashpw(pw1.encode('utf-8'), bcrypt.gensalt())
        else: 
            
            return False, 'Too short'


    def save(self, val):
        
        if val[0] == True:
            con = sqlite3.connect("C:/Users/Kinga Norbu/Desktop/game/data/database.db")
            cur = con.cursor()
            hashed_pw = val[1].decode('utf-8')
            values = (self.id, self.Name, self.DOB, self.Email,  hashed_pw)
            cur.execute("INSERT INTO USER (id, name, dob, email, password) VALUES (?, ?, ?, ?, ?)", values)
            con.commit()

            cur.close()
            con.close()
            print('Successfully Created')
        else:
            print(val[1])
            self.validate()
    
    def get_age(self, email):
         return int(datetime.date.today().split('-')[0]-self.DOB.split('/')[-1])

def createUserTable():
    if os.path.exists("C:/Users/Kinga Norbu/Desktop/game/data/database.db"):
        con = sqlite3.connect("C:/Users/Kinga Norbu/Desktop/game/data/database.db")
        cur = con.cursor()

        table_name = 'USER'
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cur.fetchmany() != None:
            cur.execute(f'''CREATE TABLE {table_name}
                    (id TEXT PRIMARY KEY, name TEXT, email TEXT, dob TEXT, password TEXT)''')
            con.commit()
            con.close()
        
        
    else:
        open("C:/Users/Kinga Norbu/Desktop/game/data/database.db", 'w').close()

def createUser(name, email, dob):
    user = User(name, email, dob)
    val = user.validate()
    user.save(val)



try:    
    createUserTable()
except sqlite3.OperationalError:
    print('Table Mitubay')


# name = input('Name: ')
# email = input('Email: ')
# dob = input('DOB in MM/DD/YY format: ')

# createUser(name, email, dob)

con = sqlite3.connect("C:/Users/Kinga Norbu/Desktop/game/data/database.db")
cur = con.cursor()

username = 'Thukten Norbu'
cur.execute("SELECT id, age FROM User WHERE username = ?", (username,))
row = cur.fetchone()

if row is not None:
    user_id = row[0]
    age = row[1]
    # Process the data...
else:
    print('Nothing')