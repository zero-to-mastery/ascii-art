# my first Hacktoberfest open-source contribution

logo = """
██╗  ██╗ █████╗  ██████╗██╗  ██╗████████╗ ██████╗ ██████╗ ███████╗██████╗ ███████╗███████╗███████╗████████╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
███████║███████║██║     █████╔╝    ██║   ██║   ██║██████╔╝█████╗  ██████╔╝█████╗  █████╗  ███████╗   ██║   
██╔══██║██╔══██║██║     ██╔═██╗    ██║   ██║   ██║██╔══██╗██╔══╝  ██╔══██╗██╔══╝  ██╔══╝  ╚════██║   ██║   
██║  ██║██║  ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝██████╔╝███████╗██║  ██║██║     ███████╗███████║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   
                                                                                                           
"""

question1 = input("What is your name?: ")
question2 = input("Is this your first open-source experience?: ")

welcomingMsg = f"\nWelcome {question1}, to your first.....\n{logo}"
print(welcomingMsg)