import logging
import math
import threading
from datetime import datetime
import time
from typing import Tuple

from astropy.io import fits

from pyobs.interfaces import ICamera, ICameraWindow, ICameraBinning, ICooling
from pyobs.modules.camera.basecamera import BaseCamera
from .flidriver import *


log = logging.getLogger(__name__)


class FliCamera(BaseCamera, ICamera, ICameraWindow, ICameraBinning, ICooling):
    """A pyobs module for FLI cameras."""

    def __init__(self, setpoint: float = -20, *args, **kwargs):
        """Initializes a new FliCamera.

        Args:
            setpoint: Cooling temperature setpoint.
        """
        BaseCamera.__init__(self, *args, **kwargs)

        # variables
        self._driver = None
        self._temp_setpoint = setpoint

        # window and binning
        self._window = None
        self._binning = None

    def open(self):
        """Open module."""
        BaseCamera.open(self)

        # list devices
        devices = FliDriver.list_devices()
        if len(devices) == 0:
            raise ValueError('No camera found.')

        # open first one
        d = devices[0]
        log.info('Opening connection to "%s" at %s...', d.name.decode('utf-8'), d.filename.decode('utf-8'))
        self._driver = FliDriver(d)
        try:
            self._driver.open()
        except ValueError as e:
            raise ValueError('Could not open FLI camera: %s', e)

        # get window and binning from camera
        self._window, self._binning = self._driver.get_window_binning()

        # set cooling
        self.set_cooling(True, self._temp_setpoint)

    def close(self):
        """Close the module."""
        BaseCamera.close(self)

        # not open?
        if self._driver is not None:
            # close connection
            self._driver.close()
            self._driver = None

    def get_full_frame(self, *args, **kwargs) -> Tuple[int, int, int, int]:
        """Returns full size of CCD.

        Returns:
            Tuple with left, top, width, and height set.
        """
        return self._driver.get_full_frame()

    def get_window(self, *args, **kwargs) -> Tuple[int, int, int, int]:
        """Returns the camera window.

        Returns:
            Tuple with left, top, width, and height set.
        """
        return self._window

    def get_binning(self, *args, **kwargs) -> Tuple[int, int]:
        """Returns the camera binning.

        Returns:
            Tuple with x and y.
        """
        return self._binning

    def set_window(self, left: float, top: float, width: float, height: float, *args, **kwargs):
        """Set the camera window.

        Args:
            left: X offset of window.
            top: Y offset of window.
            width: Width of window.
            height: Height of window.

        Raises:
            ValueError: If binning could not be set.
        """
        self._window = (left, top, width, height)
        log.info('Setting window to %dx%d at %d,%d...', width, height, left, top)

    def set_binning(self, x: int, y: int, *args, **kwargs):
        """Set the camera binning.

        Args:
            x: X binning.
            y: Y binning.

        Raises:
            ValueError: If binning could not be set.
        """
        self._binning = (x, y)
        log.info('Setting binning to %dx%d...', x, y)

    def _expose(self, exposure_time: int, open_shutter: bool, abort_event: threading.Event) -> fits.PrimaryHDU:
        """Actually do the exposure, should be implemented by derived classes.

        Args:
            exposure_time: The requested exposure time in ms.
            open_shutter: Whether or not to open the shutter.
            abort_event: Event that gets triggered when exposure should be aborted.

        Returns:
            The actual image.
        """

        # set binning
        log.info("Set binning to %dx%d.", self._binning[0], self._binning[1])
        self._driver.set_binning(*self._binning)

        # set window, divide width/height by binning, from libfli:
        # "Note that the given lower-right coordinate must take into account the horizontal and
        # vertical bin factor settings, but the upper-left coordinate is absolute."
        width = int(math.floor(self._window[2]) / self._binning[0])
        height = int(math.floor(self._window[3]) / self._binning[1])
        log.info("Set window to %dx%d (binned %dx%d) at %d,%d.",
                 self._window[2], self._window[3], width, height,
                 self._window[0], self._window[1])
        self._driver.set_window(self._window[0], self._window[1], width, height)

        # set some stuff
        self._change_exposure_status(ICamera.ExposureStatus.EXPOSING)
        self._driver.init_exposure(open_shutter)
        self._driver.set_exposure_time(int(exposure_time))

        # get date obs
        log.info('Starting exposure with %s shutter for %.2f seconds...',
                 'open' if open_shutter else 'closed', exposure_time / 1000.)
        date_obs = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

        # do exposure
        self._driver.start_exposure()

        # wait for exposure to finish
        while True:
            # aborted?
            if abort_event.is_set():
                self._change_exposure_status(ICamera.ExposureStatus.IDLE)
                raise ValueError('Aborted exposure.')

            # is exposure finished?
            if self._driver.is_exposing():
                break
            else:
                # sleep a little
                time.sleep(0.2)

        # readout
        log.info('Exposure finished, reading out...')
        self._change_exposure_status(ICamera.ExposureStatus.READOUT)
        width = int(math.floor(self._window[2] / self._binning[0]))
        height = int(math.floor(self._window[3] / self._binning[1]))
        img = np.zeros((height, width), dtype=np.uint16)
        for row in range(height):
            img[row, :] = self._driver.grab_row(width)

        # create FITS image and set header
        hdu = fits.PrimaryHDU(img)
        hdu.header['DATE-OBS'] = (date_obs, 'Date and time of start of exposure')
        hdu.header['EXPTIME'] = (exposure_time / 1000., 'Exposure time [s]')
        hdu.header['DET-TEMP'] = (self._driver.get_temp(FliTemperature.CCD), 'CCD temperature [C]')
        hdu.header['DET-COOL'] = (self._driver.get_cooler_power(), 'Cooler power [percent]')
        hdu.header['DET-TSET'] = (self._temp_setpoint, 'Cooler setpoint [C]')

        # instrument and detector
        hdu.header['INSTRUME'] = (self._driver.name, 'Name of instrument')

        # binning
        hdu.header['XBINNING'] = hdu.header['DET-BIN1'] = (self._binning[0], 'Binning factor used on X axis')
        hdu.header['YBINNING'] = hdu.header['DET-BIN2'] = (self._binning[1], 'Binning factor used on Y axis')

        # window
        hdu.header['XORGSUBF'] = (self._window[0], 'Subframe origin on X axis')
        hdu.header['YORGSUBF'] = (self._window[1], 'Subframe origin on Y axis')

        # statistics
        hdu.header['DATAMIN'] = (float(np.min(img)), 'Minimum data value')
        hdu.header['DATAMAX'] = (float(np.max(img)), 'Maximum data value')
        hdu.header['DATAMEAN'] = (float(np.mean(img)), 'Mean data value')

        # biassec/trimsec
        full = self._driver.get_visible_frame()
        self.set_biassec_trimsec(hdu.header, *full)

        # return FITS image
        log.info('Readout finished.')
        self._change_exposure_status(ICamera.ExposureStatus.IDLE)
        return hdu

    def _abort_exposure(self):
        """Abort the running exposure. Should be implemented by derived class.

        Raises:
            ValueError: If an error occured.
        """
        self._driver.cancel_exposure()
        self._camera_status = ICamera.ExposureStatus.IDLE

    def get_cooling_status(self, *args, **kwargs) -> Tuple[bool, float, float]:
        """Returns the current status for the cooling.

        Returns:
            Tuple containing:
                Enabled (bool):         Whether the cooling is enabled
                SetPoint (float):       Setpoint for the cooling in celsius.
                Power (float):          Current cooling power in percent or None.
        """
        enabled = self._temp_setpoint is not None
        return enabled, self._temp_setpoint, self._driver.get_cooler_power()

    def get_temperatures(self, *args, **kwargs) -> dict:
        """Returns all temperatures measured by this module.

        Returns:
            Dict containing temperatures.
        """
        return {
            'CCD': self._driver.get_temp(FliTemperature.CCD),
            'Base': self._driver.get_temp(FliTemperature.BASE)
        }

    def set_cooling(self, enabled: bool, setpoint: float, *args, **kwargs):
        """Enables/disables cooling and sets setpoint.

        Args:
            enabled: Enable or disable cooling.
            setpoint: Setpoint in celsius for the cooling.

        Raises:
            ValueError: If cooling could not be set.
        """

        # log
        if enabled:
            log.info('Enabling cooling with a setpoint of %.2f°C...', setpoint)
        else:
            log.info('Disabling cooling and setting setpoint to 20°C...')

        # if not enabled, set setpoint to None
        self._temp_setpoint = setpoint if enabled else None

        # set setpoint
        self._driver.set_temperature(float(setpoint) if setpoint is not None else 20.)


__all__ = ['FliCamera']
