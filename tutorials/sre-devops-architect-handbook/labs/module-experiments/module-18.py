#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import sqlite3,tempfile,os,shutil,time
folder=tempfile.mkdtemp();source=os.path.join(folder,'source.sqlite');backup=os.path.join(folder,'backup.sqlite')
try:
 db=sqlite3.connect(source);db.execute('create table t(v text)');db.execute("insert into t values ('before backup')");db.commit()
 with sqlite3.connect(backup) as b:db.backup(b)
 db.execute("insert into t values ('after backup')");db.commit();db.close()
 with sqlite3.connect(backup) as b:print('restored rows:',b.execute('select * from t').fetchall())
 print('failure: post-backup write not restored; RPO is nonzero')
finally:shutil.rmtree(folder)
print('recovery: validate backup and measure actual restore duration')
