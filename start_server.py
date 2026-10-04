#!/usr/bin/env python3
import json, sqlite3, hashlib, secrets, os, mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WEB=ROOT/'web'; DB=ROOT/'english_with_filipe.db'; PORT=8000

def hashpw(pw,salt=None):
    salt=salt or secrets.token_hex(16)
    h=hashlib.pbkdf2_hmac('sha256',pw.encode(),salt.encode(),120000).hex()
    return salt+'$'+h

def verify(pw,stored):
    try:
        salt,h=stored.split('$',1); return hashlib.pbkdf2_hmac('sha256',pw.encode(),salt.encode(),120000).hex()==h
    except: return False

def db():
    c=sqlite3.connect(DB,check_same_thread=False); c.row_factory=sqlite3.Row
    c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL DEFAULT "student",created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,quiz_id TEXT,level TEXT,score INTEGER,total INTEGER,answers_json TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id INTEGER,created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    c.commit(); return c
c=db()
def seed(email,name,pw,role):
    if not c.execute('select id from users where email=?',(email,)).fetchone(): c.execute('insert into users(name,email,password,role) values(?,?,?,?)',(name,email,hashpw(pw),role)); c.commit()
seed('teacher@englishwithfilipe.com','Filipe','Filipe2026!','teacher')
seed('student@englishwithfilipe.com','Demo Student','English123!','student')

def recs(errors):
    mapping={'meaning':'Review meaning in context and contrast near-synonyms.','vocabulary':'Build a small active vocabulary set and use each word in two original sentences.','usage':'Practice the language in different sentence patterns and communicative situations.','precision':'Compare related words and choose based on context and register.','grammar':'Revisit the grammar point, model the structure, then make the student produce it in three new contexts.'}
    out=[]
    for e in errors:
        skill=e['skill']; n=e['count']; topic=e['topic']
        out.append({'skill':skill,'topic':topic,'count':n,'recommendation':mapping.get(skill,'Revisit the topic through guided practice and new examples.')})
    return out
