class User(object):
    def __init__(self, inputDict, api):
        self.API = api
        self.Id = inputDict["id"]
        self.Name = inputDict["name"]
        self.RoleId = inputDict["roleId"]
        self.Email = inputDict["email"]
        self.PhoneNumber = inputDict["phoneNumber"]
        self.LanguageCode = inputDict["languageCode"]
        self.CanViewComfortVideo = inputDict["canViewComfortVideo"]
        self.UserReadTermsAndConditions = inputDict["userReadTermsAndConditions"]
        self.EulaLastUpdatedTime = inputDict["eulaLastUpdatedTime"]
        self.UserNotificationsSettings = inputDict["userNotificationsSettings"]
        self.UserStorages = inputDict["userStorages"]
        self.PasswordExpirationDays = inputDict["passwordExpirationDays"]
        self.CanAccessSmokeCannon = inputDict["canAccessSmokeCannon"]
        self.AccessCode = inputDict["accessCode"]
        self.EmailConfirmationStatus = inputDict["emailConfirmationStatus"]
        self.PackageOfferings = inputDict["PackageOfferings"]

    def ChangePanelPin(self, newPin):
        api.ChangeUserPanelPin(self.Id, str(newPin))
