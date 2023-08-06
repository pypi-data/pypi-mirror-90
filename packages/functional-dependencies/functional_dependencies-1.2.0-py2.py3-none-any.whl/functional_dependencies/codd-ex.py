from functional_dependencies import FD, FDSet, RelSchema, _rels2string

fde1 = FD("EmpSerialNo", {"JobCode", "DeptNo"})
fdd1 = FD("DeptNo", "ManagerNo")
fdd2 = FD("ManagerNo", {"DeptNo", "Contract"})
fds = FDSet({fde1, fdd1, fdd2})
employee = RelSchema(fds.attributes(), fds)
normalized = employee.synthesize()
print(_rels2string(normalized))
