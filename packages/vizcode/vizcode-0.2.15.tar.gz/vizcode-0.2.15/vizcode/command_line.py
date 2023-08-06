import argparse

class Command_Line:
    def __init__(self):
        parser = argparse.ArgumentParser(description = "Description for my parser")
        parser.add_argument("-H", "--Help", help = "Example: Help argument", required = False, default = "")
        parser.add_argument("-p", "--path", help = "Path to your python directory", required = True, default = "")
        parser.add_argument("-t", "--test", help = "Path to the test files in your directory", required = False, default = None)
        parser.add_argument("-e", "--env", help = "Path to python environment", required = False, default = None)

        argument = parser.parse_args()
        self.path = None
        self.env = None
        self.test = None
        status = False

        if argument.Help:
            print("You have used '-H' or '--Help' with argument: {0}".format(argument.Help))
            status = True
        if argument.path:
            print("You have used '-p or '--path' with argument: {0}".format(argument.path))
            self.path = argument.path
            status = True
        if argument.env:
            print("You have used '-e' or '--env' with argument: {0}".format(argument.env))
            self.env = argument.env
            status = True
        if argument.test:
            print("You have used '-t' or '--test' with argument: {0}".format(argument.test))
            self.test = argument.test
            status = True
        if not status:
            print("Maybe you want to use -H or -s or -p or -p as arguments ?")

    def get_path(self):
        return self.path 

    def get_env(self):
        return self.env
    
    def get_test(self):
        return self.test