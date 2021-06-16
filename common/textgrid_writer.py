import textgrid

def __separate_intervals(y, inoise):
    breakpoints = __get_breakpoints(inoise)
    is_signal = True
    start_point = 0
    for bp in breakpoints:
        yield is_signal, start_point, bp
        start_point = bp
        is_signal = not is_signal
    yield is_signal, start_point, len(y)


def __get_breakpoints(inoise):
    expected = inoise[0] + 1
    yield inoise[0]
    for i in inoise[1:]:
        if i != expected:
            yield expected
            yield i
        expected = i + 1

def add_tier(tg, y, sr, inoise, name, signal_name, non_signal_name):
    tier = textgrid.IntervalTier(name=name, maxTime=len(y)/sr)
    intervals = __separate_intervals(y, inoise)
    for is_signal, imin, imax in intervals:
        time_min, time_max = imin / sr, imax / sr
        if time_min == time_max:
            continue

        mark = signal_name if is_signal else non_signal_name
        tier.addInterval(textgrid.Interval(minTime=time_min, maxTime=time_max, mark=mark))
    
    tg.append(tier)

def audio_to_textgrid(y, sr, inoise, inoise_pre=None) -> textgrid.TextGrid:
    '''
        Converts a piece of audio into a praat's textgrid format.
    '''
    max_time = len(y) / sr
    tg = textgrid.TextGrid(maxTime=max_time)

    if inoise_pre is not None:
        add_tier(tg, y, sr, inoise_pre, 'resultado sem filtro', 'alto', 'baixo')

    add_tier(tg, y, sr, inoise, 'resultado com filtro de maioria booleana', 'locucao', 'pausa')
    return tg


def write_textgrid_to_file(filename: str, audio_filename: str, tg: textgrid.TextGrid):
    ''' write a textgrid to a file. '''
    tg.name = audio_filename
    with open(filename, 'w') as f:
        tg.write(f)