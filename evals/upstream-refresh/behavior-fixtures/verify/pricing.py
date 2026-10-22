def total(cents, tax_basis_points):
    return cents + cents * tax_basis_points // 10000
