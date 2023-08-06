import os
import sys
import io
import textwrap
import json
import tempfile
import coverxygen
import sphinx

config = None

def validate_config(app, __config):

    # Get the configuration
    global config

    try:
        config = __config.docscov_config
    except:
        raise sphinx.errors.ConfigError("'conf.py' must contain 'docscov_config' ('dict')")

    # Validate the configuration
    if type(config.get("xml_dir", None)) is not str:
        raise sphinx.errors.ConfigError("'docscov_config['xml_dir']' must be a 'str'")

    if config.get("root_dir", None) != None:
        if type(config.get("root_dir", None)) is not str:
            raise sphinx.errors.ConfigError("'docscov_config['root_dir']' must be a 'str'")
        elif not os.path.exists(config["root_dir"]) or not os.path.isdir(config["root_dir"]):
            raise sphinx.errors.ConfigError(
                "'docscov_config['root_dir']' must be contain a valid directory path"
            )
    else:
        config["root_dir"] = "."

    if config.get("badge_label", None) != None:
        if type(config.get("badge_label", None)) is not str:
            raise sphinx.errors.ConfigError("'docscov_config['badge_label']' must be a 'str'")
    else:
        config["badge_label"] = "docscov"

    if config.get("scope", None) != None:
        if type(config.get("scope", None)) is not list:
            raise sphinx.errors.ConfigError("'docscov_config['scope']' must be a 'list'")
    else:
        config["scope"] = ["all"]
    
    if config.get("kind", None) != None:
        if type(config.get("kind", None)) is not list:
            raise sphinx.errors.ConfigError("'docscov_config['kind']' must be a 'list'")
    else:
        config["kind"] = ["all"]

    # Setup config
    if "all" in config["scope"]:
        config["scope"] = [
            "private",
            "protected",
            "public"
        ]

    if "all" in config["kind"]:
        config["kind"] = [
            "class",
            "define",
            "enum",
            "enumvalue",
            "file",
            "friend",
            "function",
            "namespace",
            "page",
            "signal",
            "slot",
            "struct",
            "typedef",
            "union",
            "variable"
        ]

def write_coverage_data(app, *args):

    global config

    # Create temporary directory and setup Sphinx
    tmpdir = tempfile.mkdtemp()
    if type(app.config.html_static_path) is list:
        app.config.html_static_path.append(tmpdir)
    else:
        app.config.html_static_path = [app.config.html_static_path, tmpdir]

    # Setup coverxygen
    coverage = coverxygen.Coverxygen(
        config["xml_dir"],
        "-",
        config["scope"],
        config["kind"],
        "json-v3",
        config["root_dir"]
    )

    # Before processing Doxygen XML, setup to capture stdout
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    # Process Doxygen XML
    try:
        coverage.process()
    except:
        sys.stdout.seek(0)
        print(textwrap.dedent(f"""
            {{
                "total": {{
                    "coverage_rate": 0
                }}
            }}
        """)[1:])

    # Parse the output
    sys.stdout.seek(0)
    coverage_data = json.load(sys.stdout)

    # Revert to previous state
    sys.stdout = stdout

    # Coverage percentage
    coverage_percentage = coverage_data["total"]["coverage_rate"] * 100

    # Set the color of badge
    if coverage_percentage == 100:
        color = "brightgreen"
    elif coverage_percentage >= 95:
        color = "green"
    elif coverage_percentage >= 85:
        color = "yellowgreen"
    elif coverage_percentage >= 75:
        color = "yellow"
    elif coverage_percentage >= 60:
        color = "orange"
    else:
        color = "red"

    # Write to a json, which will be copied to HTML website
    open(f"{tmpdir}/docscov.json", "w").write(textwrap.dedent(f"""
        {{
            "schemaVersion": 1,
            "label": "{config["badge_label"]}",
            "message": "{round(coverage_percentage)}%",
            "color": "{color}"
        }}
    """)[1:]) # Don't write the leading new line

def setup(app):
    app.add_config_value("docscov_config", dict(), "")
    app.connect("config-inited", validate_config)
    app.connect("env-before-read-docs", write_coverage_data)
