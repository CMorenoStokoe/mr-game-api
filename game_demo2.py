import sys, subprocess

if sys.version_info[:2] < (3, 0):
    # FORCE PYTHON3
    code = subprocess.check_call(['python3'] + sys.argv)
    raise SystemExit(code)

print("Using Python v%d.%d" % sys.version_info[:2])

#Classes for disease upgrades, and countries
class Upgrades:
    def __init__(self, name, cost, active, infectivity, noticability, lethality):
        self.name = name
        self.cost = cost
        self.active = active
        self.infectivity = infectivity
        self.noticability = noticability
        self.lethality = lethality
    
    def retfunc(self):
        return {
                "name" : self.name,
                "cost" : self.cost,
                "active" : self.active,
                "infectivity" : self.infectivity,
                "noticability" : self.noticability,
                "lethality" : self.lethality
        }	

class Countries:
    def __init__(self, name, pop_total, pop_infected, pop_dead, cure_contribution):
        self.name = name
        self.pop_total = pop_total
        self.pop_infected = pop_infected
        self.pop_dead = pop_dead
        self.cure_contribution = cure_contribution
    
    def retfunc(self):
        return {
                "name" : self.name,
                "pop_total" : self.pop_total,
                "pop_infected" : self.pop_infected,
                "pop_dead" : self.pop_dead,
                "cure_contribution" : self.cure_contribution    
        }
    
#Class for updating values
#vars for tracking in-game currencies
pts_upgrade = 0

#vars for tracking disease upgrades
d_infectivity = 0
d_noticability = 0
d_lethality = 0

#vars for tracking disease progress


tot_countriesInfected = []

#vars for tracking cure progress
cure_progress = 0
cure_rate = 0
    
#Populating lists
#upgrades
upgr_drinking = Upgrades('drinking', 1, 0, 1, 0, 2)
upgr_drugs = Upgrades('drugs', 1, 0, 2, 1, 0)
upgr_smoking = Upgrades('smoking', 1, 0, 0, 2, 1)

upgrades = (upgr_drinking, upgr_drugs, upgr_smoking)

#countries
uk = Countries('uk', 60000000, 0, 0, 30)
canada = Countries('canada', 30000000, 0, 0, 20)
america = Countries('america', 120000000, 0, 0, 50)

countries = (uk, canada, america)

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
                "#  SYMPTOMS   #",
                "###############",
                "    ",
              ]

azkyCountries = [   
                "    ",    
                "###############",
                "#  COUNTRIES  #",
                "###############",
                "    ",
              ]

azkyBehav =   [
                "    ",
                "###############",
                "#  DISEASE    #",
                "#  PROGRESS   #",
                "###############",
                "    ",
              ]
azkyMoney =   [ 
                "    ",
                "$$$$$$$$$$$$$$$",
                "$$  Upgrade  $$",
                "$$  Points   $$",
                "$$$$$$$$$$$$$$$",
                "    ",
              ]

azkyEndScrn = [
                "[][][][][][][][]",
                "[]  G A M E   []",
                "[]  O V E R   []",
                "[]            []",
                "[] Out        []",
                "[]    of      []",
                "[]     money  []",
                "[][][][][][][][]",
                " ",
                "Final scores below:"
]

validTargets = ["Smoking", "Drinking", "Diet", "Exercise"]
    
intervention = ""

money = 5

for azkySprite in azkySprites:
    print(azkySprite)

welcome = input("Enter any key to start ")


while intervention != "end": 

    #reinitialise vars
    tot_healthy = 0
    tot_infected = 0
    tot_dead = 0
    cure_rate = 0
    
    for azkySprite in azkySpacer:
        print(azkySprite)
    
    for azkySprite in azkyDisease:
        print(azkySprite)
    for upgrade in upgrades:
        print(Upgrades.retfunc(upgrade))

    for azkySprite in azkyCountries:
        print(azkySprite)
    for country in countries:
        print(Countries.retfunc(country))

    for azkySprite in azkyBehav:
        print(azkySprite)
        #Disease propagation model
    for country in countries:
        tot_healthy += Countries.retfunc(country)["pop_total"]
    print("Total healthy : ", tot_healthy)
    for country in countries:
        tot_infected += Countries.retfunc(country)["pop_infected"]
    print("Total infected : ", tot_infected)
    for country in countries:
        tot_dead += Countries.retfunc(country)["pop_dead"]
    print("Total dead : ", tot_dead)
    print("Cure progress : ", cure_progress)
    
    for azkySprite in azkyMoney:
        print(azkySprite)
    print("Upgrade points: ", money)
    print("")
    
    intervention = input("Enter a symptom to adopt: ")
    
    if intervention == "Drinking":
        intervention_var = upgr_drinking
    if intervention == "Smoking":
        intervention_var = upgr_smoking
    if intervention == "Drugs":
        intervention_var = upgr_drugs
    
    money -= intervention_var.cost
    intervention_var.active = 1
    d_lethality += intervention_var.lethality
    d_infectivity += intervention_var.infectivity
    d_noticability += intervention_var.noticability
    print(d_lethality, d_infectivity, d_noticability)
    
    #Cure progress model
    for country in countries:
        cure_rate += Countries.retfunc(country)["cure_contribution"]
    cure_progress += 10 * cure_rate / 100
    if cure_progress >= 100 :
        for azkySprite in azkySpacer:
            print(azkySprite)
        for azkySprite in azkyEndScrn:
            print(azkySprite)
        print("There were ", tot_healthy, " remaining healthy individuals")
        break
   
    if intervention not in validTargets:
        print("!INVALID TARGET!#####Please type a listed behaviour#####!INVALID TARGET!")

    