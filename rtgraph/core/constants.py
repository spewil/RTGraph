from enum import Enum


class SourceType(Enum):
    """
    Enum for the types of sources. Indices MUST match app_sources constant.
    """
    SocketServer = 0
    SocketClient = 1
    serial = 2
    simulator = 3


class Constants:
    """
    Common constants for the application.
    """
    app_title = "RTGraph"
    app_version = '0.3.1'
    app_export_path = "data"
    app_sources = ["SocketServer", "SocketClient", "Serial", "Simulator"]
    app_encoding = "utf-8"

    plot_update_ms = 8  # 60Hz
    plot_xlabel_title = "Time"
    plot_xlabel_unit = "s"
    plot_colors = [
        '#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee',
        '#a2142f', '#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30',
        '#4dbeee', '#a2142f', '#0072bd', '#d95319', '#edb120', '#7e2f8e',
        '#77ac30', '#4dbeee', '#a2142f', '#0072bd', '#d95319', '#edb120',
        '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f', '#0072bd', '#d95319',
        '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f', '#0072bd',
        '#d95319', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f',
        '#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee',
        '#a2142f', '#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30',
        '#4dbeee', '#a2142f', '#0072bd', '#d95319', '#edb120', '#7e2f8e',
        '#77ac30', '#4dbeee', '#a2142f', '#0072bd'
    ]
    plot_max_lines = len(plot_colors)

    process_join_timeout_ms = 1000

    argument_default_samples = 500

    serial_default_speed = 115200
    serial_timeout_ms = 0.5

    class SocketServer:
        timeout = 0.01
        host_default = "tcp://localhost"
        port_default = [45454]
        buffer_recv_size = 2048

    class SocketClient:
        timeout = 0.01
        host_default = "localhost"
        port_default = [45454]
        buffer_recv_size = 2048

    simulator_default_speed = 0.002

    csv_default_filename = "%Y-%m-%d_%H-%M-%S"
    csv_delimiter = ","
    csv_extension = "csv"

    parser_timeout_ms = 0.005

    log_filename = "{}.log".format(app_title)
    log_max_bytes = 5120
    log_default_level = 0
    log_default_console_log = False


class MinimalPython:
    """
    Specifies the minimal Python version required.
    """
    major = 3
    minor = 2
    release = 0
