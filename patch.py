import json,re,zipfile,os,shutil
base='/mnt/data/v67fix/web'
# Localize explanation how-to and mistakes.
p=os.path.join(base,'explanations.json')
data=json.load(open(p,encoding='utf-8'))
# Specific translations for basic concepts; generic but grammatically natural fallback for all advanced concepts.
specific={
'noun':('Use um substantivo para nomear a pessoa, o lugar, a coisa, a ideia ou a atividade de que você está falando.','Folosește un substantiv pentru a denumi persoana, locul, lucrul, ideea sau activitatea despre care vorbești.'),
'verb':('Use um verbo para expressar uma ação, acontecimento ou estado. Verifique o tempo verbal e o sujeito antes de falar.','Folosește un verb pentru a exprima o acțiune, un eveniment sau o stare. Verifică timpul verbal și subiectul înainte de a vorbi.'),
'adjective':('Coloque um adjetivo antes de um substantivo ou depois de um verbo de ligação para descrever o substantivo ou o sujeito.','Pune un adjectiv înaintea unui substantiv sau după un verb copulativ pentru a descrie substantivul sau subiectul.'),
'adverb':('Use um advérbio para acrescentar informações sobre como, quando, onde ou com que frequência algo acontece.','Folosește un adverb pentru a adăuga informații despre cum, când, unde sau cât de des se întâmplă ceva.'),
'pronoun':('Use um pronome no lugar de repetir um substantivo quando a referência estiver clara.','Folosește un pronume în loc să repeți un substantiv atunci când referința este clară.'),
'determiner':('Use um determinante antes de um substantivo para indicar qual, de quem, quantos ou quanto.','Folosește un determinant înaintea unui substantiv pentru a arăta care, al cui, câți sau cât.'),
'article':('Use a/an com um substantivo contável singular não específico e the quando o ouvinte consegue identificar o substantivo.','Folosește a/an cu un substantiv numărabil singular nespecific și the atunci când ascultătorul poate identifica substantivul.'),
'preposition':('Use uma preposição para ligar um substantivo ou pronome a outra parte da frase, geralmente indicando tempo ou lugar.','Folosește o prepoziție pentru a lega un substantiv sau pronume de o altă parte a propoziției, adesea pentru timp sau loc.'),
'conjunction':('Use uma conjunção para ligar palavras, expressões ou orações e mostrar a relação entre elas.','Folosește o conjuncție pentru a lega cuvinte, expresii sau propoziții și pentru a arăta relația dintre ele.'),
'auxiliary':('Use um verbo auxiliar para formar perguntas, negativas, tempos verbais e estruturas de ênfase.','Folosește un verb auxiliar pentru a forma întrebări, negații, timpuri verbale și structuri de accentuare.'),
'modal':('Use um modal antes do verbo na forma base para expressar capacidade, possibilidade, permissão, obrigação ou dedução.','Folosește un verb modal înaintea verbului la forma de bază pentru a exprima abilitate, posibilitate, permisiune, obligație sau deducție.'),
}
term_pt={x['id']:x['title_pt'] for x in data}; term_ro={x['id']:x['title_ro'] for x in data}
for x in data:
    i=x['id']; termpt=term_pt[i]; termro=term_ro[i]
    if i in specific: hpt,hro=specific[i]
    else:
        hpt=f'Use {termpt} no contexto explicado na definição, prestando atenção aos padrões dos exemplos e ao nível de formalidade.'
        hro=f'Folosește {termro} în contextul explicat în definiție, acordând atenție modelelor din exemple și nivelului de formalitate.'
    # More natural common-mistakes translations for all entries.
    ept='Verifique a estrutura e o significado em vez de traduzir palavra por palavra.'
    ero='Verifică structura și sensul în loc să traduci cuvânt cu cuvânt.'
    if i=='noun': ept='Não confunda substantivos contáveis e incontáveis; verifique as formas singular e plural.'; ero='Nu confunda substantivele numărabile cu cele nenumărabile; verifică formele de singular și plural.'
    elif i=='verb': ept='Não se esqueça da concordância entre sujeito e verbo nem do tempo verbal correto.'; ero='Nu uita de acordul dintre subiect și verb și de timpul verbal corect.'
    elif i=='adjective': ept='Não use um adjetivo quando a frase exigir um advérbio.'; ero='Nu folosi un adjectiv atunci când este necesar un adverb.'
    elif i=='adverb': ept='Verifique a posição do advérbio e não use por engano a forma de adjetivo.'; ero='Verifică poziția adverbului și nu folosi din greșeală forma de adjectiv.'
    elif i=='pronoun': ept='Certifique-se de que o pronome se refere claramente ao substantivo pretendido.'; ero='Asigură-te că pronumele se referă clar la substantivul dorit.'
    elif i=='determiner': ept='Não combine determinantes em combinações incorretas.'; ero='Nu combina determinanți în combinații incorecte.'
    elif i=='article': ept='Não use a/an com substantivos plurais ou incontáveis.'; ero='Nu folosi a/an cu substantive la plural sau nenumărabile.'
    elif i=='preposition': ept='Evite traduzir preposições palavra por palavra do português ou do romeno.'; ero='Evită traducerea prepozițiilor cuvânt cu cuvânt din portugheză sau română.'
    x['how_to_use']['pt']=hpt; x['how_to_use']['ro']=hro
    x['common_mistakes']['pt']=ept; x['common_mistakes']['ro']=ero
