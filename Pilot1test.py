# 1. Creating the grid and a list of letters from which it can be filled
    # 1.1 Creating a window that letters can be displayed
from psychopy import visual, core, event
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")

    # 1.2 Creating a list of letters that can be presented
from random import * # makes sure a random selection can be made later on
possible_letters = 'QERTYUOPSDFGKLCBN'
rotatable_letters = 'RYGKCB'
"""print(len(possible_letters))
print(len(rotatable_letters))"""

    # 1.3 Setting up twelve letters with fixed locations
        # Letters need a location, an identity (the random letter that is chosen) and rotation value
letter1 = visual.TextStim(mywin, pos=(-3.0,2.0)) # locations top left-to-right, middle LTR, bottom LTR
letter2 = visual.TextStim(mywin, pos=(-1.0,2.0))
letter3 = visual.TextStim(mywin, pos=(1.0,2.0))
letter4 = visual.TextStim(mywin, pos=(3.0,2.0))
letter5 = visual.TextStim(mywin, pos=(-3.0,0.0))
letter6 = visual.TextStim(mywin, pos=(-1.0,0.0))
letter7 = visual.TextStim(mywin, pos=(1.0,0.0))
letter8 = visual.TextStim(mywin, pos=(3.0,0.0))
letter9 = visual.TextStim(mywin, pos=(-3.0,-2.0))
letter10 = visual.TextStim(mywin, pos=(-1.0,-2.0))
letter11 = visual.TextStim(mywin, pos=(1.0,-2.0))
letter12 = visual.TextStim(mywin, pos=(3.0,-2.0))
trial_letters = [letter1, letter2, letter3, letter4, letter5, letter6, letter7, letter8, letter9, letter10, letter11, letter12]
        # If drawing the letters (i.e. during the trial) takes long, resetting the texts by: myTextStim.text=myTextStim.text after changing the parameters, should make the drawing faster

    # 1.4 Creating a target circle
target_circle = visual.Circle(mywin,lineWidth=8,lineColor='red',size=3)

    #1.5 Creating an answer box
        # Should contain user letter entry (any of the possible letters), spacebar entry to rotate letter, backspace to enter a new letter, arrow input for certainty judgment, enter to proceed
        # Creates six squares that answer options (letters) will appear in 
trial_q = visual.TextStim(mywin, pos=(0,4), text='Please click on the cued letter')
ans_loc_1 = visual.ShapeStim(mywin, lineColor='white', vertices=((-4,2.5),(-2,2.5),(-2,.5),(-4,.5))) # vertice order top-left top-right bottom-right bottom-left
ans_loc_2 = visual.ShapeStim(mywin, lineColor='white', vertices=((-1,2.5),(1,2.5),(1,.5),(-1,.5))) # loc top left-to-right, bottom left-to-right
ans_loc_3 = visual.ShapeStim(mywin, lineColor='white', vertices=((2,2.5),(4,2.5),(4,.5),(2,.5)))
ans_loc_4 = visual.ShapeStim(mywin, lineColor='white', vertices=((-4,-.5),(-2,-.5),(-2,-2.5),(-4,-2.5)))
ans_loc_5 = visual.ShapeStim(mywin, lineColor='white', vertices=((-1,-.5),(1,-.5),(1,-2.5),(-1,-2.5)))
ans_loc_6 = visual.ShapeStim(mywin, lineColor='white', vertices=((2,-.5),(4,-.5),(4,-2.5),(2,-2.5)))

#I need only a list of possible locations, which is to be randomised and then added to the answer options
ans_locations = [(-3,1.5),(0,1.5),(3,1.5),(-3,-1.5),(0,-1.5),(3,-1.5)]
# I will need these because otherwise the trial letters get updated when they are also an answer option
ans_1 = visual.TextStim(mywin, pos=(-3,1.5), text='1', ori=0) # These positions and text should be updated later)
ans_2 = visual.TextStim(mywin, pos=(0,1.5), text='2', ori=0) # idem
ans_3 = visual.TextStim(mywin, pos=(3,1.5), text='3', ori=0) # idem
ans_4 = visual.TextStim(mywin, pos=(-3,-1.5), text='4', ori=0) # idem
ans_5 = visual.TextStim(mywin, pos=(0,-1.5), text='5', ori=0) # idem
ans_6 = visual.TextStim(mywin, pos=(3,-1.5), text='6', ori=0) # idem

        # Creates confidence rating question and answer options
conf_question = visual.TextStim(mywin, pos=(0,-4), text='How confident are you of your answer? 1=not, 4=very', height=.6, wrapWidth=12)

conf_1 = visual.ShapeStim(mywin, vertices=((-2,-5),(-3.25,-5),(-3.25,-6.25),(-2,-6.25)))
conf_2 = visual.ShapeStim(mywin, vertices=((-.25,-5),(-1.5,-5),(-1.5,-6.25),(-.25,-6.25)))
conf_3 = visual.ShapeStim(mywin, vertices=((.25,-5),(1.5,-5),(1.5,-6.25),(.25,-6.25)))
conf_4 = visual.ShapeStim(mywin, vertices=((2,-5),(3.25,-5),(3.25,-6.25),(2,-6.25)))

