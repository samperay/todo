#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import sqlite3,tempfile,os
fd,path=tempfile.mkstemp(suffix='.sqlite');os.close(fd)
try:
 db=sqlite3.connect(path);db.execute('create table todo (id integer primary key, title text)')
 db.execute('insert into todo(title) values (?)',('healthy',));db.commit()
 print('baseline rows:',db.execute('select count(*) from todo').fetchone()[0])
 try:
  db.execute('insert into todo(id,title) values (1,?)',('duplicate',));db.commit()
 except sqlite3.IntegrityError as e:print('EXPECTED failure:',type(e).__name__);db.rollback()
 print('after rollback rows:',db.execute('select count(*) from todo').fetchone()[0]);db.close()
finally:os.remove(path)
print('Recovery: transaction rolled back; disposable database deleted')
