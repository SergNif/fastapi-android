from pydantic import BaseModel

class Fitness(BaseModel):
    __tablename__="fitnes"
    id = Column(Integer, primary_key = True)
    email = Column(String(255), nullable = False, unique = True)
    fullName= Column(String(25), nullable = False, unique = False)
    
    Nothing = Column(Boolean, default = False)#": false,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:55 PM",
    fastFood = Column(Boolean, default = False)#": true,
    fastSugar = Column(Boolean, default = False)#": false,
    laterNight = Column(Boolean, default = False)#": true
    
    age = Column(Integer, nullable= False)#": 30,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:19:31 PM",
    desired_weight = Column(FLOAT(precision=10, scale=2))#": 50.0,
    height = Column(Integer, nullable= False)#": 20,
    weight = Column(FLOAT(precision=10, scale=2))#": 40.0
    
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:25 PM",
    everyDayFitness = Column(Boolean, default = False)#": false,
    examine1_2TimesWeek = Column(Boolean, default = False)#": false,
    examine3_5TimesWeek = Column(Boolean, default = False)#": false,
    fastWalkOnFoot = Column(Boolean, default = False)#": true,
    minimalPhysicalActive = Column(Boolean, default = False)#": false
    
    chicken = Column(Boolean, default = False)#": false,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:34 PM",
    fish = Column(Boolean, default = False)#": true,
    meat = Column(Boolean, default = False)#": false,
    pork = Column(Boolean, default = False)#": true,
    seaFood = Column(Boolean, default = False)#": true,
    tyrkey = Column(Boolean, default = False)#": true,
    withoutFish = Column(Boolean, default = False)#": false,
    withoutMeat = Column(Boolean, default = False)#": false
    
    avocado = Column(Boolean, default = False)#": false,
    broccoli = Column(Boolean, default = False)#": true,
    cauliflower = Column(Boolean, default = False)#": false,
    cucumbers = Column(Boolean, default = False)#": false,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:42 PM",
    ggplant = Column(Boolean, default = False)#": true,
    mushrooms = Column(Boolean, default = False)#": true,
    tomato = Column(Boolean, default = False)#": true,
    zucchini = Column(Boolean, default = False)#": false
    
    cheese = Column(Boolean, default = False)#": true,
    cottage = Column(Boolean, default = False)#": false,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:47 PM",
    egg = Column(Boolean, default = False)#": false,
    kefir = Column(Boolean, default = False)#": false,
    nuts = Column(Boolean, default = False)#": true,
    yogurt = Column(Boolean, default = False)#": true
    
    coffee = Column(Boolean, default = False)#": false,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:50 PM",
    tea = Column(Boolean, default = False)#": false,
    waterSugarGas = Column(Boolean, default = False)#": true,
    waterWithoutGas = Column(Boolean, default = False)#": false
    
    InHome = Column(Boolean, default = False)#": false,
    OnFoot = Column(Boolean, default = False)#": false,
    date = Column(Date, nullable = False)#": "May 4, 2022 12:20:53 PM",
    regularTraffic = Column(Boolean, default = False)#": true,
    workOffice = Column(Boolean, default = False)#": false

    man = Column(Boolean, default = False)#": true,
    woman = Column(Boolean, default = False)#": false