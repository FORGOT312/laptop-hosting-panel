#!/usr/bin/env python3
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os, json, bcrypt, jwt, sqlite3, subprocess, threading, queue, psutil, shutil, hashlib, time
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hostpanel-secret-2024')
CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

DB_PATH    = './data/panel.db'
SERVERS_DIR = './servers'
for d in ['./data','./logs', SERVERS_DIR]:
    os.makedirs(d, exist_ok=True)

# ── DATABASE ──────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT UNIQUE NOT NULL,
            password   TEXT NOT NULL,
            email      TEXT DEFAULT '',
            role       TEXT DEFAULT 'user',
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS servers (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            type        TEXT NOT NULL,
            subtype     TEXT DEFAULT '',
            config      TEXT DEFAULT '{}',
            working_dir TEXT NOT NULL,
            port        INTEGER,
            owner_id    INTEGER,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(owner_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS console_logs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT,
            line      TEXT,
            ts        TEXT DEFAULT (datetime('now'))
        );
    ''')
    pw = bcrypt.hashpw(b'admin', bcrypt.gensalt()).decode()
    c.execute("INSERT OR IGNORE INTO users (username,password,role) VALUES (?,?,?)",
              ('admin', pw, 'admin'))
    conn.commit(); conn.close()
    print('✅ DB ready')

init_db()

# ── AUTH ──────────────────────────────────────────────────────────────────────
def token_required(f):
    @wraps(f)
    def d(*args, **kwargs):
        t = request.headers.get('Authorization','').replace('Bearer ','')
        if not t: return jsonify({'error':'Token required'}), 401
        try: data = jwt.decode(t, app.config['SECRET_KEY'], algorithms=['HS256'])
        except: return jsonify({'error':'Invalid token'}), 401
        return f(data, *args, **kwargs)
    return d

@app.route('/api/auth/login', methods=['POST'])
def login():
    d = request.json or {}
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE username=?", (d.get('username',''),)).fetchone()
    conn.close()
    if not u or not bcrypt.checkpw(d.get('password','').encode(), u['password'].encode()):
        return jsonify({'error':'Неверный логин или пароль'}), 401
    token = jwt.encode(
        {'id':u['id'],'username':u['username'],'role':u['role'],
         'exp': datetime.utcnow()+timedelta(hours=24)},
        app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token':token,'username':u['username'],'role':u['role']})

@app.route('/api/auth/register', methods=['POST'])
def register():
    d = request.json or {}
    if not d.get('username') or not d.get('password'):
        return jsonify({'error':'Логин и пароль обязательны'}), 400
    if len(d['password']) < 4:
        return jsonify({'error':'Пароль минимум 4 символа'}), 400
    pw = bcrypt.hashpw(d['password'].encode(), bcrypt.gensalt()).decode()
    try:
        conn = get_db()
        conn.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)",
                     (d['username'].strip(), pw, d.get('email','')))
        conn.commit(); conn.close()
        return jsonify({'message':'Аккаунт создан'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error':'Логин уже занят'}), 409

# ── RUNNING PROCESSES ─────────────────────────────────────────────────────────
running = {}   # sid -> {process, queue}

def _reader(sid, proc):
    conn = get_db()
    for line in iter(proc.stdout.readline, ''):
        line = line.rstrip('\n\r')
        if not line: continue
        try: running[sid]['queue'].put_nowait(line)
        except: pass
        conn.execute("INSERT INTO console_logs (server_id,line) VALUES (?,?)", (sid,line))
        conn.commit()
        socketio.emit('console_line', {'server_id':sid,'line':line})
    conn.close()

def srv_status(sid):
    if sid in running:
        if running[sid]['process'].poll() is None: return 'running'
        del running[sid]
    return 'stopped'

def get_srv_stats(sid, pid):
    try:
        p = psutil.Process(pid)
        mi = p.memory_info()
        return {'cpu': round(p.cpu_percent(interval=0.1),1),
                'memory_mb': round(mi.rss/1024/1024,1),
                'memory': mi.rss}
    except: return {'cpu':0,'memory_mb':0,'memory':0}

# ── SERVERS CRUD ──────────────────────────────────────────────────────────────
@app.route('/api/servers', methods=['GET'])
@token_required
def list_servers(u):
    conn = get_db()
    rows = conn.execute("SELECT * FROM servers WHERE owner_id=? ORDER BY created_at DESC",
                        (u['id'],)).fetchall()
    conn.close()
    out = []
    for r in rows:
        s = dict(r)
        s['status'] = srv_status(s['id'])
        s['config'] = json.loads(s['config'] or '{}')
        if s['status']=='running':
            s['stats'] = get_srv_stats(s['id'], running[s['id']]['process'].pid)
        else:
            s['stats'] = {'cpu':0,'memory_mb':0,'memory':0}
        out.append(s)
    return jsonify(out)

@app.route('/api/servers', methods=['POST'])
@token_required
def create_server(u):
    d = request.json or {}
    if not d.get('name'): return jsonify({'error':'Название обязательно'}), 400
    sid = hashlib.md5(f"{d['name']}{time.time()}".encode()).hexdigest()[:16]
    wd  = os.path.join(SERVERS_DIR, sid)
    os.makedirs(wd, exist_ok=True)
    conn = get_db()
    conn.execute(
        "INSERT INTO servers (id,name,type,subtype,config,working_dir,port,owner_id) VALUES (?,?,?,?,?,?,?,?)",
        (sid, d['name'], d.get('type','custom'), d.get('subtype',''),
         json.dumps(d.get('config',{})), wd, d.get('port'), u['id']))
    conn.commit(); conn.close()
    return jsonify({'id':sid}), 201

@app.route('/api/servers/<sid>', methods=['GET'])
@token_required
def get_server(u, sid):
    conn = get_db()
    r = conn.execute("SELECT * FROM servers WHERE id=? AND owner_id=?",(sid,u['id'])).fetchone()
    conn.close()
    if not r: return jsonify({'error':'Not found'}), 404
    s = dict(r); s['status']=srv_status(sid); s['config']=json.loads(s['config'] or '{}')
    if s['status']=='running':
        s['stats'] = get_srv_stats(sid, running[sid]['process'].pid)
    else: s['stats'] = {'cpu':0,'memory_mb':0,'memory':0}
    return jsonify(s)

@app.route('/api/servers/<sid>', methods=['PUT'])
@token_required
def update_server(u, sid):
    conn = get_db()
    r = conn.execute("SELECT * FROM servers WHERE id=? AND owner_id=?",(sid,u['id'])).fetchone()
    if not r: conn.close(); return jsonify({'error':'Not found'}), 404
    d = request.json or {}
    cfg = json.loads(r['config'] or '{}')
    cfg.update(d.get('config',{}))
    conn.execute("UPDATE servers SET name=?,port=?,config=? WHERE id=?",
                 (d.get('name',r['name']), d.get('port',r['port']),
                  json.dumps(cfg), sid))
    conn.commit(); conn.close()
    return jsonify({'message':'Updated'})

@app.route('/api/servers/<sid>', methods=['DELETE'])
@token_required
def delete_server(u, sid):
    conn = get_db()
    r = conn.execute("SELECT * FROM servers WHERE id=? AND owner_id=?",(sid,u['id'])).fetchone()
    if not r: conn.close(); return jsonify({'error':'Not found'}), 404
    if srv_status(sid)=='running':
        running[sid]['process'].terminate()
        del running[sid]
    try: shutil.rmtree(r['working_dir'])
    except: pass
    conn.execute("DELETE FROM servers WHERE id=?",(sid,))
    conn.execute("DELETE FROM console_logs WHERE server_id=?",(sid,))
    conn.commit(); conn.close()
    return jsonify({'message':'Deleted'})

# ── START / STOP / RESTART ────────────────────────────────────────────────────
@app.route('/api/servers/<sid>/start', methods=['POST'])
@token_required
def start_server(u, sid):
    conn = get_db()
    r = conn.execute("SELECT * FROM servers WHERE id=? AND owner_id=?",(sid,u['id'])).fetchone()
    conn.close()
    if not r: return jsonify({'error':'Not found'}), 404
    if srv_status(sid)=='running': return jsonify({'error':'Already running'}), 400
    cfg = json.loads(r['config'] or '{}')
    cmd = cfg.get('start_command')
    if not cmd: return jsonify({'error':'Команда запуска не задана. Задайте её в настройках.'}), 400
    wd = r['working_dir']
    try:
        env = os.environ.copy()
        if cfg.get('env_vars'):
            for line in cfg['env_vars'].split('\n'):
                if '=' in line:
                    k,v = line.split('=',1); env[k.strip()]=v.strip()
        p = subprocess.Popen(cmd, shell=True, cwd=wd, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.PIPE, universal_newlines=True, bufsize=1)
        running[sid] = {'process':p,'queue':queue.Queue(500)}
        threading.Thread(target=_reader, args=(sid,p), daemon=True).start()
        return jsonify({'message':'Started'})
    except Exception as e: return jsonify({'error':str(e)}), 500

@app.route('/api/servers/<sid>/stop', methods=['POST'])
@token_required
def stop_server(u, sid):
    if sid not in running: return jsonify({'error':'Not running'}), 400
    p = running[sid]['process']
    p.terminate()
    try: p.wait(timeout=10)
    except: p.kill()
    del running[sid]
    return jsonify({'message':'Stopped'})

@app.route('/api/servers/<sid>/restart', methods=['POST'])
@token_required
def restart_server(u, sid):
    if srv_status(sid)=='running':
        running[sid]['process'].terminate()
        try: running[sid]['process'].wait(timeout=5)
        except: running[sid]['process'].kill()
        del running[sid]
    return start_server(u, sid)

@app.route('/api/servers/<sid>/command', methods=['POST'])
@token_required
def send_cmd(u, sid):
    cmd = (request.json or {}).get('command','')
    if sid not in running: return jsonify({'error':'Not running'}), 400
    try:
        running[sid]['process'].stdin.write(cmd+'\n')
        running[sid]['process'].stdin.flush()
        return jsonify({'message':'Sent'})
    except Exception as e: return jsonify({'error':str(e)}), 500

@app.route('/api/servers/<sid>/console', methods=['GET'])
@token_required
def get_console(u, sid):
    limit = request.args.get('limit',300,type=int)
    conn = get_db()
    rows = conn.execute(
        "SELECT line,ts FROM console_logs WHERE server_id=? ORDER BY id DESC LIMIT ?",
        (sid,limit)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in reversed(rows)])

# ── FILE MANAGER ──────────────────────────────────────────────────────────────
def safe_path(base, rel):
    t = os.path.realpath(os.path.join(base, rel.lstrip('/')))
    if not t.startswith(os.path.realpath(base)):
        raise PermissionError('Access denied')
    return t

def get_wd(u, sid):
    conn = get_db()
    r = conn.execute("SELECT working_dir FROM servers WHERE id=? AND owner_id=?",(sid,u['id'])).fetchone()
    conn.close()
    if not r: raise FileNotFoundError('Server not found')
    return r['working_dir']

@app.route('/api/servers/<sid>/files', methods=['GET'])
@token_required
def list_files(u, sid):
    try:
        base = get_wd(u, sid)
        rel  = request.args.get('path','')
        target = safe_path(base, rel)
        if not os.path.isdir(target): return jsonify({'error':'Not a directory'}), 400
        entries = []
        for name in sorted(os.listdir(target)):
            full = os.path.join(target,name)
            st   = os.stat(full)
            entries.append({'name':name,'type':'dir' if os.path.isdir(full) else 'file',
                            'size':st.st_size,
                            'modified':datetime.fromtimestamp(st.st_mtime).isoformat()})
        entries.sort(key=lambda x:(x['type']=='file', x['name'].lower()))
        return jsonify({'path':rel,'entries':entries})
    except PermissionError as e: return jsonify({'error':str(e)}), 403
    except Exception as e: return jsonify({'error':str(e)}), 500

@app.route('/api/servers/<sid>/files/read', methods=['GET'])
@token_required
def read_file(u, sid):
    try:
        base   = get_wd(u, sid)
        target = safe_path(base, request.args.get('path',''))
        with open(target,'r',errors='replace') as f: return jsonify({'content':f.read()})
    except PermissionError as e: return jsonify({'error':str(e)}), 403
    except Exception as e: return jsonify({'error':str(e)}), 500

@app.route('/api/servers/<sid>/files/write', methods=['POST'])
@token_required
def write_file(u, sid):
    try:
        base   = get_wd(u, sid)
        target = safe_path(base, (request.json or {}).get('path',''))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target,'w') as f: f.write((request.json or {}).get('content',''))
        return jsonify({'message':'Saved'})
    except PermissionError as e: return jsonify({'error':str(e)}), 403
    except Exception as e: return jsonify({'error':str(e)}), 500

@app.route('/api/servers/<sid>/files/delete', methods=['DELETE'])
@token_required
def delete_file(u, sid):
    try:
        base   = get_wd(u, sid)
        target = safe_path(base, (request.json or {}).get('path',''))
        if os.path.isdir(target): shutil.rmtree(target)
        else: os.remove(target)
        return jsonify({'message':'Deleted'})
    except PermissionError as e: return jsonify({'error':str(e)}), 403
    except Exception as e: return jsonify({'error':str(e)}), 500

# ── SYSTEM STATS ──────────────────────────────────────────────────────────────
@app.route('/api/system/stats')
def system_stats():
    mem  = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net  = psutil.net_io_counters()
    return jsonify({
        'cpu': psutil.cpu_percent(interval=0.5),
        'memory': {'used_gb':round(mem.used/1024**3,2),
                   'total_gb':round(mem.total/1024**3,2),
                   'percent':mem.percent},
        'disk': {'used_gb':round(disk.used/1024**3,1),
                 'total_gb':round(disk.total/1024**3,1),
                 'percent':disk.percent},
        'network': {'bytes_sent':net.bytes_sent,'bytes_recv':net.bytes_recv}
    })

# ── FRONTEND ──────────────────────────────────────────────────────────────────
@app.route('/', defaults={'p':''})
@app.route('/<path:p>')
def frontend(p=''):
    html = os.path.abspath(os.path.join(os.path.dirname(__file__),'../frontend/index.html'))
    return send_file(html)

# ── WEBSOCKET ─────────────────────────────────────────────────────────────────
@socketio.on('connect')
def on_connect(): emit('connected',{'ok':True})

def _broadcast():
    while True:
        time.sleep(2)
        try:
            mem = psutil.virtual_memory(); net = psutil.net_io_counters()
            socketio.emit('stats_update',{
                'cpu': psutil.cpu_percent(interval=0),
                'memory':{'used_gb':round(mem.used/1024**3,2),
                          'total_gb':round(mem.total/1024**3,2),
                          'percent':mem.percent},
                'network':{'bytes_sent':net.bytes_sent,'bytes_recv':net.bytes_recv}
            })
        except: pass

threading.Thread(target=_broadcast, daemon=True).start()

if __name__=='__main__':
    print('🚀 HostPanel v2.0  →  http://localhost:5000')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
