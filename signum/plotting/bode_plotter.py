import numpy as np
import matplotlib.pyplot as plt

from signum import SignalContainer, TimeDomainSignal
from signum.plotting.plotter import Plotter


class BodePlotter(Plotter):
    def __init__(self, figsize=(8, 6), db_scale: bool = False, rad: bool = False, unwrapped: bool = False, **kwargs):
        super().__init__(n_rows=2, n_cols=1, figsize=figsize, **kwargs)

        self.amplitude_ax.set_ylabel(f"Amplitude{' [db]' if db_scale else ''}")
        self.phase_ax.set_ylabel(f"Phase [{'rad' if rad else 'deg'}]")

        self._db_scale = db_scale
        self._rad = rad
        self._unwrapped = unwrapped

    @property
    def amplitude_ax(self) -> plt.Axes:
        return self.axes[0, 0]

    @property
    def phase_ax(self) -> plt.Axes:
        return self.axes[1, 0]

    def add_line(self, signal: SignalContainer, add_legend=True, **kwargs):
        if signal.description and 'label' not in kwargs:
            kwargs['label'] = signal.description

        mag = signal.magnitude_db if self._db_scale else signal.magnitude
        amplitude_line, = self.amplitude_ax.plot(signal.x_axis, mag.T, **kwargs)

        phase = signal.get_phase(rad=self._rad, unwrapped=self._unwrapped)
        phase_line, = self.phase_ax.plot(signal.x_axis, phase.T, **kwargs)

        if add_legend and 'label' in kwargs:
            self.add_legend()

        return amplitude_line, phase_line


if __name__ == '__main__':
    s1 = TimeDomainSignal(np.random.rand(10) + 1j * np.random.rand(10), f_sampling=2, description='Random data')

    x = np.arange(-3, 3, 0.1)
    s2 = TimeDomainSignal(x**2/2 - 2, description="x^2", x_axis=x)

    plot = BodePlotter(title='Bode plot', unwrapped=True, rad=True)
    plot.add_line(s1, marker='d')
    plot.add_line(s2, color='crimson', label='Square func')
    plot.show_all()
