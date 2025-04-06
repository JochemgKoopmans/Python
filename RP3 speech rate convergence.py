import psychopy
from psychopy import visual, core, event, sound #, microphone
import pandas as pd
import numpy as np
import psychtoolbox as ptb #?

#IN SOUNDLAB: TEST SOUND PRESENTATION AND MICROPHONE FUNCTIONALITIES

## ---------------------------------
##  SETTING UP EXPERIMENT BACKGROUND: VARIABLES, FUNCTIONS, ETC. 
## ---------------------------------

win = visual.Window(size=(800, 600), fullscr=True, allowGUI=True,color=[1,1,1])

continuePrompt = visual.TextStim(win, text = 'Druk op Enter om door te gaan', pos = [0,-.7], height = .05, color=[-1,-1,-1])

freeEntry = visual.TextBox2(win, text=None, letterHeight=0.08, size=0.2, color=[-1,-1,-1], borderWidth=2.0,
    editable=True, borderColor=[.2,.2,.2], autoLog=True, placeholder='')

## Declaring functions
def stringify(list_of_langs):
    if len(list_of_langs) == 0:
        print('Language list empty!')
        return('! see output! ')
    elif len(list_of_langs) == 1:
        return list_of_langs[0]
    elif len(list_of_langs) == 2:
        return list_of_langs[0] + ' en ' + list_of_langs[1]
    else:
        lang_string = ''
        for language in range(len(list_of_langs)-1):
            lang_string += list_of_langs[language] + ', '
        lang_string += 'en ' + list_of_langs[len(list_of_langs)-1]
        return lang_string

def spaceContinues(trialType, dataframe):
    proceed = event.waitKeys(keyList=['space','escape'], timeStamped=expTime)
    ppDataAdd = pd.DataFrame( {
        "trialType": [trialType],
        "timeElapsed": [ proceed[0][1] ]
    } )
    dataframe = dataframe.append( ppDataAdd, ignore_index=True )
    checkEsc('proceed', proceed, dataframe)

def checkEsc(context, variable, df):
    if context == 'proceed' and variable[0][0] == 'escape':
        saveData(pp_file, df)
        win.close()
        core.quit()
    elif context == 'freeEntry':
        keys = event.getKeys(keyList=['escape'])
        if keys and keys[0] == 'escape':
            saveData(pp_file, df)
            win.close()
            core.quit()

def saveData(datafile, passedDF):
    datafile = datafile.append(pp_info, ignore_index=True)
    with pd.ExcelWriter("participant_info.xlsx", mode='a', if_sheet_exists='replace') as writer:
        datafile.to_excel(writer, sheet_name='ppInfo')
        passedDF.to_excel(writer, sheet_name='pp' + str(pp_num))

## Open excel file with subject number, age, gender, etc., and read the latest subject number
pp_file = pd.read_excel(r'participant_info.xlsx',index_col=0)
pp_num = len(pp_file['ppNum']) + 1
pp_info = {
    "ppNum": pp_num,
    "age": -999,
    "gender": '',
    "occupation": '',
    "foreignLanguages": [],
    "scandinavianExp": '',
    "sourceMem": -999,
    "debrief1": '',
    "debrief2": '',
    "debrief3": ''
}

stimuli_file = pd.read_excel(r'stimuli.xlsx')

## Create new dataframe for storing participant data
ppData = pd.DataFrame({
    "trialType": [],
    "timeElapsed": [],
    "word": [],
    "speechVoice": [],
    "speechRate": [],
    "rtSpeech": [],
    "respondedVoice": [],
    "rtVoice": [],
    "voiceCorrect": []
})

expTime = core.MonotonicClock()

## -------------------------------------
##          EXPERIMENT STARTS HERE      
## -------------------------------------

## =========== Introduction ============= #

introText = '''Bedankt voor het meedoen aan dit onderzoek.\n
    Het onderzoek zal uit vijf korte delen bestaan, die samen ongeveer 45 minuten zullen duren.\n\n
    Het eerste gedeelte bestaat uit een paar algemene vragen over jou en jouw ervaring met vreemde talen.\n
    Druk op spatie om door te gaan.''' 

