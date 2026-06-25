# =========================
# Immutable Data Type Demo
# =========================

x = 10
print("x =", x)
print("Memory address of x:", id(x))

x = 20
print("\nx =", x)
print("New memory address of x:", id(x))

# Tech Lead Explanation:
# The memory address changes because integers are immutable in Python.
# When we assign x = 20, Python does not modify the existing integer object whose value is 10. Instead, it creates (or reuses) a different integer object representing 20 and makes x reference that object.
#
# In C++, a typical integer variable stores the value directly in memory.
# Modifying the variable changes the value at the same memory location.
# Python variables are references to objects, so reassigning an immutable object points the variable to a different object rather than modifying the original one.


# =======================
# Mutable Data Type Demo
# =======================

my_list = [1, 2, 3]
print("\nmy_list =", my_list)
print("Memory address of my_list:", id(my_list))

my_list.append(4)
print("\nmy_list after append =", my_list)
print("Memory address after append:", id(my_list))

# Explanation:
# The memory address stays the same because lists are mutable in Python.
# The append() method modifies the existing list object in place instead
# of creating a new list object. Since the same object is being changed,
# its identity (returned by id()) remains unchanged.