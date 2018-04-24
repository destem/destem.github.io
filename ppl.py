#The Python code a[j:k] means Bpositions j, j + 1, . . . , k – 1^ in the vector a. The code a[j,:] means Bthe entire row indexed by j^ in matrix a. The expression range(j) means 0, 1, . . . , j – 1.
def AdvanceByOne(u, a, c, d):
    return (u, a, c, d+1)
    
def ComputeWindowErrorMatrix(curve): 
    l_curve = len(curve)
    M = zeros([l_curve-min_window+1, l_curve-min_window+1])
    for i in range(l_curve-min_window):
        if i > 0: 
            warm_start_parameters = AdvanceByOne(previous_parameters)
            fit = FitPowerLaw(curve[i:i+min_window], warm_start=warm_start_parameters) 
        else:
            fit = FitPowerLaw(curve[i:i+min_window]) 
            previous_parameters = fit.parameters 
            M[i,0] = fit.error 
            warm_start_parameters =previous_parameters
            for j in range(l_curve-i-min_window):
                fit = FitPowerLaw(curve[i:i+j+ min_window+1], warm_start=warm_start_parameters)
                warp_start_parameters = fit.parameters M[i,j+1] = fit.error
    return M
    
def FitPiecewisePowerLaw(curve, min_window=50, max_pieces=10):
    l_curve = len(curve)
    M = ComputeWindowErrorMatrix(curve,min_window)
    P = zeros([max_pieces, l_curve+1]) + infinity
    B = zeros([max_pieces, l_curve+1]) P[0,:] = M[0,:]
    for i in range(1, max_pieces):
        for j in range(1, n+1):
            vals = P[i-1,0:j] + M[0:j,j]
            argm = argmin(vals)
            P[i,j] = vals[argm]
            B[i,j] = argm
            best_paths = [None] * max_pieces
            for pl_i in range(max_pieces): 
                best_paths[pl_i] = [l_curve]
                j = pl_i
                while j > 0: 
                    best_paths[pl_i].append(B[j,best_paths[pl_i][−1]]) j -= 1
                    best_paths[pl_i].append(0) best_paths[pl_i].reverse()
    return P, B, best_paths