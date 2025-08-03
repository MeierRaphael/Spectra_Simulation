def count_peaks(spectra):
    ascending=True
    before=spectra[0]
    n_peaks=0
    i=0
    for spectrum in spectra:
        i=i+1
        if ascending:
            if spectrum>=before-0.01:
                before=spectrum
            else:
                #print(f"peak found: {i/len(spectra) *120 -10}")
                before=spectrum
                n_peaks=n_peaks+1
                ascending=False
        else:
            if spectrum<=before+0.01:
                before=spectrum
            else:
                before=spectrum
                ascending=True
    return n_peaks