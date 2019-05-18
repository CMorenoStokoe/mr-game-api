#Class for diseases, which each have risk factors (percentages which sum to 100%)
class Diseases:
    def __init__(self, name, risk_smok, risk_drink, risk_diet, risk_exer):
        self.name = name
        self.risk_smok = risk_smok
        self.risk_drink = risk_drink
        self.risk_diet = risk_diet
        self.risk_exer = risk_exer
    
    def retfunc(self):
        return {
                "Disease" : self.name,
                "RiskFactor_Smoking" : self.risk_smok,
                "RiskFactor_Drinking" : self.risk_drink,
                "RiskFactor_Diet" : self.risk_diet,
                "RiskFactor_Exercising" : self.risk_exer
        }

#Populating disease list

lungCancer_risks = Diseases('Lung cancer', 60, 10, 20, 10)
heartDisease_risks = Diseases('Heart disease', 20, 20, 40, 20)
liverDisease_risks = Diseases('Liver disease', 20, 40, 20, 20)

diseaseList = [lungCancer_risks, heartDisease_risks, liverDisease_risks]

#Populating initial prevalence values

prev_Smoking=100
prev_Drinking=100
prev_Diet=100
prev_Exercise=100

#Lists for UI  
azkySpacer = ["    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    ",    "    "]

azkySprites = [
                "    ",
                "###############",
                "###############",
                "### WELCOME ###",
                "###  TO A   ###",
                "###  DEMO   ###",
                "###############",
                "###############",
                "    ",
              ]
azkyDisease = [   
                "    ",    
                "###############",
                "#   DISEASE   #",
                "#  PREVALENCE #",
                "###############",
                "    ",
              ]
azkyBehav =   [
                "    ",
                "###############",
                "#  BEHAVIOUR  #",
                "#  PREVALENCE #",
                "###############",
                "    ",
              ]
azkyMoney =   [ 
                "    ",
                "$$$$$$$$$$$$$$$",
                "$$  BUDGET   $$",
                "$$$$$$$$$$$$$$$",
                "    ",
              ]

validTargets = ["Smoking", "Drinking", "Diet", "Exercise"]
    
intervention = ""

money = 100000

for azkySprite in azkySprites:
    print(azkySprite)

welcome = input("Enter any key to start ")


while intervention != "end":

    prev_LungCancer=Diseases.retfunc(lungCancer_risks)["RiskFactor_Smoking"]*prev_Smoking + Diseases.retfunc(lungCancer_risks)["RiskFactor_Drinking"]*prev_Drinking + Diseases.retfunc(lungCancer_risks)["RiskFactor_Diet"]*prev_Diet + Diseases.retfunc(lungCancer_risks)["RiskFactor_Exercising"]*prev_Exercise
    prev_HeartDisease=Diseases.retfunc(heartDisease_risks)["RiskFactor_Smoking"]*prev_Smoking +Diseases.retfunc(heartDisease_risks)["RiskFactor_Drinking"]*prev_Drinking +Diseases.retfunc(heartDisease_risks)["RiskFactor_Diet"]*prev_Diet + Diseases.retfunc(heartDisease_risks)["RiskFactor_Exercising"]*prev_Exercise
    prev_LiverDisease= Diseases.retfunc(liverDisease_risks)["RiskFactor_Smoking"]*prev_Smoking +Diseases.retfunc(liverDisease_risks)["RiskFactor_Drinking"]*prev_Drinking +Diseases.retfunc(liverDisease_risks)["RiskFactor_Diet"]*prev_Diet +Diseases.retfunc(liverDisease_risks)["RiskFactor_Exercising"]*prev_Exercise

    for azkySprite in azkySpacer:
        print(azkySprite)
    
    for azkySprite in azkyDisease:
        print(azkySprite)
    print("Lung Cancer : ", prev_LungCancer)
    print("Heart Disease : ", prev_HeartDisease)
    print("Liver Disease : ", prev_LiverDisease)

    for azkySprite in azkyBehav:
        print(azkySprite)
    print("Smoking : ", prev_Smoking)
    print("Drinking : ", prev_Drinking)
    print("Diet : ", prev_Diet)
    print("Exercise : ", prev_Exercise)
    
    for azkySprite in azkyMoney:
        print(azkySprite)
    print("Budget remaining: ", money)
    print("")
    
    intervention = input("Enter a behaviour to intervene upon (-10% prevalence) ")
    
    if intervention == "Smoking":
        prev_Smoking -= 10 
        money -= 10000
    if intervention == "Drinking":
        prev_Drinking -= 10 
        money -= 10000
    if intervention == "Diet":
        prev_Diet -= 10 
        money -= 10000
    if intervention == "Exercise":
        prev_Exercise -= 10 
        money -= 10000
    
    if money == 0 :
        print("!OUT OF BUDGET!#####Final scores below:#####!OUT OF BUDGET!")
        print("Lung Cancer : ", prev_LungCancer)
        print("Heart Disease : ", prev_HeartDisease)
        print("Liver Disease : ", prev_LiverDisease)
        break
   
    if intervention not in validTargets:
        print("!INVALID TARGET!#####Please type a listed behaviour#####!INVALID TARGET!")

    