class Developer:
    def __init__(self):
        self.name = "Donoban"
        self.role = "Frontend Developer"
        self.location = "Colombia 🇨🇴"
        self.education = "Systems Engineering Student"
        self.company = "Tiendana S.A.S"

    def say_hi(self):
        print("Debugging my life one commit at a time.")
        print(self.name)
        print(self.role)
        print(self.location)


me = Developer()
me.say_hi()