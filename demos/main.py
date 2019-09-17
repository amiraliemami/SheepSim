
print("importing-------")
import scopetest 
from scopetest import global_variable # Needed to access the global variable.

print("building object-------")
point_1 = scopetest.GeoPoint()

print("calling method-------")
try:
    point_1.another_method()
except Exception as e:
    print(e)
    
print("getting variables-------")
# Note that we don't need to define global_variable as global as it isn't global here.
print(scopetest.global_variable + " printed from an external script.") 
print(scopetest.GeoPoint.class_attribute + " printed from an external script.")
print(point_1.instance_variable + " printed from an external script.")

print("getting local method variable-------")
# Test we can't reach method local variables:
try:
    print(point_1.method_local_variable + " printed from an external script.")
except Exception as e:
    print(e)



