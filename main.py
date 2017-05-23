# consider using an accordian for the line and controller setup, also allows other draw options
#  in limited space


# create a grid of buttons which if pressed will inform the paint class where to paint the symbol on the canvas
# but the symbol type (AC masked/unmasked) will be based on input from other buttons
# ill need 250,500,750,1000,2000,3000,4000,6000,8000 (9 buttons) by
# (-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110) (25 buttons)

from itertools import izip as zip

# create an audiogram widget with 9 frequency children [propery] each frequency child to have 25 buttons [property]
# from PIL import Image
# create an audiogram widget with 9 frequency children [propery] each frequency child to have 25 buttons [property]
# from PIL import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.widget import Widget

get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]


Window.clearcolor = (1, 1, 1, 1)



def reCodeStringToButton(currentSymbol):
    index = 'RAC'
    value = [0, 0]

    if currentSymbol[0] == 'ra':
        index = 'RAC'
    elif currentSymbol[0] == 'rb':
        index = 'RBC'
    elif currentSymbol[4] == 'la':
        index = 'LAC'
    elif currentSymbol[4] == 'lb':
        index = 'LBC'

    if currentSymbol[0][0] == 'r':
        if currentSymbol[1] == '-' and currentSymbol[2] == '--':  # threshold
            value = [1, currentSymbol[3]]
        elif currentSymbol[1] == 'm' and currentSymbol[2] == '--':  # maskedthreshold
            value = [2, currentSymbol[3]]
        elif currentSymbol[1] == '-' and currentSymbol[2] == 'nr':  # nrthreshold
            value = [3, currentSymbol[3]]
        elif currentSymbol[1] == 'm' and currentSymbol[2] == 'nr':  # nrmaskedthreshold
            value = [4, currentSymbol[3]]

    else:
        if currentSymbol[5] == '-' and currentSymbol[6] == '--':  # threshold
            value = [1, currentSymbol[7]]
        elif currentSymbol[5] == 'm' and currentSymbol[6] == '--':  # maskedthreshold
            value = [2, currentSymbol[7]]
        elif currentSymbol[5] == '-' and currentSymbol[6] == 'nr':  # nrthreshold
            value = [3, currentSymbol[7]]
        elif currentSymbol[5] == 'm' and currentSymbol[6] == 'nr':  # nrmaskedthreshold
            value = [4, currentSymbol[7]]

    output = [index, value]

    return output


def ButtonDictToString(value):
    '''reads input (ButtonDict) and returns a list of strings in the format:
     [[rightBCcode], [centreACcode], [leftBCcode]]
    '''

    # output base

    string_dict = {}

    start_key = {'RAC': 'ra', 'LAC': 'la', 'RBC': 'rb', 'LBC': 'lb'}
    symbol_key = {0: '---', 1: '---', 2: 'm--', 3: '-nr', 4: 'mnr'}

    for key in value:
        # determine if value is 0 and then put '--' in string
        if value[key][0] == 0:
            string_dict[key] = '--' + symbol_key[value[key][0]]
        else:
            string_dict[key] = start_key[key] + symbol_key[value[key][0]]

    RBCcode = string_dict['RBC'] + str(value['RBC'][1]) + '-----0'
    LBCcode = '-----0' + string_dict['LBC'] + str(value['LBC'][1])
    ACcode = string_dict['RAC'] + str(value['RAC'][1]) + string_dict['LAC'] + str(value['LAC'][1])

    return [RBCcode, ACcode, LBCcode]


