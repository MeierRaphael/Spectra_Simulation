function [CouplingMatrix] = getCouplingMatrix(spin_matrix, n_spins)
    J = spin_matrix;
    J(logical(eye(size(J)))) = 0;           % eye: Einheitsmatrix same size, logical: 1 = true
    CouplingMatrix = cell(n_spins);
    for i = 1:n_spins
        for j = 1:n_spins
            if J(i,j) ~= 0                  % ~= is nonzero
                CouplingMatrix{i,j} = J(i,j); 
            else
                CouplingMatrix{i,j} = [];
            end
        end
    end
end

