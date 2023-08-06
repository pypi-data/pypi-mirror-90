import io
import os
import subprocess
import tempfile

import jinja2

# =============================================================================
def generate_outfile(
        templatesdir,
        templatename,
        context,
        outfilename,
        log = None,
        cachedir = None,
        ):

    # Template rendering
    # -------------------------------------------------------------------------
    log.info("Generating SVG using '{}' template".format(templatename))
    log.debug("Context : {}".format(context))

    log.debug(
            "Initializing jinja2 with template dir '{}'" \
                    .format(templatesdir)
                    )
    jj2_env = jinja2.Environment(
            loader = jinja2.FileSystemLoader(
                str(templatesdir),
                )
            )

    try:
        jj2_tpl = jj2_env.get_template(
                # Jinja specific path format
                "{}/template.svg.j2".format(templatename),
                )
    except Exception as e:
        log.error("Could not find template '{}'".format(templatename))
        log.debug(e, exc_info=1)
        return None

    # To SVG
    # -------------------------------------------------------------------------
    if outfilename.suffix == ".svg":
        jj2_tpl.stream(context).dump( str(outfilename) )
        return outfilename

    # To PNG with inkscape
    # -------------------------------------------------------------------------
    if outfilename.suffix == ".png":

        cachedir.mkdir(parents=True, exist_ok=True)

        tmpsvg = tempfile.NamedTemporaryFile(
                suffix=".svg",
                mode = "w",
                delete = False,
                dir = str(cachedir),
                )
        tmpsvg.close()
        try:
            log.info(
                    "Exporting to {} using inkscape" \
                            .format(outfilename.suffix),
                            )
            import subprocess

            jj2_tpl.stream(context).dump( tmpsvg.name )

            inkscape_process = subprocess.Popen(
                    [
                        "inkscape",
                        tmpsvg.name,
                        "--export-filename",
                        str(outfilename),
                        ],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT,
                    universal_newlines = True,
                    )

            for line_out in iter(inkscape_process.stdout.readline, ""):
                log.debug(line_out)

            inkscape_process.stdout.close()

            rv = inkscape_process.wait()

            if rv != 0:
                raise Exception(
                        "Bad inkscape return code '{}'" \
                                .format(inkscape_process.returncode)
                                )


            return outfilename

        except Exception as e:
            log.warning("Failed to export with inkscape")
            log.debug(e, exc_info=True)

        finally:
            os.unlink(tmpsvg.name)

    # To png, pdf or ps with cairosvg
    # -------------------------------------------------------------------------
    if outfilename.suffix in [ ".png", ".pdf", ".ps" ]:

        log.info("Exporting to {} using cairosvg".format(outfilename.suffix))

        try:
            import cairosvg
        except ImportError as e:
            log.error(
                    "Failed to export to '{}' with cairosvg" \
                            .format(
                                outfilename,
                                )
                            )
            log.debug(e)

        else:
            svg_str = jj2_tpl.render(context)

            if outfilename.suffix == ".png":
                conversion_fun = cairosvg.svg2png
            elif outfilename.suffix == ".pdf":
                conversion_fun = cairosvg.svg2pdf
            elif outfilename.suffix == ".ps":
                conversion_fun = cairosvg.svg2ps

            conversion_fun(
                bytestring = svg_str,
                write_to = str(outfilename),
                )

            return outfilename

    # To unsupported format
    # -------------------------------------------------------------------------
    log.error(
            "Can't export to '{}' : unsupported format '{}'" \
                    .format(
                        outfilename,
                        outfilename.suffix,
                        )
                    )
    return None

# =============================================================================
def generate_pic(
        templatesdir,
        templatename,
        context,
        outform="svg",
        log = None,
        cachedir = None,
        ):

    if outform not in ["svg", "png"]:
        raise ValueError("unsupported output format '{}'".format(outform))

    # Template rendering
    # -------------------------------------------------------------------------
    log.info("Generating SVG using '{}' template".format(templatename))
    log.debug("Context : {}".format(context))

    log.debug(
            "Initializing jinja2 with template dir '{}'" \
                    .format(templatesdir)
                    )
    jj2_env = jinja2.Environment(
            loader = jinja2.FileSystemLoader(
                str(templatesdir),
                )
            )

    try:
        jj2_tpl = jj2_env.get_template(
                # Jinja specific path format
                "{}/template.svg.j2".format(templatename),
                )
    except jinja2.exceptions.TemplateNotFound as e:
        raise e
    except Exception as e:
        log.error("Could not find template '{}'".format(templatename))
        log.debug(e, exc_info=1)
        return None

    # To SVG
    # -------------------------------------------------------------------------
    if outform == "svg":
        return jj2_tpl.render(context)

    # To PNG with inkscape
    # -------------------------------------------------------------------------
    if outform == "png":

        if cachedir is None:
            cachedir_tmp = tempfile.TemporaryDirectory()
            cachedir = cachedir_tmp.name
        else:
            cachedir.mkdir(parents=True, exist_ok=True)

        tmpsvg = tempfile.NamedTemporaryFile(
                suffix=".svg",
                mode = "w",
                delete = False,
                dir = str(cachedir),
                )
        tmpsvg.close()
        tmppng = tempfile.NamedTemporaryFile(
                suffix = ".png",
                mode = "w",
                delete = False,
                dir = str(cachedir),
                )
        tmppng.close()
        try:
            log.info(
                    "Exporting to {} using inkscape" \
                            .format(outform),
                            )
            import subprocess

            jj2_tpl.stream(context).dump( tmpsvg.name )

            inkscape_process = subprocess.Popen(
                    [
                        "inkscape",
                        tmpsvg.name,
                        "--export-filename",
                        tmppng.name,
                        ],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT,
                    universal_newlines = True,
                    )

            for line_out in iter(inkscape_process.stdout.readline, ""):
                log.debug(line_out)

            inkscape_process.stdout.close()

            rv = inkscape_process.wait()

            if rv != 0:
                raise Exception(
                        "Bad inkscape return code '{}'" \
                                .format(inkscape_process.returncode)
                                )

            with open(tmppng.name, "rb") as fh:
                buf = io.BytesIO(fh.read())

            return buf

        except Exception as e:
            log.warning("Failed to export with inkscape")
            log.debug(e, exc_info=True)

        finally:
            os.unlink(tmpsvg.name)
            os.unlink(tmppng.name)

            try:
                cachedir_tmp.cleanup()
            except:
                pass

        return None
