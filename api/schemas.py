"""Module for defining custom web fields to use on the API interface.
This module is used by the API server to generate the input form for the
prediction and training methods. You can use any of the defined schemas
to add new inputs to your API.

The module shows simple but efficient example schemas. However, you may
need to modify them for your needs.
"""

import marshmallow
from webargs import ValidationError, fields, validate

from . import config, responses, utils


class ModelName(fields.String):
    """Field that takes a string and validates against current available
    models at config.MODELS_PATH.
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if value not in utils.ls_dirs(config.MODELS_PATH):
            raise ValidationError(f"Checkpoint `{value}` not found.")
        return str(config.MODELS_PATH / value)


class Dataset(fields.String):
    """Field that takes a string and validates against current available
    data files at config.DATA_PATH.
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if value not in utils.ls_dirs(config.DATA_PATH):
            raise ValidationError(f"Dataset `{value}` not found.")
        return str(config.DATA_PATH / value)


# EXAMPLE of Prediction Args description
# = HAVE TO MODIFY FOR YOUR NEEDS =
class PredArgsSchema(marshmallow.Schema):
    """Prediction arguments schema for api.predict function."""

    class Meta:  # Keep order of the parameters as they are defined.
        # pylint: disable=missing-class-docstring
        # pylint: disable=too-few-public-methods
        ordered = True

    #    model_name = ModelName(
    #        metadata={
    #            "description": "String/Path identification for models.",
    #        },
    #        required=True,
    #    )
    #
    #    input_file = fields.Field(
    #        metadata={
    #            "description": "File with np.arrays for predictions.",
    #            "type": "file",
    #            "location": "form",
    #        },
    #        required=True,
    #    )
    #
    name = fields.String(
        metadata={
            "description": "Name of the simulation. If None or "
            ", default name is used.",
        },
        load_default="my_experiment",
    )

    start_datetime = fields.DateTime(
        metadata={
            "description": "Start date of the simulation in the format of YYYY-MM-DDTHH:MM:SS as this example 2021-08-21T03:43:00.",
        },
        # load_default="2021-08-21T03:43:00",
    )
    sim_length = fields.Float(
        metadata={
            "description": "Length of the simulation in hours.",
        },
        load_default=24.0,
    )

    spill_lat = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "List of latitudes of the oil spill (deg N).",
        },
        load_default=[35.25],
    )

    spill_lon = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "List of longitudes of the oil spill (deg E).",
        },
        load_default=[35.90],
    )

    spill_duration = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "List of durations of the oil spill in hours. 0.0 for instantaneous release.",
        },
        load_default=[0.0],
    )

    spill_rate = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "List of spill rates in tons per hour.",
        },
        load_default=[27.78],
    )

    slick_age = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "List of ages of the oil slick in hours.",
        },
        load_default=[0.0],
    )

    oil = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "List of either API (number) of the oil or names (string). Names must be exact.",
        },
        load_default=[28],
    )

    area_spill = fields.Boolean(
        metadata={
            "description": "Whether area or points should be used for the spill.",
        },
        load_default=False,
    )

    area_vertex = fields.Boolean(
        metadata={
            "description": "Comprehends three levels of lists. 1st: all slicks. 2nd: individual slick. 3rd: Coordinates of each vertex in each individual slick.",
        },
        load_default=False,
    )

    multiple_slick = fields.Boolean(
        metadata={
            "description": "Whether there are multiple slicks.",
        },
        load_default=False,
    )

    copernicus_user = fields.String(
        required=True,
        validate=validate.Length(min=1),
        metadata={
            "description": "User for downloading COPERNICUS data.",
        },
    )

    copernicus_password = fields.String(
        required=True,
        validate=validate.Length(min=1),
        load_only=True,
        metadata={
            "description": "Password for downloading COPERNICUS data.",
            "format": "password",
        },
    )

    cds_token = fields.String(
        required=True,
        validate=validate.Length(min=1),
        load_only=True,
        metadata={
            "description": "Token for downloading ERA5 data.",
            "format": "password",
        },
    )

    set_domain = fields.Boolean(
        metadata={
            "description": "Whether the user wants to set the domain for cropping/preprocessing input data.",
        },
        load_default=False,
    )

    lat = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "List of latitude values.",
        },
        load_default=[31, 38],
    )

    lon = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "List of longitude values.",
        },
        load_default=[32, 37],
    )

    delta = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(min=1, max=5),
        metadata={
            "description": "default domain length in degrees (applied to both lon/lat), to download or crop data. delta is used only if set_domain = false.",
        },
        load_default=[0.75],
    )

    plot_lon = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "Longitudinal boundaries for plotting.",
        },
        load_default=[35.5, 36.5],
    )

    plot_lat = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "Latitudinal boundaries for plotting.",
        },
        load_default=[35, 36],
    )

    accept = fields.String(
        metadata={
            "description": "Return format for method response.",
            "location": "headers",
        },
        required=True,
        validate=validate.OneOf(list(responses.content_types)),
    )


# EXAMPLE of Training Args description
# = HAVE TO MODIFY FOR YOUR NEEDS =
class TrainArgsSchema(marshmallow.Schema):
    """Training arguments schema for api.train function."""

    class Meta:  # Keep order of the parameters as they are defined.
        # pylint: disable=missing-class-docstring
        # pylint: disable=too-few-public-methods
        ordered = True

    model_name = ModelName(
        metadata={
            "description": "String/Path identification for models.",
        },
        required=True,
    )

    dataset = Dataset(
        metadata={
            "description": "Path to the training dataset.",
        },
        required=False,
    )

    epochs = fields.Integer(
        metadata={
            "description": "Number of epochs to train the model.",
        },
        required=False,
        load_default=1,
        validate=validate.Range(min=1),
    )
