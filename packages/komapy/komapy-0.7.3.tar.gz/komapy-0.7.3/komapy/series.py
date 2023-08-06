"""
KomaPy chart series.
"""

from collections import OrderedDict
from collections.abc import Callable
from functools import partial

from . import client, processing, transforms, utils
from .addons import addon_registers
from .constants import SUPPORTED_NAMES, SUPPORTED_TYPES
from .decorators import register_as_decorator
from .exceptions import ChartError
from .utils import get_validation_methods

DATA_SOURCES = OrderedDict([
    ('csv', {
        'resolver': processing.read_csv,
        'options': 'csv_params',
    }),
    ('json', {
        'resolver': processing.read_json,
        'options': 'json_params',
    }),
    ('excel', {
        'resolver': processing.read_excel,
        'options': 'excel_params',
    }),
    ('sql', {
        'resolver': processing.read_sql,
        'options': 'sql_params',
    }),
    ('url', {
        'resolver': client.fetch_url_as_dataframe,
        'options': 'query_params',
    }),
    ('name', {
        'resolver': client.fetch_bma_as_dataframe,
        'options': 'query_params',
    }),
])


@register_as_decorator
def register_addon(name, resolver, **kwargs):
    """
    Register add-on function.

    :param name: Name of addon register.
    :type name: str
    :param resolver: Addon callable resolver function.
    :type resolver: :class:`collections.Callable`
    """
    if not isinstance(resolver, Callable):
        raise ChartError('Add-on resolver must be callable')

    if name in addon_registers:
        raise ChartError(
            'Add-on {} already exists in the global register names. '
            'Use different name or use namespace prefix.'.format(name))

    addon_registers[name] = resolver


def unregister_addon(name):
    return addon_registers.pop(name, None)


