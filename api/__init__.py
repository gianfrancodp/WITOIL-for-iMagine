"""Endpoint functions to integrate your model with the DEEPaaS API.

For more information about how to edit the module see, take a look at the
docs [1] and at a canonical exemplar module [2].

[1]: https://docs.ai4eosc.eu/
[2]: https://github.com/ai4os-hub/demo-advanced
"""
import logging

import toml
from . import interface as witoil

from . import config, responses, schemas, utils

import glob

import os

logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)


def get_metadata():
    """Returns a dictionary containing metadata information about the module.

    Raises:
        HTTPException: Unexpected errors aim to return 50X

    Returns:
        A dictionary containing metadata information required by DEEPaaS.
    """
    try:  # Call your AI model metadata() method
        logger.info("Collecting metadata from: %s", config.API_NAME)
        metadata = {
            "author": config.API_METADATA.get("authors"),
            "author-email": config.API_METADATA.get("author-emails"),
            "description": config.API_METADATA.get("summary"),
            "license": config.API_METADATA.get("license"),
            "version": config.API_METADATA.get("version"),
            "datasets": utils.ls_files(config.DATA_PATH, '[A-Za-z0-9]*'),
            "models": utils.ls_dirs(config.MODELS_PATH),
        }
        logger.debug("Package model metadata: %s", metadata)
        return metadata
    except Exception as err:
        logger.error("Error collecting metadata: %s", err, exc_info=True)
        raise  # Reraise the exception after log


@utils.predict_arguments(schema=schemas.PredArgsSchema)
def predict(**options):
    """Performs model prediction from given input data and parameters.

    Arguments:
        model_name -- Model name from registry to use for prediction values.
        input_file -- File with data to perform predictions from model.
        accept -- Response parser type, default is json.
        **options -- Arbitrary keyword arguments from PredArgsSchema.

    Raises:
        HTTPException: Unexpected errors aim to return 50X

    Returns:
        The predicted model values png, pdf or mp4 file.
    """

    logger.debug("Predict with args: %s", options)
    try:  # Call your AI model predict() method
        # Load config.toml and modify the user inputs
        tdata = toml.load("WITOIL_iMagine/config.toml")

        tdata['simulation']['name'] = options['name']
        tdata['simulation']['start_datetime'] = options['start_datetime']
        tdata['simulation']['sim_length'] = options['sim_length']
        tdata['simulation']['spill_lat'] = options['spill_lat']
        tdata['simulation']['spill_lon'] = options['spill_lon']
        tdata['simulation']['spill_duration'] = options['spill_duration']
        tdata['simulation']['spill_rate'] = options['spill_rate']
        tdata['simulation']['slick_age'] = options['slick_age']
        tdata['simulation']['oil'] = options['oil']
        tdata['simulation']['area_spill'] = options['area_spill']
        tdata['simulation']['area_vertex'] = options['area_vertex']
        tdata['simulation']['multiple_slick'] = options['multiple_slick']
        tdata['download']['copernicus_user'] = options['copernicus_user']
        tdata['download']['copernicus_password'] = options['copernicus_password']
        tdata['download']['cds_token'] = options['cds_token']
        tdata['input_files']['set_domain'] = options['set_domain']
        tdata['input_files']['lat'] = options['lat']
        tdata['input_files']['lon'] = options['lon']
        tdata['input_files']['delta'] = options['delta']
        tdata['plot_options']['plot_lon'] = options['plot_lon']
        tdata['plot_options']['plot_lat'] = options['plot_lat']

        conf = open("WITOIL_iMagine/config.toml",'w')
        toml.dump(tdata, conf)
        conf.close()

        witoil.main_run("WITOIL_iMagine/config.toml")
        result = "WITOIL_iMagine/cases/"+options['name']+"/out_files/figures/"

        logger.debug("Predict result: %s", result)

        logger.info(
                "Returning content_type for: %s", options["accept"]
            )

        return responses.png_response(result,**options)
    
    except Exception as err:(
        logger.error("Error calculating predictions: %s", err, exc_info=True))
    raise  # Reraise the exception after log

