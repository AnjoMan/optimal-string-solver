from pyomo.environ import *

infity = float('inf')

model = AbstractModel()



# set of potential string lengths
model.F = Set()
# potential strings per MPPT
model.M = Set()



#number of panels per string length
model.f = Param(model.F, within=NonNegativeIntegers)

#number of strings per mppt grouping
model.m = Param(model.M, within=NonNegativeIntegers)


# max number of panels
model.Pmax = Param(within=NonNegativeIntegers)
# max number of panels we can remove
model.p_r = Param(within=NonNegativeIntegers)

#
model.x = Var(model.F, within=NonNegativeIntegers)
model.g = Var(model.F, model.M, within=NonNegativeIntegers)

# define the objective function
def cost_rule(model):
    return sum(model.x[i] for i in model.F)
model.cost = Objective(rule=cost_rule)


# define Pmax Constraint
def panel_limit(model):
    return model.Pmax >= sum(model.f[i]*model.x[i] for i in model.F)
model.max_panel_count = Constraint(model.F, rule=panel_limit)

def panel_relaxation(model):
    return model.Pmax-model.p_r <= sum(model.f[i]*model.x[i] for i in model.F)
model.max_panel_relaxation = Constraint(model.F, rule=panel_relaxation)


#
def mppt_string_count(model, i):
    return model.x[i] == sum(model.m[j]*model.g[i,j] for j in model.M)
model.mppt_grouping = Constraint(model.F, rule=mppt_string_count)