# Show instruction text, wait for spacebar
introWin = visual.TextStim(win, text=introText, color=[-1,-1,-1])
introWin.draw()
win.flip()
spaceContinues('introText',ppData)

## Demographic questions 
demoQ1 = visual.TextStim(win, text=stimuli_file['Demographic questions'][0], pos=[0,.2], color=[-1,-1,-1]) #How old are you (in years)?
while '\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    demoQ1.draw()
    freeEntry.draw()
    continuePrompt.draw()
    win.flip()

ppDataAdd = pd.DataFrame( { "trialType": ['ageQ'], "timeElapsed": [expTime.getTime()] } )
ppData = ppData.append(ppDataAdd, ignore_index=True)

pp_age = freeEntry.text
pp_info["age"] = pp_age.replace('\n','')
freeEntry.clear()

demoQ2 = visual.TextStim(win, text=stimuli_file['Demographic questions'][1], pos=[0,.4], color=[-1,-1,-1]) #With which gender do you identify most?
q2instrText = '(type \'v\' voor vrouw, \'m\' voor man, \'a\' voor anders, en \'x\' als je het liever voor jezelf houdt.)'
q2instr = visual.TextStim(win, text=q2instrText, pos=[0,.2], height=.05, color=[-.7,-.7,-.7])

while '\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    demoQ2.draw()
    q2instr.draw()
    freeEntry.draw()
    continuePrompt.draw()
    win.flip()

ppData = ppData.append(pd.DataFrame({"trialType": ['genderQ'], "timeElapsed": [expTime.getTime()]} ), ignore_index=True )

pp_gender = freeEntry.text
pp_info["gender"] = pp_gender.replace('\n','')
freeEntry.clear()

demoQ3 = visual.TextStim(win, text=stimuli_file['Demographic questions'][2], pos=[0,.4], color=[-1,-1,-1]) #What is your occupation?
freeEntry.placeholder = 'e.g. student'
freeEntry.size = [.4,.15]
while '\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    demoQ3.draw()
    freeEntry.draw()
    continuePrompt.draw()
    win.flip()

ppData = ppData.append(pd.DataFrame({"trialType": ['occupationQ'], "timeElapsed": [expTime.getTime()]} ), ignore_index=True)

pp_occupation = freeEntry.text
pp_info["occupation"] = pp_occupation.replace('\n','')

freeEntry.placeholder = ''
freeEntry.clear()

## Language Background Questionnaire
languages = ['Nederlands']
foreignLanguages = []

while True:
    languages_text = stringify(languages)
    lbq1q = stimuli_file['Language background questions'][0].replace('%LANGUAGE%',languages_text) #Do you speak other languages, apart from [languages already listed]?
    lbq1 = visual.TextStim(win, text=lbq1q, pos=[0,.4], color=[-1,-1,-1])
    lbq1instrText = '(antwoord met een taal die je nog meer spreekt of \'nee\' als je ze allemaal hebt ingevoerd)'
    lbq1instr = visual.TextStim(win, text=lbq1instrText, pos=[0,.2], height=.05, color=[-.7,-.7,-.7])
    freeEntry.clear()
    while '\n' not in freeEntry.text:
        checkEsc('freeEntry',freeEntry,ppData)
        lbq1.draw()
        lbq1instr.draw()
        freeEntry.draw()
        continuePrompt.draw()
        win.flip()
    
    if (freeEntry.text == 'nee\n' or freeEntry.text == 'Nee\n' or freeEntry.text == '\n'):
        freeEntry.clear()
        break
    else:
        newLanguage = freeEntry.text
        foreignLanguages.append( [newLanguage.replace('\n','')] )
        languages.append(newLanguage.replace('\n','') )
        freeEntry.clear()
    
    lbq2q = stimuli_file['Language background questions'][1].replace('%LANGUAGE%',languages[len(languages)-1]) #How well do you speak [latest language entered]?
    lbq2 = visual.TextStim(win, text=lbq2q, pos=[0,.3], color=[-1,-1,-1])
    
    while '\n' not in freeEntry.text:
        checkEsc('freeEntry',freeEntry,ppData)
        lbq2.draw()
        freeEntry.draw()
        continuePrompt.draw()
        win.flip()
    
    proficiency = freeEntry.text
    foreignLanguages[len(foreignLanguages)-1].append(proficiency.replace('\n',''))
    freeEntry.clear()
    
    lbq3q = stimuli_file['Language background questions'][2].replace('%LANGUAGE%',languages[len(languages)-1]) #How often do you use [latest language entered]?
    lbq3 = visual.TextStim(win, text=lbq3q, pos=[0,.3], color=[-1,-1,-1])
    
    while '\n' not in freeEntry.text:
        checkEsc('freeEntry',freeEntry,ppData)
        lbq3.draw()
        freeEntry.draw()
        continuePrompt.draw()
        win.flip()
    
    langUse = freeEntry.text
    foreignLanguages[len(foreignLanguages)-1].append(langUse.replace('\n',''))