json.dump(data,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

html=open('/mnt/data/v67fix/web/index.html',encoding='utf-8').read()
# Add localized UI keys before footer in each language object.
html=html.replace("storyLabel:'About me',footer:", "storyLabel:'About me',vocabLibrary:'Vocabulary library',uniqueItems:'unique learning items.',aiLab:'AI Lab',testsIntro:'Original English with Filipe tests.',testsDescription:'Practice grammar, vocabulary, reading, cloze, transformations and functional language.',questionDescription:'questions with feedback and a final score.',loading:'Loading...',noStudents:'No students registered yet.',teacherLoadError:'Teacher Lab could not load.',footer:")
html=html.replace("storyLabel:'Sobre mim',footer:", "storyLabel:'Sobre mim',vocabLibrary:'Biblioteca de vocabulário',uniqueItems:'itens de aprendizagem únicos.',aiLab:'Laboratório de testes',testsIntro:'Testes originais English with Filipe.',testsDescription:'Pratique gramática, vocabulário, leitura, cloze, transformações e linguagem funcional.',questionDescription:'questões com feedback e pontuação final.',loading:'Carregando...',noStudents:'Nenhum aluno cadastrado ainda.',teacherLoadError:'A Área do Professor não pôde ser carregada.',footer:")
html=html.replace("storyLabel:'Despre mine',footer:", "storyLabel:'Despre mine',vocabLibrary:'Biblioteca de vocabular',uniqueItems:'elemente de învățare unice.',aiLab:'Laborator de teste',testsIntro:'Teste originale English with Filipe.',testsDescription:'Exersează gramatica, vocabularul, citirea, exercițiile cloze, transformările și limbajul funcțional.',questionDescription:'întrebări cu feedback și scor final.',loading:'Se încarcă...',noStudents:'Nu există încă elevi înregistrați.',teacherLoadError:'Zona profesorului nu a putut fi încărcată.',footer:")
# Hero highlight helper and renderHome replacement.
marker="function route(view){activeView=view||'home';"
helper="function heroTitleHTML(){const parts=t('heroTitle').split('. ');return parts.map((p,i)=>i===1?`<span>${esc(p)}.</span>`:esc(p)+(i<parts.length-1?'. ':'' )).join('')}\n"
html=html.replace(marker,helper+marker)
html=html.replace("<h1>${esc(t('heroTitle')).replace('Practice.', '<span>Practice.</span>')}</h1>","<h1>${heroTitleHTML()}</h1>")
# Localize explanation category labels and count, and title stays learning term localized.
catmap="const CAT_UI={en:{'grammar & language':'Grammar & language','parts of speech':'Parts of speech','grammar':'Grammar'},pt:{'grammar & language':'Gramática e linguagem','parts of speech':'Classes de palavras','grammar':'Gramática'},ro:{'grammar & language':'Gramatică și limbaj','parts of speech':'Părți de vorbire','grammar':'Gramatică'}};\n"
html=html.replace("function renderExplain(){",catmap+"function renderExplain(){")
old="const cats=[...new Set(explanations.map(x=>x.category||'grammar'))].sort();"
new="const cats=[...new Set(explanations.map(x=>x.category||'grammar'))].sort();"
# Replace the full drawExplain function.
start=html.index('function drawExplain(){')
end=html.index('\nfunction ',start+10)
newfunc="""function drawExplain(){const q=($('#explainSearch')?.value||'').toLowerCase().trim(),lv=$('#explainLevel')?.value||'',cat=$('#explainCat')?.value||'';const arr=explanations.filter(x=>(!lv||x.level===lv)&&(!cat||x.category===cat)&&(!q||JSON.stringify(x).toLowerCase().includes(q)));$('#explainCount').textContent=`${arr.length} ${lang==='pt'?'explicações':lang==='ro'?'explicații':'explanations'}`;$('#explainCards').innerHTML=arr.map(x=>{const d=x.definition?.[lang]||x.definition?.en||'';const how=x.how_to_use?.[lang]||'';const mistakes=x.common_mistakes?.[lang]||'';const catName=(CAT_UI[lang]||CAT_UI.en)[x.category||'grammar']||x.category||'Grammar';return `<article class=\"explain-card\"><div class=\"chip\">${esc(x.level)} · ${esc(catName)}</div><h3>${esc(lang==='pt'?x.title_pt:lang==='ro'?x.title_ro:x.title_en)}</h3><div class=\"translation\">${esc(x.title_en)}</div><p><strong>${lang.toUpperCase()}:</strong> ${esc(d)}</p><p><strong>${t('how')}:</strong> ${esc(how)}</p><p><strong>${t('mistakes')}:</strong> ${esc(mistakes)}</p><div class=\"example\"><strong>${t('examples')}</strong><br>${(x.examples||[]).map(esc).join('<br>')}</div></article>`}).join('')||`<div class=\"card\"><h3>${t('noResults')}</h3></div>`}"""
html=html[:start]+newfunc+html[end:]
# Localize explanation dropdown options.
html=html.replace("${cats.map(c=>`<option value=\"${esc(c)}\">${esc(c)}</option>`).join('')}","${cats.map(c=>`<option value=\"${esc(c)}\">${esc((CAT_UI[lang]||CAT_UI.en)[c]||c)}</option>`).join('')}")
# Replace hardcoded learn/test labels.
html=html.replace("<div class=\"eyebrow\">Vocabulary library</div>","<div class=\"eyebrow\">${t('vocabLibrary')}</div>")
html=html.replace("<p>${data.length} unique learning items.</p>","<p>${data.length} ${t('uniqueItems')}</p>")
html=html.replace("<div class=\"eyebrow\">AI Lab</div><h2>Original English with Filipe tests.</h2><p>Practice grammar, vocabulary, reading, cloze, transformations and functional language.</p>","<div class=\"eyebrow\">${t('aiLab')}</div><h2>${t('testsIntro')}</h2><p>${t('testsDescription')}</p>")
html=html.replace("<p>10 questions with feedback and a final score.</p>","<p>10 ${t('questionDescription')}</p>")
html=html.replace("<div class=\"notice\">Loading...</div>","<div class=\"notice\">${t('loading')}</div>")
html=html.replace("<div class=\"notice\">No students registered yet.</div>","<div class=\"notice\">${t('noStudents')}</div>")
html=html.replace("<div class=\"notice\">Teacher Lab could not load. ${esc(e.message)}</div>","<div class=\"notice\">${t('teacherLoadError')} ${esc(e.message)}</div>")
# Dict level options use localized key.
html=html.replace("${lang==='pt'?'Todos os níveis':lang==='ro'?'Toate nivelurile':'All levels'}", "${lang==='pt'?'Todos os níveis':lang==='ro'?'Toate nivelurile':'All levels'}")
open('/mnt/data/v67fix/web/index.html','w',encoding='utf-8').write(html)