# buttons create
class AudioButton(Button):
    level = NumericProperty(0)
    bLev = ObjectProperty(None)
    airconduction = ObjectProperty(None)
    rightboneconduction = ObjectProperty(None)
    leftboneconduction = ObjectProperty(None)
    mipmap = True
    # ctex = ObjectProperty(None)
    # ltex = ObjectProperty(None)
    # rtex = ObjectProperty(None)

    # dictionary that stores contents, numeric values = [0-empty, 1-threshold, 2-maskedthreshold 3-threshnoresp, 4maskenoresp],[ 0-no note,1-note1, 2-note2, 3-note3]]
    contents = DictProperty({'LAC': [0, 0], 'RAC': [0, 0], 'LBC': [0, 0], 'RBC': [0, 0]})

    # create a method that on click reports position of button, gives level, gets frequencycolumn label
    def changeImage(self):
        currentSymbol = App.get_running_app().controllerOutput
        print currentSymbol

        # adds the symbol to the Button dictProperty "contents"
        # print reCodeStringToButton(currentSymbol)
        new_content_list = reCodeStringToButton(currentSymbol)
        print 'this is the content list: '
        print new_content_list
        self.contents[new_content_list[0]] = new_content_list[1]

        # decode contents
        symbolList = ButtonDictToString(self.contents)
        print 'this is the symbolList: '
        print symbolList

        self.airconduction.source = 'Images/' + symbolList[1] + '.png'

        # only do BC for BC frequencies alternatively could have a second method for intermediate freq
        if self.parent.parent.frequencyLabel in ['125', '250', '500', '1000', '2000', '4000']:
            self.rightboneconduction.source = 'Images/' + symbolList[0] + '.png'
            self.leftboneconduction.source = 'Images/' + symbolList[2] + '.png'


        print self.text  # references the level,
        print self.parent.parent.frequencyLabel  # references the frequency


        return



    def on_touch_down(self, touch):
        if (self.collide_point(*touch.pos) and touch.is_double_tap == False
            and self.parent.parent.parent.parent.parent.parent.parent.parent.ids.drawlineDrawer.collapse == False):
            print('my precious you found the parent')
            # so now I want to reference a draw method in the audiogramW canvas I think?
            # I want it to take thes touck inputs and then take the next collide on drag for a button containing either
            # a r or l AC symbol, and draw a line between them

        elif self.collide_point(*touch.pos) and touch.is_double_tap == False:
            super(AudioButton, self).on_touch_down(touch)
            # print self.text  # references the level,
            # print self.parent.parent.frequencyLabel  #
            print self.parent.parent.parent.parent.ids
            print self.parent.parent.parent.parent.parent.parent.parent.parent.ids  # this is it

        #     double tap
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            currentSymbol = App.get_running_app().controllerOutput
            print currentSymbol
            new_content_list = reCodeStringToButton(currentSymbol)
            self.contents[new_content_list[0]] = [0, 0]  # removes item from list
            symbolList = ButtonDictToString(self.contents)  # this is the

            self.airconduction.source = 'Images/' + symbolList[1] + '.png'

            # only do BC for BC frequencies alternatively could have a second method for intermediate freq
            if self.parent.parent.frequencyLabel in ['125', '250', '500', '1000', '2000', '4000']:
                self.rightboneconduction.source = 'Images/' + symbolList[0] + '.png'
                self.leftboneconduction.source = 'Images/' + symbolList[2] + '.png'
            #self.airconduction.source = 'Icons\EMPTY.png'
            print "popped"  # will need to implement a time delay
        return


class FrequencyColumn(Widget):
    frequencyLabel = StringProperty("")


class HalfFrequencyColumn(Widget):
    frequencyLabel = StringProperty("")


class AudiogramW(Widget):
    soll = NumericProperty(0)
    # def on_touch_up(self, touch):


# frequency column create
# class


class PatientDetails(Widget):
    # takes input for the patient database
    nameLabel = StringProperty("")
    surnameLabel = StringProperty("")
    dateOfBirth = StringProperty("")
    sexLabel = StringProperty("")