ppData = ppData.append( pd.DataFrame( { "trialType": ['foreignLanguages'], "timeElapsed": [expTime.getTime()] } ), ignore_index=True)
pp_info["foreignLanguages"] = foreignLanguages

## Scandinavian languages question
freeEntry.size = .75
freeEntry.pos = (0,-.1)

scandQuestion = 'Beschrijf kort je ervaring met Scandinavische talen tot nu toe:\n(Druk tweemaal op enter om door te gaan)'
scandQ = visual.TextStim(win, text=scandQuestion, pos=[0,.5], color=[-1,-1,-1])
while '\n\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    scandQ.draw()
    freeEntry.draw()
    #continuePrompt.draw()
    win.flip()

expScandQ = freeEntry.text
ppData = ppData.append( pd.DataFrame( { "trialType": ['scandinavianExperience'], "timeElapsed": [expTime.getTime()] } ), ignore_index=True)
pp_info["scandinavianExp"] = expScandQ.replace('\n\n','')

freeEntry.size = .2
freeEntry.clear()

## =========== COGNATE WORD LEARNING PHASE =============== ##

learnInstructions = '''Deel 2 van 5: Zweedse woorden leren\n
    Je ziet en hoort zometeen twintig Zweedse woorden. Probeer ze zo goed mogelijk te onthouden, je wordt er later op getest. Als ze allemaal zijn geweest, worden ze allemaal nog eens herhaald.\n
    Alle woorden worden dus twee keer gepresenteerd.\n
    Druk op spatie om door te gaan en het eerste woord te zien en horen.'''

learnInstr = visual.TextStim(win, text=learnInstructions, pos=[0,.2], color=[-1,-1,-1])

learnInstr.draw()
win.flip()
spaceContinues('learnInstructions',ppData)

## Cognate word display
for repeat in range(2):
    colNameSw = 'Learn words Sw' + str(repeat+1)
    colNameEn = 'Learn words En' + str(repeat+1)
    for trial in range(len(stimuli_file[colNameSw])):
        if type(stimuli_file[colNameSw][trial]) is float: #Takes care of PsychoPy reading empty cells
            continue
        word = stimuli_file[colNameSw][trial]
        img = stimuli_file[colNameEn][trial]
        visual.ImageStim(win, image='images/' + img + '.jpg').draw()
        visual.TextStim(win, text=word, pos=[0,.7], color=[-1,-1,-1]).draw()
        #cognateWord = Sound('sounds/' + word + '_F.wav')
        win.flip()
        core.wait(.5)
        #cognateWord.play()
        #something to hold further execution until sound is finished; e.g. while cognateWord.isFinished: pass
        visual.ImageStim(win, image='images/' + img + '.jpg').draw()
        visual.TextStim(win, text=word, pos=[0,.7], color=[-1,-1,-1]).draw()
        continuePrompt.draw()
        win.flip()
        nextTrial = event.waitKeys(keyList=['return','escape'], timeStamped=expTime)
        checkEsc('proceed',nextTrial,ppData)
    if repeat == 0:
        endBlockText = '''Dat waren alle woorden die je moet onthouden. Ze worden allemaal een keer herhaald zodra je op spatie drukt'''
        visual.TextStim(win, text=endBlockText, pos=[0,.1], color=[-1,-1,-1]).draw()
        win.flip()
        spaceContinues('firstWordPresentation',ppData)