class Series(object):
    """
    A series object.

    A series object in KomaPy holds information about series data, including
    plot type, plot data, data query parameters, axis locator, axis formatter,
    and many more. Here it is an example on how to create series instance:

    .. code-block:: python

        from komapy.series import Series

        series = Series(
            name='edm',
            query_params={
                'benchmark: 'BAB0',
                'reflector': 'RB2',
                'start_at': '2019-04-01',
                'end_at: '2019-08-01',
                'ci': True
            },
            plot_params={
                'color': 'k',
                'marker': 'o',
                'markersize': 6,
                'zorder': 2,
                'linewidth': 1,
                'label': 'RB2'
            },
            fields=['timestamp', 'slope_distance'],
            xaxis_date=True
        )

        series.validate()
        data = series.resolve_data()
    """

    required_parameters = ['fields']
    available_parameters = {
        'addons': [],
        'aggregations': [],
        'axis': None,
        'csv_params': {},
        'csv': None,
        'excel_params': {},
        'excel': None,
        'field_options': {},
        'fields': [],
        'formatter': {},
        'grid': {},
        'index': None,
        'json_params': {},
        'json': None,
        'labels': {},
        'legend': {},
        'locator': {},
        'merge_options': {},
        'name': None,
        'partial': [],
        'plot_params': {},
        'query_params': {},
        'secondary': None,
        'sql_params': {},
        'sql': [],
        'tertiary': {},
        'title': None,
        'transforms': [],
        'type': 'line',
        'url': None,
        'xaxis_date': False,
        'yaxis_date': False,
    }

    def __init__(self, **kwargs):
        for key, value in self.available_parameters.items():
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

        self._check_required_parameters(kwargs)

    def _check_required_parameters(self, kwargs):
        for param in self.required_parameters:
            if param not in kwargs:
                raise ChartError('Parameter {} is required'.format(param))

    def validate_name(self):
        """Validate name attribute."""
        if self.name:
            if self.name not in SUPPORTED_NAMES:
                raise ChartError('Unknown parameter name {}'.format(self.name))

    def validate_type(self):
        """Validate type attribute."""
        if self.type not in SUPPORTED_TYPES:
            raise ChartError('Unsupported plot type {}'.format(self.name))

    def validate_fields(self):
        """Validate fields attribute."""
        if not self.fields:
            raise ChartError('Series fields must be set')

    def validate(self):
        """Validate all config attributes."""
        validation_methods = get_validation_methods(Series)

        for method in validation_methods:
            getattr(self, method)()

    def get_dict_config(self):
        """
        Get series configurations as dictionary.
        """
        config = {}
        for key in self.available_parameters.keys():
            config[key] = getattr(self, key)
        return config

    def fetch_resource(self, **kwargs):
        """
        Fetch series resource.

        Series resource is resolved in the following order, CSV, JSON URL, and
        BMA API name. If none of the sources found in the chart series
        configuration, it returns None.

        :return: :class:`pandas.DataFrame` object if using CSV, JSON URL, or
                 BMA API name. Otherwise, it returns None.
        """

        def get_resource(config_dict):
            for name in DATA_SOURCES:
                source = config_dict.get(name)
                if source:
                    resolve_fn = DATA_SOURCES[name]['resolver']
                    options = config_dict.get(
                        DATA_SOURCES[name]['options'], {})

                    if isinstance(source, list):
                        return resolve_fn(*source, **options)
                    return resolve_fn(source, **options)
            return None

        if self.partial:
            data_containers = []
            for config_dict in self.partial:
                data_containers.append(get_resource(config_dict))

            # Merge all resource data.
            merge_options = {
                'ignore_index': True,
                'sort': True
            }
            merge_options.update(self.merge_options)
            return processing.merge_dataframe(data_containers, **merge_options)

        return get_resource(self.get_dict_config())

    def resolve_data(self, **kwargs):
        """
        Resolve plot data.

        Plot data is resolved in the following order, CSV, JSON URL, and BMA API
        name. Each of sources has certain resolver. If none of the sources found
        in the chart series, data source is treated as plain object.

        :return: A list of resolved plot data whose type of
                 :class:`pandas.DataFrame` if using CSV, JSON URL, or BMA API
                 name. Otherwise, it returns native object.
        :rtype: list of :class:`pandas.DataFrame` or native object
        """
        if kwargs.get('resource') is not None:
            resource = kwargs.get('resource')
        else:
            resource = self.fetch_resource(**kwargs)

        if resource is not None:
            func = partial(processing.dataframe_or_empty, resource)
            iterator = map(func, self.fields)
        else:
            iterator = self.fields

        plot_data = []
        for i, field in enumerate(iterator):
            if i == 0 and self.xaxis_date:
                plot_data.append(utils.resolve_timestamp(field))
            elif i == 1 and self.yaxis_date:
                plot_data.append(utils.resolve_timestamp(field))
            else:
                plot_data.append(field)

        if self.aggregations:
            for item in self.aggregations:
                func = item.get('func')
                if func is None:
                    raise ChartError(
                        'Function name or callable must be set '
                        'if using data aggregations')

                agg_field = item.get('field')
                if agg_field is None:
                    raise ChartError('Field name must be set '
                                     'if using data aggregations')
                if resource is not None:
                    index = self.fields.index(agg_field)
                else:
                    index = agg_field

                params = item.get('params', {})

                if isinstance(func, str):
                    if func not in processing.supported_aggregations:
                        continue

                    resolver = processing.supported_aggregations[func]
                    if isinstance(resolver, str):
                        callback = getattr(processing, resolver)
                    elif isinstance(resolver, Callable):
                        callback = resolver
                    plot_data[index] = callback(plot_data[index], params)

                elif isinstance(func, Callable):
                    plot_data[index] = callback(plot_data[index], params)

        if self.transforms:
            for item in self.transforms:
                if isinstance(item, str):
                    if item not in transforms.transform_registers:
                        continue

                    resolver = transforms.transform_registers[item]
                    if isinstance(resolver, str):
                        callback = getattr(transforms, resolver)
                    elif isinstance(resolver, Callable):
                        callback = resolver
                    plot_data = callback(plot_data, self)

                elif isinstance(item, Callable):
                    plot_data = callback(plot_data, self)

        return plot_data
