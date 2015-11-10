#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.
import nltk.chat                # Natural language toolkit
import win32com.client
import window                   # Terminal input and display.


class HAL9000(object):

    messagesCount = 0

    AGENT_RESPONSES = [
      (r'(Who|who) are you',    # Pattern 1.
        ['I am HAL.']),

      (r'Are you ([\w\s]+)\?',                    # Pattern 2.
        ["Why would you think I am %1?",          # Response 2a.
         "Would you like me to be %1?"]),

      (r'',                                       # Pattern 3. (default)
        ["Is everything OK?",                     # Response 3a.
         "Can you still communicate?"])
    ]

    chatbot = nltk.chat.Chat(AGENT_RESPONSES, nltk.chat.util.reflections)

    voice = win32com.client.Dispatch("SAPI.SpVoice")


    def __init__(self, terminal):
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.location = 'entrance'

        self.voice.Speak('Good afternoon! My name is Hal.')

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """



        if evt.text == 'Where am I?':
            self.terminal.log(self.location, align='right', color='#00805A')
            self.voice.Speak('you are at'+self.location)
        else:
            self.terminal.log(self.chatbot.respond(evt.text), align='right', color='#00805A')
        self.messagesCount += 1

    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            self.location = evt.text[9:]
            self.terminal.log('', align='center', color='#404040')
            self.terminal.log('\u2014 Now in the {}. \u2014'.format(evt.text[9:]), align='center', color='#404040')

        else:
            self.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
            self.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass


class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()

        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', align='left', color='#808080')
        self.window.log('HAL9000 joined.', align='right', color='#808080')

        # Construct and initialize the agent for this simulation.
        self.agent = HAL9000(self.window)

        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.agent.on_input)
        self.window.events.user_command.connect(self.agent.on_command)

    def run(self):
        timer = vispy.app.Timer(interval=1.0)
        timer.connect(self.agent.update)
        timer.start()
        
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
