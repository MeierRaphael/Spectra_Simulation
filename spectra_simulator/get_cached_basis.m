function spin_system = get_cached_basis(spin_system, bas, key_components)
%GET_CACHED_BASIS Reuses or creates a Spinach basis and caches it.

    persistent basis_cache
    if isempty(basis_cache)
        basis_cache = containers.Map();
    end

    % Construct a unique key (safe for Map)
    key = sprintf('n%d_a%s_l%d_i%s', ...
        key_components.n_spins, ...
        key_components.approx, ...
        key_components.approx_level, ...
        strjoin(key_components.isotopes, '-'));

    % Check cache
    if isKey(basis_cache, key)
        disp("⏩ Reusing cached basis for: " + key);
        spin_system.bas = basis_cache(key);
    else
        disp("⚙️ Generating basis for: " + key);
        spin_system = basis(spin_system, bas);
        basis_cache(key) = spin_system.bas;
    end
end