class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        if path.startswith('/api/'): return ''
        p=path.split('?',1)[0]
        return str((WEB/p.lstrip('/')).resolve()) if (WEB/p.lstrip('/')).exists() else str(WEB/'index.html')
    def json(self,code,obj):
        raw=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('Cache-Control','no-store, no-cache, must-revalidate'); self.end_headers(); self.wfile.write(raw)
    def end_headers(self):
        self.send_header('Cache-Control','no-store, no-cache, must-revalidate')
        self.send_header('Pragma','no-cache')
        super().end_headers()
    def body(self):
        n=int(self.headers.get('Content-Length','0')); return json.loads(self.rfile.read(n) or '{}')
    def user(self):
        token=self.headers.get('Cookie','').replace('ewf_session=','').split(';')[0].strip()
        if not token: return None
        row=c.execute('select u.* from sessions s join users u on u.id=s.user_id where s.token=?',(token,)).fetchone(); return dict(row) if row else None
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/api/me':
            user=self.user(); 
            if user: user.pop('password',None)
            self.json(200,{'authenticated':bool(user),'user':user}); return
        if u.path=='/api/teacher/overview':
            user=self.user()
            if not user or user['role']!='teacher': return self.json(403,{'error':'Teacher access required'})
            students=[dict(x) for x in c.execute('select id,name,email,created_at from users where role="student" order by name')]
            data=[]
            for s in students:
                a=c.execute('select count(*) n,coalesce(avg(score*100.0/total),0) avg from attempts where user_id=?',(s['id'],)).fetchone()
                last=c.execute('select level,score,total,created_at from attempts where user_id=? order by id desc limit 1',(s['id'],)).fetchone()
                data.append({**s,'tests':a['n'],'average':round(a['avg'],1),'last':dict(last) if last else None})
            self.json(200,{'students':data}); return
        if u.path=='/api/teacher/student':
            user=self.user()
            if not user or user['role']!='teacher': return self.json(403,{'error':'Teacher access required'})
            sid=parse_qs(u.query).get('id',[''])[0]
            s=c.execute('select id,name,email from users where id=? and role="student"',(sid,)).fetchone()
            if not s:return self.json(404,{'error':'Student not found'})
            attempts=[dict(x) for x in c.execute('select id,quiz_id,level,score,total,answers_json,created_at from attempts where user_id=? order by id desc',(sid,))]
            errors={}
            for a in attempts:
                for q in json.loads(a['answers_json']):
                    if not q.get('correct'):
                        key=(q.get('skill','unknown'),q.get('topic','general')); errors[key]=errors.get(key,0)+1
            err=[{'skill':k[0],'topic':k[1],'count':n} for k,n in sorted(errors.items(),key=lambda x:-x[1])]
            self.json(200,{'student':dict(s),'attempts':attempts,'diagnosis':recs(err)}); return
        return super().do_GET()
    def do_POST(self):
        u=urlparse(self.path); data=self.body()
        if u.path=='/api/login':
            row=c.execute('select * from users where email=?',(data.get('email','').lower().strip(),)).fetchone()
            if not row or not verify(data.get('password',''),row['password']): return self.json(401,{'error':'Email or password incorrect.'})
            token=secrets.token_urlsafe(32); c.execute('insert into sessions(token,user_id) values(?,?)',(token,row['id'])); c.commit()
            self.send_response(200); self.send_header('Set-Cookie',f'ewf_session={token}; Path=/; HttpOnly; SameSite=Lax'); self.send_header('Content-Type','application/json'); self.end_headers(); u=dict(row); u.pop('password',None); self.wfile.write(json.dumps({'ok':True,'user':u}).encode()); return
        if u.path=='/api/logout':
            tok=self.headers.get('Cookie','').replace('ewf_session=','').split(';')[0].strip(); c.execute('delete from sessions where token=?',(tok,)); c.commit(); self.send_response(200); self.send_header('Set-Cookie','ewf_session=; Path=/; Max-Age=0'); self.end_headers(); return
        if u.path=='/api/register':
            name=data.get('name','').strip(); email=data.get('email','').lower().strip(); pw=data.get('password','')
            if not name or not email or len(pw)<6:return self.json(400,{'error':'Name, email and a password with at least 6 characters are required.'})
            try:
                cur=c.execute('insert into users(name,email,password,role) values(?,?,?,"student")',(name,email,hashpw(pw))); c.commit(); uid=cur.lastrowid
                token=secrets.token_urlsafe(32); c.execute('insert into sessions(token,user_id) values(?,?)',(token,uid)); c.commit()
                self.send_response(200); self.send_header('Set-Cookie',f'ewf_session={token}; Path=/; HttpOnly; SameSite=Lax'); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps({'ok':True,'user':{'id':uid,'name':name,'email':email,'role':'student'}}).encode()); return
            except sqlite3.IntegrityError:return self.json(409,{'error':'That email is already registered.'})
        if u.path=='/api/attempt':
            user=self.user()
            if not user:return self.json(401,{'error':'Please log in first.'})
            level=data.get('level',''); score=int(data.get('score',0)); total=int(data.get('total',10)); answers=data.get('answers',[])
            c.execute('insert into attempts(user_id,quiz_id,level,score,total,answers_json) values(?,?,?,?,?,?)',(user['id'],data.get('quiz_id',''),level,score,total,json.dumps(answers,ensure_ascii=False))); c.commit(); self.json(200,{'ok':True}); return
        return self.json(404,{'error':'Not found'})

def main():
    os.chdir(WEB); print(f'English with Filipe — HTTP server: http://localhost:{PORT}')
    print('Teacher credentials are stored only in PRIVATE_TEACHER_NOTES.txt.')
    ThreadingHTTPServer(('0.0.0.0',PORT),Handler).serve_forever()
if __name__=='__main__': main()