## Cognate memory and production trial
repeatInstructions = '''Je hebt nu alle woorden tweemaal gezien en gehoord.\n
    De plaatjes worden nu één voor één weer laten zien.\n
    Zodra de microfoon verschijnt is het aan jou om het Zweedse woord ervoor uit te spreken.\n
    Daarna word je gevraagd of je de stem kunt herinneren die het woord twee keer voor jou heeft uitgesproken.\n
    Druk op spatie om met het eerste woord te starten.'''
visual.TextStim(win, text=repeatInstructions, pos=[0,.2], color=[-1,-1,-1]).draw()
win.flip()
spaceContinues('repeatCognateInstructions',ppData)

    ## Cognate memory + pronunciation
trialTimer = core.Clock()
for trial in range(len(stimuli_file['Retrieve word'])):
    if type(stimuli_file['Retrieve word'][trial]) is float: #Takes care of PsychoPy reading empty cells
        continue
    
    imgName = stimuli_file['Retrieve word'][trial]
    repTrial = {
        "word": imgName,
        "speechVoice": stimuli_file['Retrieve voice'][trial],
        "speechRate": stimuli_file['Retrieve speed'][trial]
    }
    
    visual.ImageStim(win, image='images/' + imgName + '.jpg').draw()
    continuePrompt.draw()
    win.flip()
    trialTimer.reset()
    
    #start microphone
    endRecording = event.waitKeys(keyList=['return','escape'], timeStamped=trialTimer)
    repTrial["rtSpeech"] = endRecording[0][1]
    checkEsc('proceed',endRecording,ppData)
    #close microphone, save recording
    
    ## Source memory question
    voiceText = 'Weet je nog of dit woord door een man of vrouw werd uitgesproken?\nDruk op \'m\' voor man en \'v\' voor vrouw.\nAls je het niet meer weet mag je gokken.'
    visual.TextStim(win, text=voiceText, pos=[0,0], color=[-1,-1,-1]).draw()
    win.flip()
    
    ppAns = event.waitKeys(keyList=['m','v','escape'], timeStamped=trialTimer)
    repTrial["respondedVoice"] = ppAns[0][0]
    repTrial["rtVoice"] = ppAns[0][1]
    if (stimuli_file['voice'][trial] == 'M' and ppAns[0][0] == 'm'):
        repTrial["voiceCorrect"] = 1
    elif (stimuli_file['voice'][trial] == 'F' and ppAns[0][0] == 'v'):
        repTrial["voiceCorrect"] = 1
    else:
        repTrial["voiceCorrect"] = 0
    #Add answer to participant data file
    repTrial["trialType"] = 'repeatCognate'
    repTrial["timeElapsed"] = expTime.getTime()
    ppData = ppData.append(repTrial, ignore_index=True)
    checkEsc('proceed',ppAns,ppData)
    win.flip() #shows a white screen: intertrial interval
    core.wait(.2)

pp_info["sourceMem"] = sum(ppData["voiceCorrect"][3:])

## ========= NON-COGNATE PRODUCTION ========= ##

productionInstructions = '''Deel 3 van 5: Uitspreken van nieuwe Zweedse woorden\n
    Je ziet zometeen tien keer een Zweeds woord en een illustratie ervan. Zodra de microfoon verschijnt, spreek dan het woord in het Zweeds uit.\n
    Nadat je het woord hebt uitgesproken ga je naar de volgende woord door op Enter te drukken.\n
    Druk op Spatie om dit deel te beginnen.'''

prodInstr = visual.TextStim(win, text=productionInstructions, pos=[0,.1], color=[-1,-1,-1])
prodInstr.draw()
win.flip()
spaceContinues('pronunciationInstructions',ppData)

