ALWAYS_TRUE = [("LoadConstTrue", [("Reg8", False, 0)]), ("Ret", [("Reg8", False, 0)])]
ALWAYS_FALSE = [("LoadConstFalse", [("Reg8", False, 0)]), ("Ret", [("Reg8", False, 0)])]
ALWAYS_UNDEFINED = [
    ("LoadConstUndefined", [("Reg8", False, 0)]),
    ("Ret", [("Reg8", False, 0)]),
]
EMPTY_OBJECT = [("NewObject", [("Reg8", False, 0)]), ("Ret", [("Reg8", False, 0)])]
