'''
Created on Oct 2, 2015

@author: luozhipei
'''
class option(object):
    """An option object

    Attributes:
        location: where you are building the factory.
        cost: construction costs.
        yearstocomplere: years to build factory
        lifeTime
        discount: the interest rate for NPV calculation
        union: true or false
        costpercar: labor cost for this option
        revenuepercar: not including labor costs
        monthlyoutput: how many cars you build each month
        npv: the calculated net present value
    """

    def __init__(self, location, cost, yearstocomplete, 
                lifetime, discount, union, costpercar, 
                revenuepercar, monthlyoutput):
        """Return an option object 
        with the given parameters initialized
        """
        self.location = location
        self.cost = cost
        self.yearstocomplete = yearstocomplete
        self.lifetime = lifetime
        self.discount = discount
        self.union = union
        self.costpercar = costpercar
        self.revenuepercar = revenuepercar
        self.monthlyoutput = monthlyoutput
        self.senNpv = []
        self.senPoint = [0 for i in range(0, 10)]
        self.explanation = {}
        
    def __str__(self):
        return ("#<option location: " + self.location + 
            " cost: " + str(self.cost) + ">")
        
    def get_location(self): return self.location 
    def get_cost(self): return self.cost
    def get_yearstocomplete(self): return self.yearstocomplete
    def get_lifetime(self): return self.lifetime
    def get_discount(self): return self.discount
    def get_union(self): return self.union
    def get_costpercar(self): return self.costpercar
    def get_revenuepercar(self): return self.revenuepercar
    def get_monthlyoutput(self): return self.monthlyoutput            
    
    
class decision(object):
    """A decision object

    Attributes:
        options: a list of option object
        stakeholders: a list of stakeholder
        choice: the selected option
        explanation: the justification for the decision
    """

    def __init__(self, options, stakeholders):
        """Return a decision object 
        with the given option list and stakeholder list
        """
        self.options = options
        self.stakeholders = stakeholders
        
    def __str__(self):
        return ("#<decision options: " + str(self.options) + 
            " stakeholders: " + str(self.stakeholders) + ">")
        
    def get_options(self):
        return self.options
    
    def get_stakeholders(self):
        return self.stakeholders
    
def decide(optionList):
        npvMax = 0
        optionMax = {}
        for option in optionList:
            myNpv = npv(option)
            option.npv = myNpv
            optionMax = option if myNpv > npvMax else optionMax
            npvMax = myNpv if myNpv > npvMax else npvMax
        return optionMax
    
def npv(option):
        myNpv = 0
        costPerYear = option.cost / option.yearstocomplete
        for i in range(1, option.yearstocomplete + 1):
            myNpv -= costPerYear / ((1 + option.discount) ** i)
        for i in range(option.yearstocomplete + 1, option.lifetime + 1):
            myNpv += 12 * option.monthlyoutput * (option.revenuepercar - option.costpercar) / ((1 + option.discount) ** i)
        return myNpv
    
def sensitivity(optionList):
    for option in optionList:
        for opAttr in ['cost', 'discount', 'costpercar', 'revenuepercar', 'monthlyoutput']:
            """
            The following code gets and sets the attributes and 
            calculate the npvs accordingly.
            """
            oriValue = getattr(option, opAttr)
            setattr(option, opAttr, oriValue * 1.2)
            option.senNpv.append(npv(option))
            setattr(option, opAttr, oriValue * 0.8)
            option.senNpv.append(npv(option))
            setattr(option, opAttr, oriValue)
            
    maxIndex = [0 for i in range(0, 10)]
    maxSensi = [0 for i in range(0, 10)]
    
    pointWeight = [1,1,2,2,3,3,3,50,1,1]
    
    optionPoints = [0 for i in range(0, len(optionList))]
    curIndex = 0
    for option in optionList:
        for i in range(0, 10):
            if maxSensi[i] <= option.senNpv[i]:
                maxSensi[i] = option.senNpv[i]
                maxIndex[i] = curIndex
        curIndex += 1
        
    for i in range(0, 10):
        optionPoints[maxIndex[i]] += pointWeight[i]
        optionList[maxIndex[i]].senPoint[i] += 1
    
    return optionList[optionPoints.index(max(optionPoints))]   
            
