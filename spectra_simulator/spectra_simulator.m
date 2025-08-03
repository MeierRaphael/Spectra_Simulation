function done = spectra_simulator(varargin)
%SPECTRA_SIMULATOR Reads and processes spin matrices from a CSV file and creates spectra data.
%
%   The function expects the CSV file to have the following columns:
%   - 'Name':           String, representing the name of the spin system.
%   - 'Field Strength': Numeric (in MHz), representing the magnetic field strength.
%   - 'n_spins':        Integer, representing the number of spins.
%   - 'spin_matrix':    String, representing a semi-colon delimited matrix
%                       (e.g., "[0. 1. 2.];[3. 4. 5.]"). This string will be
%                       converted into a numeric matrix.
%
%   MANDATORY Input:
%        'approx': approximation (e.g.'none' or 'IK-0)      
%        'approx_level': 1,      
%        'windowSize_ppm': span of the ppm range (e.g. 10)    
%        'offset_ppm': spart of the ppm range (e.g.0)
%        'npoints': number points to calculate in the ppm range (e.g.500)
%        'x': number of row to process in the csv file (e.g. 'all' or 10)
%
%   Output:
%       data (struct array): A structure array where each element corresponds
%                            to a row in the CSV file, containing the following fields:
%           .Name (string)
%           .FieldStrength (double)
%           .n_spins (double)
%           .spin_matrix (double matrix)

    timestamp = string(datetime('now', 'Format', 'yyyyMMdd_HHmmss'));
    
    params = struct('approx', 'IK-0', ...
    'approx_level', 1, ...
    'windowSize_ppm', 13, ...
    'offset_ppm', -1, ...
    'npoints', 4000, ...
    'formalism', 'sphten-liouv',...
    'apodisation', 'exp',...
    'apodisation_level', 2,...
    'x', '2' ...
    );

    % Override with input values
    for i = 1:2:length(varargin)
        params.(varargin{i}) = varargin{i+1};
    end

    % Load CSV
    opts = detectImportOptions('..\data\temp_dataset.csv', 'Delimiter',',');
    data = readtable('..\data\temp_dataset.csv', opts);
    
    % how many rows to process
    if ischar(params.x) && strcmpi(params.x, 'all')
        x = height(data);
    else
        x = min(str2double(params.x), height(data));
    end

    if ~ismember('spectrum', data.Properties.VariableNames)
        data.spectrum = repmat({''}, height(data), 1);
    end
    if ~ismember('computation_time', data.Properties.VariableNames)
        data.computation_time = zeros(height(data), 1);
    end

    if ~ismember('ppm', data.Properties.VariableNames)
        data.ppm = repmat({''}, height(data), 1);
    end


    % ========================= Loop over rows =========================
    disp("Beginning Loop")
    for row = 1:x
        t_start = tic;
        try
            disp("------------------- Molecule: -------------------")
            disp(data.Name(row))

            %fieldStrength
            fieldStrength = data.FieldStrength(row);
            fieldStrength_Tesla = MHz_to_Tesla(fieldStrength); % +- 100, 200
            sys.magnet = fieldStrength_Tesla;
            fprintf("fieldStrength Tesla: \n%s\n", fieldStrength_Tesla);

            % Spin matrix
            spin_matrix_str = data.spin_matrix{row};
            spin_matrix = str2num(spin_matrix_str);  %#ok<ST2NM>
            if isempty(spin_matrix)
                warning("Row %d: spin_matrix is empty after parsing.", row);
            end

            % N_spins
            n_spins = int32(data.n_spins(row));
            disp("------------------- nspins -------------------")
            disp(n_spins)
    
            % ========================= Spin system setup =========================
            sys.isotopes = repmat({'1H'}, 1, n_spins);
    
            % Chemical shifts in ppm
            inter.zeeman.scalar = num2cell(diag(spin_matrix));
            
            % Coupling matrix (off-diagonal, in Hz)
            inter.coupling.scalar = getCouplingMatrix(spin_matrix, n_spins);
    
            % ========================= Basis set =========================
            bas.formalism = params.formalism;
            bas.approximation = params.approx;
            if contains(params.approx, 'IK')
                bas.level = params.approx_level;
            end
            if contains(params.approx, 'IK-1')
                bas.connectivity='scalar_couplings';
                bas.space_level=2;
            end
            if contains(params.approx, 'IK-2')
                bas.connectivity='scalar_couplings';
                bas.space_level=2;
            end
           
    
            % ========================= Setup Spin System =========================
            spin_system = create(sys, inter);
            spin_system = basis(spin_system, bas);

            % ========================= Simulation parameters =========================
            [sweep, offset] = calc_plotWindow(params.windowSize_ppm, params.offset_ppm, fieldStrength);

            parameters.sweep = sweep;
            parameters.npoints = params.npoints;
            parameters.offset = offset;
            parameters.spins = {'1H'};
            parameters.axis_units = 'ppm';
            parameters.rho0 = state(spin_system, 'L+', '1H'); % aquire.m -> evolution.m -> human2opspec.m
            parameters.coil = state(spin_system, 'L+', '1H'); % aquire.m -> evolution.m -> human2opspec.m

            % ========================= Generate FID and Fourier transform it =========================   
            fid = liquid(spin_system, @acquire, parameters, 'nmr');
            fid = apodisation(spin_system, fid, {{params.apodisation, params.apodisation_level}});
    
            spectrum = fftshift(fft(fid));
            spectrum = real(spectrum);
            spectrum = spectrum - min(spectrum);   
            spectrum = spectrum / max(spectrum);

            % Generate ppm vector
            ppm_vector = linspace(params.offset_ppm, params.offset_ppm + params.windowSize_ppm, params.npoints);
            ppm_string = mat2str(ppm_vector);
            ppm_str = strcat('"', ppm_string, '"');
            data.ppm{row} = ppm_str;

    
            % ========================= Save spectrum data =========================
            spectrum_string = mat2str(spectrum);
            spectrum_str = strcat('"', spectrum_string, '"');
            data.spectrum{row} = spectrum_str;

            if ismember('Name', data.Properties.VariableNames)
                spectrum_title = data.Name{row};
                title(['1D NMR Spectrum: ', spectrum_title]);
            else
                title(['1D NMR Spectrum - Row ', num2str(row)]);
            end

        catch ME
            warning('Error processing row %d: %s', row, ME.message);
            data.spectrum{row} = '';
            data.computation_time(row) = NaN;
        end

        % ========================= computation time =========================
        data.computation_time(row) = toc(t_start);
    end

    % Restore double quotes around spin_matrix values before saving for
    % correct .csv readability
    for i = 1:height(data)
        if ischar(data.spin_matrix{i}) || isstring(data.spin_matrix{i})
            val = char(data.spin_matrix{i});
            % Only add quotes if not already present
            if ~(startsWith(val, '"') && endsWith(val, '"'))
                data.spin_matrix{i} = ['"', val, '"'];
            end
        end
    end
    
    % ========================= Save new .csv =========================
    csv_filename = sprintf('%s_generatedSpectra.csv', timestamp);
    json_filename = sprintf('%s_metadata.json', timestamp);

    output_filename = fullfile(pwd, csv_filename);
    metadata_path = fullfile(pwd, json_filename);

    writetable(data, output_filename, 'QuoteStrings', 'all');
    
    json_text = jsonencode(params);
    file = fopen(metadata_path, 'w');
    if file == -1
        error('Could not create metadata file.');
    end
    fwrite(file, json_text, 'char');
    fclose(file);
    done = "done";



end

