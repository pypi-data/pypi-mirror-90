import numpy
import sys

from PyQt5.QtGui import QPalette, QColor, QFont

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence
from oasys.util.oasys_util import TriggerIn, EmittingStream

from orangecontrib.wofry.util.wofry_objects import WofryData
from orangecontrib.wofry.widgets.gui.ow_wofry_widget import WofryWidget
from orangecontrib.wofry.widgets.gui.python_script import PythonScript

from syned.widget.widget_decorator import WidgetDecorator

from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D

from orangecontrib.wofry.als.util.axo_fit_profile import axo_fit_profile
import os
import orangecanvas.resources as resources
from scipy import interpolate

class OWCorrector1D(WofryWidget):

    name = "Corrector (reflector) 1D"
    id = "WofryCorrectorByReflection1D"
    description = "ALS Corrector (reflector) 1D"
    icon = "icons/eyeglasses.png"
    priority = 5

    category = "Wofry Wavefront Propagation"
    keywords = ["data", "file", "load", "read"]

    outputs = [{"name":"WofryData",
                "type":WofryData,
                "doc":"WofryData",
                "id":"WofryData"},
               {"name": "DABAM 1D Profile",
                "type": numpy.ndarray,
                "doc": "numpy.ndarray",
                "id": "numpy.ndarray"},
               {"name":"Trigger",
                "type": TriggerIn,
                "doc":"Feedback signal to start a new beam simulation",
                "id":"Trigger"}]

    inputs = [("WofryData", WofryData, "set_input"),
              ("GenericWavefront1D", GenericWavefront1D, "set_input"),
              WidgetDecorator.syned_input_data()[0]]

    correction_method = Setting(1)
    grazing_angle = Setting(1.5e-3)
    focus_at = Setting(10.0)
    apodization = Setting(0)
    apodization_ratio = Setting(0.1)
    apply_correction_to_wavefront = Setting(0)
    write_correction_profile = Setting(0)
    file_correction_profile = Setting("correction_profile1D.dat")
    write_input_wavefront = Setting(0)



    input_data = None
    titles = ["Wavefront (input) 1D Intensity", "Wavefront (input) 1D Phase", "Wavefront (target) 1D Phase", "Correction Profile"]

    def __init__(self):
        super().__init__(is_automatic=True, show_view_options=True)

        #
        # add script tab to tabs panel
        #
        script_tab = oasysgui.createTabPage(self.main_tabs, "Script")
        self.wofry_script = PythonScript()
        self.wofry_script.code_area.setFixedHeight(400)
        script_box = gui.widgetBox(script_tab, "Python script", addSpace=True, orientation="horizontal")
        script_box.layout().addWidget(self.wofry_script)


        #
        # build control panel
        #

        button_box = oasysgui.widgetBox(self.controlArea, "", addSpace=False, orientation="horizontal")

        button = gui.button(button_box, self, "Propagate Wavefront", callback=self.propagate_wavefront)
        font = QFont(button.font())
        font.setBold(True)
        button.setFont(font)
        palette = QPalette(button.palette()) # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('Dark Blue'))
        button.setPalette(palette) # assign new palette
        button.setFixedHeight(45)

        gui.separator(self.controlArea)

        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        tabs_setting.setFixedHeight(self.TABS_AREA_HEIGHT + 50)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        self.tab_sou = oasysgui.createTabPage(tabs_setting, "Generic Corrector 1D Settings")

        box_corrector = oasysgui.widgetBox(self.tab_sou, "Reflector", addSpace=False, orientation="vertical")


        gui.comboBox(box_corrector, self, "correction_method", label="Correction type", labelWidth=350,
                     items=["None","Focus to waist with reflector"],
                     callback=self.set_visible,
                     sendSelectedValue=False, orientation="horizontal")


        self.box_corrector_1 = oasysgui.widgetBox(box_corrector, "", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(self.box_corrector_1, self, "grazing_angle", "Grazing angle [rad]",
                          labelWidth=300, valueType=float, orientation="horizontal")

        oasysgui.widgetBox(self.box_corrector_1, "", addSpace=False, orientation="horizontal")
        oasysgui.lineEdit(self.box_corrector_1, self, "focus_at", "Distance to waist [m]",
                          labelWidth=300, valueType=float, orientation="horizontal")

        gui.comboBox(self.box_corrector_1, self, "apodization", label="Modify correction profile", labelWidth=350,
                     items=["No","Apodization with intensity","Apodization with Gaussian",
                            "JTEC-AXO fit (extrapolated)","JTEC-AXO fit (cropped)"],
                     sendSelectedValue=False, orientation="horizontal",callback=self.set_visible)
        self.apodization_ratio_id = oasysgui.widgetBox(self.box_corrector_1, "", addSpace=False, orientation="horizontal")
        oasysgui.lineEdit(self.apodization_ratio_id, self, "apodization_ratio", "Apodization sigma/window ratio",
                          labelWidth=300, valueType=float, orientation="horizontal")

        gui.comboBox(self.box_corrector_1, self, "apply_correction_to_wavefront", label="Apply correction to wavefront", labelWidth=350,
                     items=["No","Yes"],
                     sendSelectedValue=False, orientation="horizontal")

        gui.comboBox(self.box_corrector_1, self, "write_correction_profile", label="Correction profile to file", labelWidth=350,
                     items=["No","Yes"], sendSelectedValue=False, orientation="horizontal",
                     callback=self.set_visible)

        #
        self.box_file_out = oasysgui.widgetBox(self.box_corrector_1, "", addSpace=False, orientation="vertical")
        oasysgui.lineEdit(self.box_file_out, self, "file_correction_profile", "Correction profile file",
                            labelWidth=200, valueType=str, orientation="horizontal")
        # self.show_at("self.write_correction_profile == 1", self.box_file_out)

        #



        gui.comboBox(self.box_corrector_1, self, "write_input_wavefront", label="Input wf to file (for script)", labelWidth=350,
                     items=["No","Yes [wavefront_input.h5]"], sendSelectedValue=False, orientation="horizontal")


        self.file_box_id = oasysgui.widgetBox(self.box_corrector_1, "", addSpace=True, orientation="horizontal", width=400, height=35)


        self.set_visible()

    def set_visible(self):
        if self.correction_method == 0:
            self.box_corrector_1.setVisible(False)
        else:
            self.box_corrector_1.setVisible(True)

            if self.apodization == 2:
                self.apodization_ratio_id.setVisible(True)
            else:
                self.apodization_ratio_id.setVisible(False)

        self.box_file_out.setVisible(self.write_correction_profile == 1)

    def initializeTabs(self):
        size = len(self.tab)
        indexes = range(0, size)

        for index in indexes:
            self.tabs.removeTab(size-1-index)

        self.tab = []
        self.plot_canvas = []

        for index in range(0, len(self.titles)):
            self.tab.append(gui.createTabPage(self.tabs, self.titles[index]))
            self.plot_canvas.append(None)

        for tab in self.tab:
            tab.setFixedHeight(self.IMAGE_HEIGHT)
            tab.setFixedWidth(self.IMAGE_WIDTH)

    def check_fields(self):
        self.grazing_angle = congruence.checkStrictlyPositiveNumber(self.grazing_angle, "Grazing angle")
        self.focus_at = congruence.checkStrictlyPositiveNumber(numpy.abs(self.focus_at), "Distance to waist")
        self.apodization_ratio = congruence.checkStrictlyPositiveNumber(numpy.abs(self.apodization_ratio), "Apodzation radio")

    def receive_syned_data(self):
        raise Exception(NotImplementedError)

    def set_input(self, wofry_data):
        if not wofry_data is None:
            if isinstance(wofry_data, WofryData):
                self.input_data = wofry_data
            else:
                self.input_data = WofryData(wavefront=wofry_data)

            if self.is_automatic_execution:
                self.propagate_wavefront()

    def propagate_wavefront(self):
        self.progressBarInit()

        self.wofry_output.setText("")
        sys.stdout = EmittingStream(textWritten=self.writeStdOut)

        self.check_fields()

        if self.input_data is None: raise Exception("No Input Wavefront")

        input_wavefront = self.input_data.get_wavefront()

        if self.write_correction_profile == 0:
            file_correction_profile = ""
        else:
            file_correction_profile = self.file_correction_profile

        if self.correction_method == 0: # no correction
            output_wavefront = input_wavefront.duplicate()
            target_wavefront = input_wavefront.duplicate()
            abscissas_on_mirror = target_wavefront.get_abscissas()
            height = numpy.zeros_like(abscissas_on_mirror)
        else:
            output_wavefront, target_wavefront, abscissas_on_mirror, height = self.calculate_output_wavefront_after_corrector1D(
                    input_wavefront,
                    grazing_angle=self.grazing_angle,
                    focus_at=self.focus_at,
                    apodization=self.apodization,
                    apodization_ratio=self.apodization_ratio,
                    file_correction_profile=file_correction_profile)

        self.progressBarSet(50)
        if self.view_type > 0:
            self.do_plot_wavefront(output_wavefront, target_wavefront, abscissas_on_mirror, height)



        if self.write_input_wavefront:
            self.input_data.get_wavefront().save_h5_file("wavefront_input.h5",subgroupname="wfr",intensity=True,phase=True,
                                          overwrite=True,verbose=True)

        # script
        dict_parameters = {"grazing_angle": self.grazing_angle,
                           "focus_at": self.focus_at,
                           "focus_at":self.focus_at,
                           "apodization": self.apodization,
                           "apodization_ratio":self.apodization_ratio,
                           "file_correction_profile":file_correction_profile}

        script_template = self.script_template_output_wavefront_after_correction1D()
        self.wofry_script.set_code(script_template.format_map(dict_parameters))

        self.progressBarFinished()

        # send data
        dabam_profile = numpy.zeros((height.size, 2))
        dabam_profile[:, 0] = abscissas_on_mirror
        dabam_profile[:, 1] = height
        self.send("DABAM 1D Profile", dabam_profile)


        beamline = self.input_data.get_beamline().duplicate() # TODO add element here
        if self.apply_correction_to_wavefront == 0:
            self.send("WofryData", WofryData(beamline=beamline, wavefront=input_wavefront.duplicate()))
        else:
            self.send("WofryData", WofryData(beamline=beamline, wavefront=output_wavefront))
        self.send("Trigger", TriggerIn(new_object=True))







    @classmethod
    def calculate_output_wavefront_after_corrector1D(cls, input_wavefront,grazing_angle=1.5e-3, focus_at=10.0,
                                                     apodization=0, apodization_ratio=0.1, file_correction_profile=""):

        output_wavefront = input_wavefront.duplicate()
        target_wavefront = input_wavefront.duplicate()
        target_wavefront.set_spherical_wave(radius=-focus_at, center=0.0, complex_amplitude=1.0)

        phase_input = input_wavefront.get_phase(unwrap=True)
        phase_target = target_wavefront.get_phase(unwrap=True)
        phase_correction = phase_target - phase_input
        abscissas = target_wavefront.get_abscissas()
        abscissas_on_mirror = abscissas / numpy.sin(grazing_angle)

        # output_wavefront.add_phase_shift(phase_correction)
        height = - phase_correction / (2 * output_wavefront.get_wavenumber() * numpy.sin(grazing_angle))

        if apodization == 0:
            height -= height[height.size // 2]
        elif apodization == 1:
            apodization = input_wavefront.get_intensity()
            apodization = (apodization / apodization.max())
            height *= apodization
            height -= height[0]
        elif apodization == 2:
            sigma = numpy.abs(abscissas[-1] - abscissas[0]) * apodization_ratio
            apodization = numpy.exp( - abscissas**2 / 2 / sigma**2)
            apodization /= apodization.max()
            height *= apodization
            height -= height[0]
        elif apodization >= 3: # JTEC AXOs

            f = open("tmp_profile.dat","w")
            for i in range(height.size):
                f.write("%g %g\n"%(abscissas_on_mirror[i],height[i]))
            f.close()
            print("Ideal correction profile written to file: tmp_profile.dat" )

            file_influence = os.path.join(resources.package_dirname("orangecontrib.wofry.als.util"), "data",
                                                  "aps_axo_influence_functions2019.dat")
            file_orthonormal = os.path.join(resources.package_dirname("orangecontrib.wofry.als.util"), "data",
                                                    "aps_axo_orthonormal_functions2019.dat")

            coeffs, abscissas, interpolated, fitted = axo_fit_profile("tmp_profile.dat",
                                                                      fileout="",
                                                                      file_influence_functions=file_influence,
                                                                      file_orthonormal_functions=file_orthonormal,
                                                                      calculate=False)

            # plot(abscissas_on_mirror, height,
            #      1e-3 * abscissas, fitted, legend=["Ideal","Fitted"])

            if apodization == 3:
                f = interpolate.interp1d(1e-3 * abscissas, fitted, fill_value="extrapolate")
            elif apodization == 4:
                f = interpolate.interp1d(1e-3 * abscissas, fitted, fill_value=(0,0),bounds_error=False)
                output_wavefront.clip(1e-3 * abscissas[0] * numpy.sin(grazing_angle), 1e-3 * abscissas[-1] * numpy.sin(grazing_angle))

            height = f(abscissas_on_mirror)
            # plot(abscissas_on_mirror, height,
            #      1e-3 * abscissas, fitted, legend=["Extrapolated or Cropped","Fitted"])
        # calculate phase shift from new profile
        phi = -2 * output_wavefront.get_wavenumber() * height * numpy.sin(grazing_angle)
        output_wavefront.add_phase_shift(phi)

        # output files
        if file_correction_profile != "":
            f = open(file_correction_profile,"w")
            if apodization <= 2:
                for i in range(height.size):
                    f.write("%g %g\n"%(abscissas_on_mirror[i],height[i]))
            else:
                for i in range(fitted.size):
                    f.write("%g %g\n" % (1e-3 * abscissas[i], fitted[i]))
            f.close()
            print("File written to disk: %s " % file_correction_profile)

        return output_wavefront, target_wavefront, abscissas_on_mirror, height

    # warning: pay attention to the double backslash in \\n
    def script_template_output_wavefront_after_correction1D(self):
        return \
"""


def calculate_output_wavefront_after_corrector1D(input_wavefront,grazing_angle=1.5e-3, focus_at=10.0, apodization=0, apodization_ratio=0.1, file_correction_profile=""):
    import numpy
    from scipy import interpolate
    output_wavefront = input_wavefront.duplicate()
    target_wavefront = input_wavefront.duplicate()
    target_wavefront.set_spherical_wave(radius=-focus_at, center=0.0, complex_amplitude=1.0)

    phase_input = input_wavefront.get_phase(unwrap=True)
    phase_target = target_wavefront.get_phase(unwrap=True)
    phase_correction = phase_target - phase_input
    abscissas = target_wavefront.get_abscissas()
    abscissas_on_mirror = abscissas / numpy.sin(grazing_angle)

    # output_wavefront.add_phase_shift(phase_correction)
    height = - phase_correction / (2 * output_wavefront.get_wavenumber() * numpy.sin(grazing_angle))

    if apodization == 0:
        height -= height[height.size // 2]
    elif apodization == 1:
        apodization = input_wavefront.get_intensity()
        apodization = (apodization / apodization.max())
        height *= apodization
        height -= height[0]
    elif apodization == 2:
        sigma = numpy.abs(abscissas[-1] - abscissas[0]) * apodization_ratio
        apodization = numpy.exp( - abscissas**2 / 2 / sigma**2)
        apodization /= apodization.max()
        height *= apodization
        height -= height[0]
    elif apodization >= 3: # JTEC AXOs
        from orangecontrib.wofry.als.util.axo_fit_profile import axo_fit_profile
        import os
        import orangecanvas.resources as resources
        from scipy import interpolate
        
        f = open("tmp_profile.dat","w")
        for i in range(height.size):
            f.write("%g %g\\n"%(abscissas_on_mirror[i],height[i]))
        f.close()
        print("Ideal correction profile written to file: tmp_profile.dat" )

        file_influence = os.path.join(resources.package_dirname("orangecontrib.wofry.als.util"), "data",
                                              "aps_axo_influence_functions2019.dat")
        file_orthonormal = os.path.join(resources.package_dirname("orangecontrib.wofry.als.util"), "data",
                                                "aps_axo_orthonormal_functions2019.dat")

        coeffs, abscissas, interpolated, fitted = axo_fit_profile("tmp_profile.dat",
                                                                  fileout="",
                                                                  file_influence_functions=file_influence,
                                                                  file_orthonormal_functions=file_orthonormal,
                                                                  calculate=False)

        # plot(abscissas_on_mirror, height,
        #      1e-3 * abscissas, fitted, legend=["Ideal","Fitted"])

        if apodization == 3:
            f = interpolate.interp1d(1e-3 * abscissas, fitted, fill_value="extrapolate")
        elif apodization == 4:
            f = interpolate.interp1d(1e-3 * abscissas, fitted, fill_value=(0,0),bounds_error=False)
            output_wavefront.clip(1e-3 * abscissas[0] * numpy.sin(grazing_angle), 1e-3 * abscissas[-1] * numpy.sin(grazing_angle))

        height = f(abscissas_on_mirror)
        # plot(abscissas_on_mirror, height,
        #      1e-3 * abscissas, fitted, legend=["Extrapolated or Cropped","Fitted"])
    # calculate phase shift from new profile
    phi = -2 * output_wavefront.get_wavenumber() * height * numpy.sin(grazing_angle)
    output_wavefront.add_phase_shift(phi)

    # output files
    if file_correction_profile != "":
        f = open(file_correction_profile,"w")
        if apodization <= 2:
            for i in range(height.size):
                f.write("%g %g\\n"%(abscissas_on_mirror[i],height[i]))
        else:
            for i in range(fitted.size):
                f.write("%g %g\\n" % (1e-3 * abscissas[i], fitted[i]))
        f.close()
        print("File written to disk: %s " % file_correction_profile)

    return output_wavefront, target_wavefront, abscissas_on_mirror, height
#
# main
#
from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D
input_wavefront = GenericWavefront1D.load_h5_file("wavefront_input.h5","wfr")
output_wavefront, target_wavefront, abscissas_on_mirror, height = calculate_output_wavefront_after_corrector1D(input_wavefront,grazing_angle={grazing_angle}, focus_at={focus_at}, apodization={apodization}, apodization_ratio={apodization_ratio}, file_correction_profile="{file_correction_profile}")

from srxraylib.plot.gol import plot
plot(output_wavefront.get_abscissas(),output_wavefront.get_intensity())
"""

    def do_plot_results(self, progressBarValue): # required by parent
        pass

    def do_plot_wavefront(self, wavefront1D, target_wavefront, abscissas_on_mirror, height, progressBarValue=80):
        if not self.input_data is None:

            self.progressBarSet(progressBarValue)


            self.plot_data1D(x=1e6*wavefront1D.get_abscissas(),
                             y=wavefront1D.get_intensity(),
                             progressBarValue=progressBarValue,
                             tabs_canvas_index=0,
                             plot_canvas_index=0,
                             calculate_fwhm=True,
                             title=self.titles[0],
                             xtitle="Spatial Coordinate [$\mu$m]",
                             ytitle="Intensity")

            self.plot_data1D(x=1e6*wavefront1D.get_abscissas(),
                             y=wavefront1D.get_phase(unwrap=True, from_minimum_intensity=0.1),
                             progressBarValue=progressBarValue + 10,
                             tabs_canvas_index=1,
                             plot_canvas_index=1,
                             calculate_fwhm=False,
                             title=self.titles[1],
                             xtitle="Spatial Coordinate [$\mu$m]",
                             ytitle="Phase [unwrapped] (rad)")

            self.plot_data1D(x=1e6*target_wavefront.get_abscissas(),
                             y=target_wavefront.get_phase(unwrap=True, from_minimum_intensity=0.1),
                             progressBarValue=progressBarValue + 10,
                             tabs_canvas_index=2,
                             plot_canvas_index=2,
                             calculate_fwhm=False,
                             title=self.titles[2],
                             xtitle="Spatial Coordinate [$\mu$m]",
                             ytitle="Phase of target wavefront [unwrapped] (rad)")

            self.plot_data1D(x=abscissas_on_mirror,
                             y=1e6*height,
                             progressBarValue=progressBarValue + 10,
                             tabs_canvas_index=3,
                             plot_canvas_index=3,
                             calculate_fwhm=False,
                             title=self.titles[3],
                             xtitle="Spatial Coordinate along o.e. [m]",
                             ytitle="Profile Height [$\mu$m]")

            self.plot_canvas[0].resetZoom()



if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication


    def create_wavefront():
        #
        # create input_wavefront
        #
        from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D
        input_wavefront = GenericWavefront1D.initialize_wavefront_from_range(x_min=-0.00147, x_max=0.00147,
                                                                             number_of_points=1000)
        input_wavefront.set_photon_energy(250)
        input_wavefront.set_spherical_wave(radius=13.73, center=0, complex_amplitude=complex(1, 0))
        return input_wavefront

    app = QApplication([])
    ow = OWCorrector1D()
    ow.set_input(create_wavefront())

    # ow.receive_dabam_profile(numpy.array([[1,2],[3,4]]))
    ow.propagate_wavefront()

    ow.show()
    app.exec_()
    ow.saveSettings()
