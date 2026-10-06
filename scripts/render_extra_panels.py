import os, html

OUT = os.path.join(os.path.dirname(__file__), "..")

BG="#0d1117"; BG2="#111722"; TILE="#161b22"; FRAME="#30363d"
MUTED="#7d8590"; INK="#e6edf3"; GREEN="#39d353"; BLUE="#79c0ff"; PURPLE="#bc8cff"

def panel(title, body, filename, height=420):
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{height}" viewBox="0 0 840 {height}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
<style>
@keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes pulse{{0%,100%{{opacity:.65}}50%{{opacity:1}}}}
.t{{animation:in .6s ease-out both}}
.p{{animation:pulse 2s ease-in-out infinite}}
</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>
</linearGradient></defs>
<rect width="840" height="{height}" rx="12" fill="url(#bg)"/>
<rect x=".5" y=".5" width="839" height="{height-1}" rx="12" fill="none" stroke="{FRAME}"/>
<line x1="0" y1="30" x2="840" y2="30" stroke="{FRAME}"/>
<circle cx="20" cy="15" r="5" fill="#ff5f56"/><circle cx="36" cy="15" r="5" fill="#ffbd2e"/><circle cx="52" cy="15" r="5" fill="#27c93f"/>
<text x="420" y="19" text-anchor="middle" fill="{MUTED}" font-size="12">sairaja@github: ~$ ./{title}.sh</text>
{body}
</svg>'''
    with open(os.path.join(OUT,filename),"w",encoding="utf-8",newline="\n") as f:f.write(s)

# TECH STACK
langs=[
("JavaScript",330819,BLUE),("TypeScript",199333,"#3178c6"),
("Java",61781,"#f89820"),("CSS",41320,PURPLE),("HTML",10552,"#e34c26"),("Shell",632,GREEN)]
total=sum(x[1] for x in langs)
body='<g class="t">'
body+=f'<text x="28" y="68" fill="{INK}" font-size="21" font-weight="700">$ technology stack</text>'
body+=f'<text x="28" y="94" fill="{MUTED}" font-size="13">languages detected from your GitHub repositories</text>'
y=135
for i,(name,n,color) in enumerate(langs):
    pct=n/total*100
    body+=f'<text x="28" y="{y}" fill="{MUTED}" font-size="16">{name}</text>'
    body+=f'<rect x="170" y="{y-14}" width="500" height="12" rx="6" fill="{FRAME}"/>'
    body+=f'<rect x="170" y="{y-14}" width="{max(3,500*pct/100):.1f}" height="12" rx="6" fill="{color}"/>'
    body+=f'<text x="690" y="{y}" fill="{INK}" font-size="15">{pct:.1f}%</text>'
    y+=40
body+=f'<text x="28" y="{y+15}" fill="{MUTED}" font-size="15">frameworks → React • Spring Boot • Node.js • REST APIs</text>'
body+=f'<text x="28" y="{y+45}" fill="{MUTED}" font-size="15">cloud → AWS • Amplify • GitHub Actions</text>'
body+=f'<text x="28" y="{y+75}" fill="{MUTED}" font-size="15">data → MySQL • MongoDB • PostgreSQL</text></g>'
panel("tech-stack",body,"tech-stack.svg",500)

# PROJECTS
projects=[
("F1 COMMAND CENTER","Telemetry • WebSockets • data visualization"),
("CRICKET ANALYTICS","Live data • analytics • dashboard"),
("SMART CITY","React • Spring Boot • MySQL"),
("CAMPUS SERVICE","AWS Amplify • full-stack • cloud"),
]
body=f'<g class="t"><text x="28" y="68" fill="{INK}" font-size="21" font-weight="700">$ ./projects --featured</text>'
y=115
for i,(name,desc) in enumerate(projects):
    body+=f'<rect x="24" y="{y-28}" width="792" height="70" rx="9" fill="{TILE}" stroke="{FRAME}"/>'
    body+=f'<text x="46" y="{y}" fill="{GREEN}" font-size="16">$ open</text>'
    body+=f'<text x="145" y="{y}" fill="{BLUE}" font-size="17" font-weight="700">{name}</text>'
    body+=f'<text x="145" y="{y+25}" fill="{MUTED}" font-size="13">{desc}</text>'
    y+=84
body+='</g>'
panel("projects",body,"projects.svg",470)

# SYSTEM
rows=[
("role","Student Developer",GREEN),("focus","AI / ML",BLUE),
("frontend","React / TypeScript",PURPLE),("backend","Spring Boot",BLUE),
("cloud","AWS / Amplify",GREEN),("database","MySQL / MongoDB",PURPLE),
("status","BUILDING",GREEN)]
body=f'<g class="t"><text x="28" y="68" fill="{INK}" font-size="21" font-weight="700">$ ./system-info</text>'
y=112
for k,v,c in rows:
    body+=f'<text x="45" y="{y}" fill="{MUTED}" font-size="16">{k:<12}</text>'
    body+=f'<text x="205" y="{y}" fill="{c}" font-size="17">{v}</text>'
    y+=42
body+='</g>'
panel("system-info",body,"system-info.svg",400)

# FUN FACT
body=f'''<g class="t">
<text x="28" y="68" fill="{INK}" font-size="21" font-weight="700">$ ./fun-fact</text>
<rect x="24" y="95" width="792" height="170" rx="10" fill="{TILE}" stroke="{FRAME}"/>
<text x="48" y="145" fill="{GREEN}" font-size="18">⚡ fun fact</text>
<text x="48" y="185" fill="{INK}" font-size="18">I optimize animations nobody asked for...</text>
<text x="48" y="220" fill="{MUTED}" font-size="16">and then optimize them again. 😎</text>
<text x="48" y="252" fill="{MUTED}" font-size="12">status: unnecessarily polished</text>
</g>'''
panel("fun-fact",body,"fun-fact.svg",310)

# CONNECT
links=[
("GitHub","https://github.com/SAIRAJA-2K7",GREEN),
("LinkedIn","https://www.linkedin.com/in/sairajakrishna/",BLUE),
("Portfolio","https://sairajakrishna.netlify.app/",PURPLE),
("Email","mailto:2400031695cse2@gmail.com",INK)]
body=f'<g class="t"><text x="28" y="68" fill="{INK}" font-size="21" font-weight="700">$ ./connect</text>'
y=120
for name,url,c in links:
    body+=f'<a href="{html.escape(url,quote=True)}"><rect x="24" y="{y-30}" width="792" height="55" rx="9" fill="{TILE}" stroke="{FRAME}"/>'
    body+=f'<text x="48" y="{y+5}" fill="{c}" font-size="17">→ {name}</text>'
    body+=f'<text x="210" y="{y+5}" fill="{MUTED}" font-size="13">{html.escape(url)}</text></a>'
    y+=68
body+='</g>'
panel("connect",body,"connect.svg",410)

print("Created:")
for x in ["tech-stack.svg","projects.svg","system-info.svg","fun-fact.svg","connect.svg"]:
    print(" ",x)
