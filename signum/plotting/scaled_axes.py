import numpy as np
import matplotlib.pyplot as plt
import logging

from signum.plotting.scaled_formatter import ScaledFormatter


_NOT_GIVEN_ = object()

logger = logging.getLogger(__name__)


class ScaledAxes:
    def __init__(self, ax: plt.Axes, x_unit='', y_unit='', x_label=None, y_label=None):
        if not isinstance(ax, plt.Axes):
            raise TypeError(f"Expected matplotlib.pyplot.Axes instance, got {type(ax)=}")

        self._ax = ax
        ax.xaxis.set_major_formatter(ScaledFormatter(x_unit))
        ax.yaxis.set_major_formatter(ScaledFormatter(y_unit))

        if x_label:
            self.set_xlabel(x_label)
        if y_label:
            self.xet_ylabel(y_label)

    def __getattr__(self, item):
        return getattr(self._ax, item)

    @property
    def ax(self):
        return self._ax

    @property
    def x_ax_formatter(self):
        return self.ax.xaxis.get_major_formatter()

    @property
    def y_ax_formatter(self):
        return self.ax.yaxis.get_major_formatter()

    def get_x_unit(self):
        return self.x_ax_formatter.base_unit

    def set_x_unit(self, x_unit):
        self.x_ax_formatter.base_unit = x_unit

    def get_y_unit(self):
        return self.y_ax_formatter.base_unit

    def set_y_unit(self, y_unit):
        self.y_ax_formatter.base_unit = y_unit

    def get_units(self):
        return self.get_x_unit(), self.get_y_unit()

    def set_units(self, x_unit, y_unit):
        self.set_x_unit(x_unit)
        self.set_y_unit(y_unit)

    def plot(self, *args, add_legend=True, **kwargs):
        if len(args) == 2:
            data, fmt = args
        elif len(args) == 1:
            data, = args
            fmt = None
        else:
            raise TypeError(f"Expected 1 or 2 positional arguments, got {len(args)}")

        try:
            x_data = data.x_axis
            y_data = data.view(np.ndarray)
            x_unit = data.x_unit
            y_unit = data.unit
        except AttributeError:
            raise TypeError(f"Expected a SignalContainer instance, got {type(data)}")

        self._fix_units(x_unit, y_unit)

        plot_args = (x_data, y_data, fmt) if fmt is not None else (x_data, y_data)
        lines = self.ax.plot(*plot_args, **kwargs)

        if add_legend and 'label' in kwargs:
            self.add_legend()

        return lines

    def add_legend(self, fancybox=True, framealpha=0.5, **kwargs):
        self.ax.legend(fancybox=fancybox, framealpha=framealpha, **kwargs)

    def _fix_units(self, data_x_unit, data_y_unit):
        data_units = {'x': data_x_unit, 'y': data_y_unit}

        for xy in 'xy':
            ax_unit = getattr(self, f'get_{xy}_unit')()
            data_unit = data_units[xy]
            if ax_unit:
                if ax_unit != data_unit:  # TODO: orders of magnitude
                    raise ValueError(f"{xy} units of the axes and data do not agree: {ax_unit=}, {data_unit=}")
            else:
                logger.debug(f"Setting {xy} unit of the axes to data {xy} unit: {data_unit}")
                getattr(self, f'set_{xy}_unit', data_unit)