for trial in range(len(stimuli_file['Pronunciation words'])):
    if type(stimuli_file['Pronunciation words'][trial]) is float: #Takes care of PsychoPy reading empty cells
        continue
    
    imgName = stimuli_file['Pronunciation words En'][trial]
    prodTrial = {
        "word": imgName,
        "trialType": 'produceNonCognate'
    }
    
    nonCognateWord = stimuli_file['Pronunciation words'][trial]
    nonCognateImg = visual.ImageStim(win, image='images/' + imgName + '.jpg', pos=(.3,0))
    nonCognateImg.draw()
    visual.ImageStim(win, image='loudspeaker.png', pos=(-.3,0)).draw()
    #nonCognateSound = Sound('sounds/noncognate/' + nonCognateWord + '.wav')
    #ADD IMAGE OF LOUDSPEAKER/MOUTH WHEN SOUND IS PLAYING CQ WE WANT PP TO PRONOUNCE
    win.flip()
    #nonCognateSound.play()
    core.wait(.2)
    nonCognateImg.draw()
    visual.ImageStim(win, image='mic.png', pos=(-.3,0)).draw()
    continuePrompt.draw()
    win.flip()
    trialTimer.reset()
    #start microphone
    nextTrial = event.waitKeys(keyList=['return', 'escape'], timeStamped=trialTimer)
    #close microphone, save recording
    prodTrial["rtSpeech"] = nextTrial[0][1]
    prodTrial["timeElapsed"] = expTime.getTime()
    if nextTrial[0][0] == 'escape':
        prodTrial["respondedVoice"] = 'escape'
    ppData = ppData.append(prodTrial, ignore_index=True)
    checkEsc('proceed',nextTrial,ppData)

## Debriefing experiment
debrief1 = visual.TextStim(win, text=stimuli_file['Debrief questions'][0], pos=[0,.4], color=[-1,-1,-1]) #Did you notice anything?
freeEntry.size = .75
freeEntry.pos = (0,-.1)
freeEntry.clear()
while '\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    debrief1.draw()
    freeEntry.draw()
    continuePrompt.draw()
    win.flip()
ppDataAdd = pd.DataFrame( { "trialType": ['debrief1'], "timeElapsed": [expTime.getTime()] } )
ppData = ppData.append(ppDataAdd, ignore_index=True)
print('debrief 1 ans: ' + freeEntry.text)
pp_debrief1 = freeEntry.text
pp_info["debrief1"] = pp_debrief1.replace('\n','')
freeEntry.clear()

debrief2 = visual.TextStim(win, text=stimuli_file['Debrief questions'][1], pos=[0,.4], color=[-1,-1,-1]) #Did you notice anything?
freeEntry.clear()
while '\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    debrief2.draw()
    freeEntry.draw()
    continuePrompt.draw()
    win.flip()
print('debrief 2 ans: ' + freeEntry.text)
ppDataAdd = pd.DataFrame( { "trialType": ['debrief2'], "timeElapsed": [expTime.getTime()] } )
ppData = ppData.append(ppDataAdd, ignore_index=True)

pp_debrief2 = freeEntry.text
pp_info["debrief2"] = pp_debrief2.replace('\n','')
freeEntry.clear()

debrief3 = visual.TextStim(win, text=stimuli_file['Debrief questions'][2], pos=[0,.4], color=[-1,-1,-1]) #Did you notice anything?
while '\n' not in freeEntry.text:
    checkEsc('freeEntry',freeEntry,ppData)
    debrief3.draw()
    freeEntry.draw()
    continuePrompt.draw()
    win.flip()
print('debrief 3 ans: ' + freeEntry.text)
ppDataAdd = pd.DataFrame( { "trialType": ['debrief3'], "timeElapsed": [expTime.getTime()] } )
ppData = ppData.append(ppDataAdd, ignore_index=True)

pp_debrief3 = freeEntry.text
pp_info["debrief3"] = pp_debrief3.replace('\n','')
freeEntry.clear()

## End exp

saveData(pp_file,ppData)

thanks = 'Einde deel 3\n\nDruk op een toets om dit gedeelte af te sluiten. De onderzoeker zal de laatste twee taakjes opstarten.'
visual.TextStim(win,text=thanks, pos=[0,0], color=[-1,-1,-1]).draw()
win.flip()
event.waitKeys(maxWait=20)