conf_int_1 = visual.TextStim(mywin, pos=(-2.675,-5.625), text='1', height=.6)
conf_int_2 = visual.TextStim(mywin, pos=(-.875,-5.625), text='2', height=.6)
conf_int_3 = visual.TextStim(mywin, pos=(.875,-5.625), text='3', height=.6)
conf_int_4 = visual.TextStim(mywin, pos=(2.675,-5.625), text='4', height=.6)

# 2 Trial generation
    # 2.1 Creating a list of letters to be used in the trial
letter_list = sample(list(possible_letters),k=12) # returns a list of 12 randomly chosen letters (without replacement) from the possible letters
# Note that currently there are 17 possible letters, 6 rotatable letters and 12 letter positions. This means that necessarily at least one of the letter list must be a rotatable letter
count = 0
for letter in trial_letters:
    letter.text = letter_list[count]
    count += 1
    # 2.2 Rotating one of the letters
rotatable_letter_list = []
for letter in letter_list:
    if letter in rotatable_letters:
        rotatable_letter_list.append(letter)

rotating_letter = sample(rotatable_letter_list, k=1)
rotated_letter = []
for letter in trial_letters:
    if letter.text == rotating_letter[0]:
        letter.ori = 180
        rotated_letter.append(letter)   # This is needed later for determining answer options
print('rotated letter is ' + str(rotated_letter[0].text))   # test

    #2.3 Quasi-randomly choosing one of the letters to be the target and updating target circle coordinates
target_letter = ''
holding_list = []
chosen_letter = []
if random() <.50: # there is a [value]% chance that the rotated letter is chosen (returns a float between 0.0 and 1.0)
    for letter in trial_letters:
        if letter.ori == 180:
            chosen_letter.append(letter)
    target_letter = chosen_letter[0].text
    target_circle.pos = chosen_letter[0].pos
else:
    for letter in trial_letters:
        if letter.ori == 0.0:
            holding_list.append(letter)
    chosen_letter = sample(holding_list, k=1)
    target_letter = chosen_letter[0].text
    target_circle.pos = chosen_letter[0].pos

    #2.4 Determining letter presentation order. 
order = []
duplicate_list = []
for x in trial_letters:
    duplicate_list.append(x)
duplicate_list.remove(chosen_letter[0])
order += sample(duplicate_list, k=9)
for letter in order:
    duplicate_list.remove(letter)
duplicate_list.append(chosen_letter[0])
order += sample(duplicate_list, k=3)

    #2.5 Adding response option
        # 1 = chosen letter 2 = display distractor 3 = display distractor 4 = display distractor_rotated 5 = not in display 6 = not in display OR already rotated letter
        # First collect all the letters and their orientations
        # FOR NORMAL TRIALS ADD NORMAL ROTATION AS WELL
ans_1.text = chosen_letter[0].text
ans_1.ori = chosen_letter[0].ori
print('The chosen letter/ ans_1: ' + ans_1.text + str(ans_1.ori))   # test

copy_list = []
for x in trial_letters:
    copy_list.append(x)
copy_list.remove(chosen_letter[0])
if chosen_letter[0].ori == 0:
    copy_list.remove(rotated_letter[0])
print('The chosen letter plus its orientation:')    #test
print(chosen_letter[0].text + ' ' + str(chosen_letter[0].ori))
print('Letters and rotations in copy_list: (should be 11 if chosen letter is 180, 10 if it is not)')
print(len(copy_list))
for x in copy_list:
    print(x.text + str(x.ori))  # Test to see that the correct letters have been removed
answer_options_hold = []
answer_options_hold += sample(copy_list, k=3)
ans_2.text = answer_options_hold[0].text
ans_2.ori = answer_options_hold[0].ori
print('Ans_2: ' + ans_2.text + str(ans_2.ori))  # test

ans_3.text = answer_options_hold[1].text
ans_3.ori = answer_options_hold[1].ori
print('Ans_3: ' + ans_3.text + str(ans_3.ori))  #test

ans_4.text = answer_options_hold[2].text
ans_4.ori = 180
print('Ans_4: ' + ans_4.text + str(ans_4.ori))  #test

copy_possible_letters = []
for x in possible_letters:
    copy_possible_letters.append(x)
for x in letter_list:
    copy_possible_letters.remove(x)
ans_5.text = choice(copy_possible_letters)
ans_5.ori = 0
print('Ans_5: ' + ans_5.text + str(ans_5.ori))  #Test
print('The trial letters are: ' + str(letter_list)) #Test
print('The unused letters are: ' + str(copy_possible_letters))

if chosen_letter[0].ori == 180:
    copy_possible_letters.remove(ans_5.text)
    print('Chosen letter ori =180, so unused should be one less')   #test
    print('unused letters: ' + str(len(copy_possible_letters)) + str(copy_possible_letters))
    ans_6.text = choice(copy_possible_letters)
    ans_6.ori = 0
    print('Ans_6: ' + ans_6.text + str(ans_6.ori))  #test
