class PerPrintPressureAdvance:
    def __init__(self, config):
        self.printer = config.get_printer()
        gcode = self.printer.lookup_object("gcode")
        gcode.register_command(
            "SET_PRINT_PRESSURE_ADVANCE",
            self.cmd_SET_PRINT_PRESSURE_ADVANCE,
            desc=self.cmd_SET_PRINT_PRESSURE_ADVANCE_help,
        )

    cmd_SET_PRINT_PRESSURE_ADVANCE_help = (
        "Set pressure advance automatically, or based on provided nozzle sizes"
    )

    def cmd_SET_PRINT_PRESSURE_ADVANCE(self, gcmd):
        nozzle_size = gcmd.get("NOZZLE", parser=str, default=None)
        if nozzle_size == None:
            gcmd.respond_info(
                "SET_PRINT_PRESSURE_ADVANCE called, but no NOZZLE argument provided"
            )
            return

        # Pressure advance
        if nozzle_size == "0.2":
            pa = 0.9
        elif nozzle_size == "0.3":
            pa = 0.8
        elif nozzle_size == "0.4":
            pa = 0.7
        elif nozzle_size == "0.5":
            pa = 0.6
        elif nozzle_size == "0.6":
            pa = 0.5
        else:
            gcmd.respond_info(
                "SET_PRINT_PRESSURE_ADVANCE called with unsupported NOZZLE {nozzle}".format(
                    nozzle=nozzle_size
                )
            )
            return

        smoothing = 0.02

        extruder = self.printer.lookup_object("toolhead").get_extruder()
        extruder.extruder_stepper._set_pressure_advance(pa, smoothing)


def load_config(config):
    return PerPrintPressureAdvance(config)