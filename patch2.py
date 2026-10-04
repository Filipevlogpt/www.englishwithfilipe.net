p='/mnt/data/v67fix/web/index.html'
s=open(p,encoding='utf8').read()
# append UI keys before footer for each language
repls=[
("teacherLoadError:'Teacher Lab could not load.',footer:","teacherLoadError:'Teacher Lab could not load.',example:'Example',normal:'Normal',slow:'Slow',typeLabel:'Type',topicLabel:'Topic',dailyUse:'daily use',testsWord:'tests',loadingDiagnosis:'Loading diagnosis...',individualDiagnosis:'Individual diagnosis based on incorrect answers.',errors:'errors',noMistakes:'No mistakes recorded yet.',testHistory:'Test history',noCompletedTests:'No completed tests.',diagnosisError:'The diagnosis could not be opened.',footer:"),
("teacherLoadError:'A Área do Professor não pôde ser carregada.',footer:","teacherLoadError:'A Área do Professor não pôde ser carregada.',example:'Exemplo',normal:'Normal',slow:'Lento',typeLabel:'Tipo',topicLabel:'Tema',dailyUse:'uso diário',testsWord:'testes',loadingDiagnosis:'Carregando diagnóstico...',individualDiagnosis:'Diagnóstico individual baseado nas respostas incorretas.',errors:'erros',noMistakes:'Nenhum erro registrado ainda.',testHistory:'Histórico de testes',noCompletedTests:'Nenhum teste concluído.',diagnosisError:'Não foi possível abrir o diagnóstico.',footer:"),
("teacherLoadError:'Zona profesorului nu a putut fi încărcată.',footer:","teacherLoadError:'Zona profesorului nu a putut fi încărcată.',example:'Exemplu',normal:'Normal',slow:'Lent',typeLabel:'Tip',topicLabel:'Temă',dailyUse:'utilizare zilnică',testsWord:'teste',loadingDiagnosis:'Se încarcă diagnosticul...',individualDiagnosis:'Diagnostic individual bazat pe răspunsurile incorecte.',errors:'erori',noMistakes:'Nu există încă greșeli înregistrate.',testHistory:'Istoricul testelor',noCompletedTests:'Nu există teste finalizate.',diagnosisError:'Diagnosticul nu a putut fi deschis.',footer:")]
for a,b in repls:
 if a not in s: print('missing',a[:40])
 s=s.replace(a,b)
# Home test count
s=s.replace("${tests.filter(z=>z.level===l).length} tests","${tests.filter(z=>z.level===l).length} ${t('testsWord')}")
# Vocab cards
s=s.replace("<div class=\"example\"><strong>Example</strong>","<div class=\"example\"><strong>${t('example')}</strong>")
s=s.replace("<button class=\"audio-btn\" onclick=\"playAudio('/${x.audio.normal}',this)\">▶ Normal</button><button class=\"audio-btn\" onclick=\"playAudio('/${x.audio.slow}',this)\">🐢 Slow</button>","<button class=\"audio-btn\" onclick=\"playAudio('/${x.audio.normal}',this)\">▶ ${t('normal')}</button><button class=\"audio-btn\" onclick=\"playAudio('/${x.audio.slow}',this)\">${t('slow')}</button>")
s=s.replace("<span>${esc(x.type)}</span><span>${esc(x.topic)}</span>","<span>${t('typeLabel')}: ${esc(x.type)}</span><span>${t('topicLabel')}: ${esc(x.topic)}</span>")
# Dict fallback labels
s=s.replace("${esc(x.type||'vocabulary')} · ${esc(x.topic||'daily use')}","${esc(x.type||t('vocab'))} · ${esc(x.topic||t('dailyUse'))}")
# Teacher diagnosis hardcoded strings
s=s.replace("box.innerHTML='<div class=\"notice\">Loading diagnosis...</div>'","box.innerHTML=`<div class=\"notice\">${t('loadingDiagnosis')}</div>`")
s=s.replace("<p style=\"color:#c9ddd6\">Individual diagnosis based on incorrect answers.</p>","<p style=\"color:#c9ddd6\">${t('individualDiagnosis')}</p>")
s=s.replace("${x.count} errors","${x.count} ${t('errors')}")
s=s.replace("<div class=\"diag\">No mistakes recorded yet.</div>","<div class=\"diag\">${t('noMistakes')}</div>")
s=s.replace("<h3 style=\"font-family:Nunito;color:#fff\">Test history</h3>","<h3 style=\"font-family:Nunito;color:#fff\">${t('testHistory')}</h3>")
s=s.replace("<div class=\"diag\">No completed tests.</div>","<div class=\"diag\">${t('noCompletedTests')}</div>")
s=s.replace("<div class=\"notice\">The diagnosis could not be opened. ${esc(e.message)}</div>","<div class=\"notice\">${t('diagnosisError')} ${esc(e.message)}</div>")
# Explain search placeholders via helper
s=s.replace("function renderExplain(){activeView='explain';", "function explainSearchPlaceholder(){return lang==='pt'?'Pesquise verbo, adjetivo, substantivo ou gramática...':lang==='ro'?'Caută verb, adjectiv, substantiv sau gramatică...':'Search verb, adjective, noun or grammar...'}\nfunction renderExplain(){activeView='explain';")
s=s.replace("placeholder=\"${lang==='pt'?'Pesquisar verb, adjective, noun, grammar...':lang==='ro'?'Caută verb, adjectiv, substantiv, gramatică...':'Search verb, adjective, noun, grammar...'}\",", "placeholder=\"${explainSearchPlaceholder()}\",")
open(p,'w',encoding='utf8').write(s)