elif chosen_letter[0].ori == 0:
    ans_6.text = rotated_letter[0].text
    ans_6.ori = rotated_letter[0].ori
    print('Chosen letter ori =0; Ans_6: ' + ans_6.text + str(ans_6.ori))    #test

        # Next make them the answer options
copy_ans_locations = []
for x in ans_locations:
    copy_ans_locations.append(x)
shuffle(copy_ans_locations)
print('Ans locations shuffled: ' + str(copy_ans_locations)) #test
ans_1.pos = copy_ans_locations[0]
ans_2.pos = copy_ans_locations[1]
ans_3.pos = copy_ans_locations[2]
ans_4.pos = copy_ans_locations[3]
ans_5.pos = copy_ans_locations[4]
ans_6.pos = copy_ans_locations[5]
answer_options = [ans_1, ans_2, ans_3, ans_4, ans_5, ans_6]

    # Now let us connect answer boxes to answers, to make our life easier later on
ansbox1_ans = []
ansbox2_ans = []
ansbox3_ans = []
ansbox4_ans = []
ansbox5_ans = []
ansbox6_ans = []
for x in answer_options:    #ans_locations = [(-3,1.5),(0,1.5),(3,1.5),(-3,-1.5),(0,-1.5),(3,-1.5)]
    if all(x.pos == (-3,1.5)):
        ansbox1_ans.append(x)       # DO NOT CHANGE ANYTHING IN THE ANSBOXes! They are identical with the answer options, so changing them will change the answer options too
    elif all(x.pos == (0,1.5)):
        ansbox2_ans.append(x)
    elif all(x.pos == (3,1.5)):
        ansbox3_ans.append(x)
    elif all(x.pos == (-3,-1.5)):
        ansbox4_ans.append(x)
    elif all(x.pos == (0,-1.5)):
        ansbox5_ans.append(x)
    elif all(x.pos == (3,-1.5)):
        ansbox6_ans.append(x)
print('Ans locations: ' + str(ans_1.pos) + ' ' + str(ans_2.pos) + ' ' + str(ans_3.pos) + ' ' + str(ans_4.pos) + ' ' + str(ans_5.pos) + ' ' + str(ans_6.pos))
print('Ans boxes: ' + str(ansbox1_ans) + ' ' + str(ansbox2_ans) + ' ' + str(ansbox3_ans) + ' ' + str(ansbox4_ans) + ' ' + str(ansbox5_ans) + ' ' + str(ansbox6_ans))
print('test ansbox connections: ansbox1 - ' + str(ansbox1_ans[0].pos) + ', ansbox2 - ' + str(ansbox2_ans[0].pos) + ', ansbox3 - ' + str(ansbox3_ans[0].pos) + ', ansbox4 - ' + str(ansbox4_ans[0].pos) + ', ansbox5 - ' + str(ansbox5_ans[0].pos) + ', ansbox6 - ' + str(ansbox6_ans[0].pos)) #test 
        # Then create the mouse and record two clicks. Compare chosen answer option with answer options (4 types).
cursor = event.Mouse(mywin)
# Figure out how to get the answer type from the class instance.
    
            # If mouse clicks on answer options: answer variables should reset, new value should be chosen. Also, answer box and letter should become red
given_answer = visual.TextStim(mywin) #is what the subject thinks it was, extract .text and .ori
answer_type = ''    # Is what the answer type was (correct, distractor, distractor_rot, not-in-display)
"""
if mouse.isPressedIn(ans_loc_1):
    for x in answer_options:    #ans_locations = [(-3,1.5),(0,1.5),(3,1.5),(-3,-1.5),(0,-1.5),(3,-1.5)]
"""
            # If mouse clicks on certainty box: answer should reset, new value should be chosen. Also, certainty and value should become red
            
        # Then move on to the next trial (assuming it saved the clicks)
            # Wait with the screen updating (see psychopy mywin)
        
# From here on, things are printed and drawn on the window

print('Target letter is: ' + target_letter) # to check that the circled one is correct
#target_circle.draw() # this is to know which letter to look for
mywin.update()
core.wait(.3)
for x in range(12):
    order[x].draw() # the order contains all 12 TextStim instances (letters) in a ready order
    mywin.update()
    core.wait(.05) # this is the presentation time
target_circle.draw()
mywin.update()
core.wait(3)
"""
"""
trial_q.draw()
ans_loc_1.draw()
ans_loc_2.draw()
ans_loc_3.draw()
ans_loc_4.draw()
ans_loc_5.draw()
ans_loc_6.draw()
ans_1.draw()
ans_2.draw()
ans_3.draw()
ans_4.draw()
ans_5.draw()
ans_6.draw()
conf_question.draw()
conf_1.draw()
conf_2.draw()
conf_3.draw()
conf_4.draw()
conf_int_1.draw()
conf_int_2.draw()
conf_int_3.draw()
conf_int_4.draw()
mywin.update()
core.wait(4)
