function [sweep, offset] = calc_plotWindow(windowSize_ppm, offset_ppm, field_Strength)

sweep = windowSize_ppm * field_Strength;
offset = offset_ppm * field_Strength + sweep/2;

end