class Controller(Widget):
    # select symbols and modifiers, print, and save,load dialog, erase, clear and line markup
    controlID = ObjectProperty(None)
    controllerNR = ObjectProperty(None)
    controllerNote = ObjectProperty(None)

    def getControllerInput(self, symbol):
        # reinit the list on button press - but keep notes and NR
        App.get_running_app().controllerOutput[0:3] = ['--', '-', '--']
        App.get_running_app().controllerOutput[4:7] = ['--', '-', '--']
        # assign values to list
        if symbol == 'ra-':
            App.get_running_app().controllerOutput[0] = 'ra'
            App.get_running_app().controllerOutput[1] = '-'
        elif symbol == 'la-':
            App.get_running_app().controllerOutput[4] = 'la'
            App.get_running_app().controllerOutput[5] = '-'
        elif symbol == 'ram':
            App.get_running_app().controllerOutput[0] = 'ra'
            App.get_running_app().controllerOutput[1] = 'm'
        elif symbol == 'lam':
            App.get_running_app().controllerOutput[4] = 'la'
            App.get_running_app().controllerOutput[5] = 'm'
        elif symbol == 'rb-':
            App.get_running_app().controllerOutput[0] = 'rb'
            App.get_running_app().controllerOutput[1] = '-'
        elif symbol == 'lb-':
            App.get_running_app().controllerOutput[4] = 'lb'
            App.get_running_app().controllerOutput[5] = '-'
        elif symbol == 'rbm':
            App.get_running_app().controllerOutput[0] = 'rb'
            App.get_running_app().controllerOutput[1] = 'm'
        elif symbol == 'lbm':
            App.get_running_app().controllerOutput[4] = 'lb'
            App.get_running_app().controllerOutput[5] = 'm'

        # self.ids.nr.getControllerNR(self.ids.nr.getControllerNR.state)
        # reset notes and NR widgets on new item select
        self.ids.controllerNR.state = 'normal'
        self.ids.controllerNote.text = 'No Note'
        # App.get_running_app().symbolType = symbol
        # print(App.get_running_app().symbolType)
        print(App.get_running_app().controllerOutput)

        # will need to change this so I'm inputting to a list property at a certain position but yay!

    def getControllerNote(self, note):

        # reinit controller Output note info
        App.get_running_app().controllerOutput[3] = '0'
        App.get_running_app().controllerOutput[7] = '0'

        # set pos of list to be relapced based on l or r input
        if App.get_running_app().controllerOutput[0] != '--':
            pos = 3
        else:
            pos = 7

        if note == 'No Note':
            App.get_running_app().controllerOutput[pos] = '0'
            print 'Note0'
        elif note == 'Note 1':
            App.get_running_app().controllerOutput[pos] = '1'
            print 'Note1'
        elif note == 'Note 2':
            App.get_running_app().controllerOutput[pos] = '2'
            print 'Note2'
        elif note == 'Note 3':
            App.get_running_app().controllerOutput[pos] = '3'
            print 'Note1'

        print App.get_running_app().controllerOutput

    def getControllerNR(self, state):
        # Note NR state resets when the getControllerInput method is called
        no_response_text = '--'
        if state == 'normal':
            App.get_running_app().controllerOutput[2] = '--'
            App.get_running_app().controllerOutput[6] = '--'
        if state == 'down':
            no_response_text = 'nr'

        if App.get_running_app().controllerOutput[0] != '--':
            App.get_running_app().controllerOutput[2] = no_response_text
            App.get_running_app().controllerOutput[6] = '--'
        if App.get_running_app().controllerOutput[4] != '--':
            App.get_running_app().controllerOutput[6] = no_response_text
            App.get_running_app().controllerOutput[2] = '--'

        print App.get_running_app().controllerOutput

        print(state)

        # get input from widgets and pass to the audiogram button widgets


class MainScreen(TabbedPanel):
    drawlineDrawer = ObjectProperty()
    pass


class DrawAudioApp(App):
    symbolType = StringProperty
    controllerOutput = ListProperty(['--', '-', '--', '0', '--', '-', '--', '0'])


    def build(self):
        return MainScreen()
        # return AudiogramW()
        # return DatePicker()


if __name__ == '__main__':
    DrawAudioApp().run()
