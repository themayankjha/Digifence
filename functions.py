import sqlite3
import hashlib
import os,glob


def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest() 

def validate(username,password):
    
    con = sqlite3.connect('app.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users where username = ? ",(username,))
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
                        break
    return completion

def listfiles():
    filelist = filter( lambda x: os.path.isfile(os.path.join('uploads/', x)),
                        os.listdir('uploads/') )
    filelist = [ (file_name, os.stat(os.path.join('uploads/', file_name)).st_size) 
                    for file_name in filelist  ]
    return filelist

def deletefile(name):
    os.remove('uploads/'+name) 