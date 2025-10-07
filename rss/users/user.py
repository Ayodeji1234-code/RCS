class User:
    def __init__(self,username,name,role):
        self.username = username
        self.name = name
        self.role = role

    def view_details(self):
        return f'\nName : {self.name}\nUsername : {self.username}\nRole : {self.role}'
        