def explain(optionList, stackHolder = None):
    if stackHolder is None:
        stackHolder = ['stockholders']
    preferOption = decide(optionList)
    senOption = sensitivity(optionList)
    
    for holder in stackHolder:
        if holder == 'stockholders':
            preferOption.explanation[holder] = "My fellow " + holder + " members, " + "the preferred choice is " + preferOption.location
            preferOption.explanation[holder] += ", because it has the highest expected profit return (Net Present Value): " + str(preferOption.npv)
            if preferOption.location == senOption.location:
                preferOption.explanation[holder] += ",\n and even when conditions vary, " + preferOption.location + " has the best profit in most cases."
            else :
                preferOption.explanation[holder] += ",\n although to be fair, " + preferOption.location + " may have worse tolerance towards changes."
        elif holder == 'unions':
            preferOption.explanation[holder] = "My fellow " + holder + " members, " + "the preferred choice is " + preferOption.location
            preferOption.explanation[holder] += ", because it has the highest expected profit return : " + str(preferOption.npv)
            if preferOption.union == True:
                preferOption.explanation[holder] += ".\n Besides, our factory will have a labor union, which fits your benefits."
            else :
                if preferOption.senPoint[4] : #If with a raise in wage, the preferred option still wins
                    preferOption.explanation[holder] += ".\n Even though we don't plan on a labor union right now, we can stand a wage raise,\n thus a union may be possible in the future."
                else :
                    preferOption.explanation[holder] += ".\n We have no future plans on setting up a labor union. Sorry"
        else :
            preferOption.explanation[holder] = "My fellow " + holder + " members, " + "the preferred choice is " + preferOption.location
            if holder == preferOption.location:
                preferOption.explanation[holder] += ", because you offer us the highest expected profit return (Net Present Value): " + str(preferOption.npv)
                negParts = ""
                for pointIndex in range(0, len(preferOption.senPoint)):
                    if preferOption.senPoint[pointIndex] == 0:
                        if len(negParts) != 0:
                            negParts += "or "
                        negParts += returnStr(pointIndex)
                if len(negParts) > 0:
                    preferOption.explanation[holder] += ".\n However, if there is a " + negParts + ",\n we might reconsider our decision and choose other options."
            else:
                preferOption.explanation[holder] += ", because you failed to offer us the highest expected profit return, which is " + str(preferOption.npv)
                posParts = ""
                for pointIndex in range(0, len(preferOption.senPoint)):
                    if preferOption.senPoint[pointIndex] == 0:
                        if len(posParts) != 0:
                            posParts += "or "
                        posParts += returnStr(pointIndex)
                if len(posParts) > 0:
                    preferOption.explanation[holder] += ".\n However, if there is a " + posParts + ",\n we might reconsider our decision and choose you as our option."
                
    return decision(preferOption, stackHolder)

def returnStr(index):
    if index % 2 == 0:
        res = "raise "
    else:
        res = "drop "
    
    res += "of "
    
    if index / 2 == 0:
        res += "cost "
    elif index / 2 == 1:
        res += "npv discount "
    elif index / 2 == 2:
        res += "labor cost per car "
    elif index / 2 == 3:
        res += "revenue per car "
    else:
        res += "monthly car output "
        
    return res
    
optOH = option("OH", 40000000, 2, 12, .05, True, 6500,
                    10000, 1000)
optSC = option("SC", 20000000, 2, 10, .05, True, 4000,
                    10000, 500)

s = ["stockholders", "unions", "OH", "SC"]
opt = [optOH, optSC]
d = decision(opt, s)

"""
print decide(opt)
print sensitivity(opt)
print('OH npv: ' + str(optOH.npv))
print("SC npv: " + str(optSC.npv))

printStr = ""
index = 0
for loc in ['OH', 'SC']:
    attrIndex = 0
    options = opt[index]
    for attr in ['cost', 'discount', 'costpercar', 'revenuepercar', 'monthlyoutput']:
        printStr += loc + ':\t' + attr + ':\t'
        printStr += str('%e' % options.senNpv[attrIndex]) + '  ' + str('%e' % options.senNpv[attrIndex + 1]) + ' '
        printStr += 'Sensitivity:\t' + str('%e' % (options.senNpv[attrIndex] - options.senNpv[attrIndex + 1]))
        printStr += '\n'
        attrIndex += 2
    index += 1
print printStr

for explanation in explain(opt, d.stakeholders).options.explanation.items():
    print explanation[1]
"""
    