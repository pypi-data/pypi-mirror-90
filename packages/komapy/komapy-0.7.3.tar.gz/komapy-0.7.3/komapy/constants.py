"""
KomaPy contants.
"""
import datetime

TIME_ZONE = 'Asia/Jakarta'

SUPPORTED_NAMES = [
    'bulletin',
    'doas',
    'doas2',
    'edm',
    'energy',
    'gas_emission',
    'gas_temperature',
    'gps_baseline',
    'gps_position',
    'magnitude',
    'meteorology',
    'rainfall',
    'rsam_infrasound_band',
    'rsam_infrasound',
    'rsam_seismic_band',
    'rsam_seismic',
    'seismicity',
    'slope',
    'thermal',
    'thermal2',
    'tiltborehole',
    'tiltmeter_raw',
    'tiltmeter_tlr',
    'tiltmeter',
    'topo',
    'users',
    'windrose',
]

SUPPORTED_TYPES = {
    # Basic plotting
    'line': 'plot',
    'plot': 'plot',
    'errorbar': 'errorbar',
    'scatter': 'scatter',
    'plot_date': 'plot_date',
    'step': 'step',
    'log': 'loglog',
    'loglog': 'loglog',
    'semilogx': 'semilogx',
    'semilogy': 'semilogy',
    'bar': 'bar',
    'barh': 'barh',
    'stem': 'stem',
    'eventplot': 'eventplot',
    'fill_between': 'fill_between',

    # Spectral plotting
    'acorr': 'acorr',
    'angle_spectrum': 'angle_spectrum',
    'cohere': 'cohere',
    'csd': 'csd',
    'magnitude_spectrum': 'magnitude_spectrum',
    'phase_spectrum': 'phase_spectrum',
    'psd': 'psd',
    'specgram': 'specgram',
    'xcorr': 'xcorr',
}

SUPPORTED_CUSTOMIZERS = {
    # Appearance
    'showgrid': 'grid',
    'axis_off': 'set_axis_off',
    'axis_on': 'set_axis_on',
    'frame': 'set_frame_on',
    'axis_below': 'set_axisbelow',
    'facecolor': 'set_facecolor',

    # Property cycle
    'prop_cycle': 'set_prop_cycle',

    # Axis limits and direction
    'invert_xaxis': 'invert_xaxis',
    'invert_yaxis': 'invert_yaxis',
    'xlimit': 'set_xlim',
    'ylimit': 'set_ylim',
    'xbound': 'set_xbound',
    'ybound': 'set_ybound',

    # Axis labels, title, legends
    'xlabel': 'set_xlabel',
    'ylabel': 'set_ylabel',

    # Axis scales
    'xscale': 'set_xscale',
    'yscale': 'set_yscale',

    # Autoscaling and margins
    'margins': 'margins',
    'xmargin': 'set_xmargin',
    'ymargin': 'set_ymargin',
    'relim': 'relim',
    'autoscale': 'autoscale',
    'autoscale_view': 'autoscale_view',
    'autoscale_on': 'set_autoscale_on',
    'autoscalex_on': 'set_autoscalex_on',
    'autoscaley_on': 'set_autoscaley_on',

    # Aspect ratio
    'aspect': 'set_aspect',
    'adjustable': 'set_adjustable',

    # Ticks and tick labels
    'xticks': 'set_xticks',
    'xticklabels': 'set_xticklabels',
    'yticks': 'set_yticks',
    'yticklabels': 'set_yticklabels',
    'minorticks_off': 'minorticks_off',
    'minorticks_on': 'minorticks_on',
    'ticklabel_format': 'ticklabel_format',
    'tick_params': 'tick_params',
    'locator_params': 'locator_params',

    # Axis position
    'ancor': 'set_anchor',
    'position': 'set_position',

    # Async/Event based
    'callback': 'add_callback',

    # General artist properties
    'agg_filter': 'set_agg_filter',
    'alpha': 'set_alpha',
    'animated': 'set_animated',
    'clip_on': 'set_clip_on',
    'gid': 'set_gid',
    'label': 'set_label',
    'rasterized': 'set_rasterized',
    'sketch_params': 'set_sketch_params',
    'snap': 'set_snap',
    'artist_url': 'set_url',
    'zorder': 'set_zorder',
}


def get_phase_dates():
    return [
        [datetime.datetime(2012, 7, 15), datetime.datetime(2018, 5, 11), ''],
        [datetime.datetime(2018, 5, 11), datetime.datetime(2018, 6, 1), 'II'],
        [datetime.datetime(2018, 6, 1),  datetime.datetime(2018, 7, 1), 'III'],
        [datetime.datetime(2018, 7, 1),  datetime.datetime(2018, 8, 12), 'IV'],
        [datetime.datetime(2018, 8, 12), datetime.datetime(2019, 1, 29), 'V'],
        [datetime.datetime(2019, 1, 29), datetime.datetime(2019, 9, 22), 'VI'],
        [datetime.datetime(2019, 9, 22), datetime.datetime.now(), 'VII'],
    ]
