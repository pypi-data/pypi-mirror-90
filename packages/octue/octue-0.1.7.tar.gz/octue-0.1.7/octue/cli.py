import os
import sys
import click
import pkg_resources

from octue.definitions import FOLDER_DEFAULTS, MANIFEST_FILENAME, VALUES_FILENAME
from octue.logging_handlers import get_remote_handler
from octue.runner import Runner


global_cli_context = {}


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--id",
    default=None,
    type=click.UUID,
    show_default=True,
    help="UUID of the analysis being undertaken. None (for local use) will cause a unique ID to be generated.",
)
@click.option(
    "--skip-checks/--no-skip-checks",
    default=False,
    is_flag=True,
    show_default=True,
    help="Skips the input checking. This can be a timesaver if you already checked "
    "data directories (especially if manifests are large).",
)
@click.option("--logger-uri", default=None, show_default=True, help="Stream logs to a websocket at the given URI.")
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error"], case_sensitive=False),
    show_default=True,
    help="Log level used for the analysis.",
)
@click.option(
    "--force-reset/--no-force-reset",
    default=True,
    is_flag=True,
    show_default=True,
    help="Forces a reset of analysis cache and outputs [For future use, currently not implemented]",
)
@click.version_option(version=pkg_resources.get_distribution("octue").version)
def octue_cli(id, skip_checks, logger_uri, log_level, force_reset):
    """ Octue CLI, enabling a data service / digital twin to be run like a command line application.

    When acting in CLI mode, results are read from and written to disk (see
    https://octue-python-sdk.readthedocs.io/en/latest/ for how to run your application directly without the CLI).
    Once your application has run, you'll be able to find output values and manifest in your specified --output-dir.
    """
    global_cli_context["analysis_id"] = id
    global_cli_context["skip_checks"] = skip_checks
    global_cli_context["logger_uri"] = logger_uri
    global_cli_context["log_level"] = log_level.upper()
    global_cli_context["force_reset"] = force_reset


@octue_cli.command()
@click.option(
    "--app-dir",
    type=click.Path(),
    default=".",
    show_default=True,
    help="Directory containing your source code (app.py)",
)
@click.option(
    "--data-dir",
    type=click.Path(),
    default=".",
    show_default=True,
    help="Location of directories containing configuration values and manifest, input values and manifest, and output "
    "directory.",
)
@click.option(
    "--config-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory containing configuration (overrides --data-dir).",
)
@click.option(
    "--input-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory containing input (overrides --data-dir).",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory to write outputs as files (overrides --data-dir).",
)
@click.option("--twine", type=click.Path(), default="twine.json", show_default=True, help="Location of Twine file.")
def run(app_dir, data_dir, config_dir, input_dir, output_dir, twine):
    config_dir = config_dir or os.path.join(data_dir, FOLDER_DEFAULTS["configuration"])
    input_dir = input_dir or os.path.join(data_dir, FOLDER_DEFAULTS["input"])
    output_dir = output_dir or os.path.join(data_dir, FOLDER_DEFAULTS["output"])

    runner = Runner(
        twine=twine,
        configuration_values=os.path.join(config_dir, VALUES_FILENAME),
        configuration_manifest=os.path.join(config_dir, MANIFEST_FILENAME),
        log_level=global_cli_context["log_level"],
    )

    if global_cli_context["logger_uri"]:
        handler = get_remote_handler(
            logger_uri=global_cli_context["logger_uri"], log_level=global_cli_context["log_level"]
        )
    else:
        handler = None

    analysis = runner.run(
        app_src=app_dir,
        analysis_id=global_cli_context["analysis_id"],
        handler=handler,
        input_values=os.path.join(input_dir, VALUES_FILENAME),
        input_manifest=os.path.join(input_dir, MANIFEST_FILENAME),
        output_manifest_path=os.path.join(output_dir, MANIFEST_FILENAME),
        skip_checks=global_cli_context["skip_checks"],
    )
    analysis.finalise(output_dir=output_dir)
    return 0


if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    octue_cli(args)
