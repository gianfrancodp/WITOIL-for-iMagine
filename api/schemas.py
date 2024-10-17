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
            "description": "Name of the simulation. If None or "", default name is used.",
        },
        load_default="syria",
    )
        
    start_datetime = fields.String(
        metadata={
            "description": "Start date of the simulation.",
        },
        load_default="",
    )
    sim_length = fields.Float(
        metadata={
            "description": "Length of the simulation in hours.",
        },
        load_default=48.0,
    )
    
    time_step = fields.Integer(
        metadata={
            "description": "Simulation time step in seconds.",
        },
        load_default=1800,
    )
    
    spill_lat = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(max=5),
        metadata={
            "description": "List of latitudes of the oil spill.",
        },
        load_default=[33],
    )
    
    spill_lon = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(max=5),
        metadata={
            "description": "List of longitudes of the oil spill.",
        },
        load_default=[33],
    )
    
    spill_duration = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(max=5),
        metadata={
            "description": "List of durations of the oil spill in hours. 0 for instantaneous release.",
        },
        load_default=[0.0],
    )
    
    spill_rate = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(max=5),
        metadata={
            "description": "List of spill rates in tons per hour.",
        },
        load_default=[100.5],
    )
    
    slick_age = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(max=5),
        metadata={
            "description": "List of ages of the oil slick in hours.",
        },
        load_default=[0.0],
    )
    
    oil = fields.List(
        cls_or_instance=fields.String,
        validate=validate.Length(max=5),
        metadata={
            "description": "List of either API of the oil or names. Names must be exact.",
        },
        load_default=[28],
    )

    preproc_path = fields.String(
        metadata={
            "description": "Where preprocessed MET/OCE data should be placed.",
        },
        load_default="cases/",
    )
    
    set_domain = fields.Boolean(
        metadata={
            "description": "Whether to set the domain.",
        },
        load_default=False,
    )
    
    delta = fields.List(
        cls_or_instance=fields.Float,
        validate=validate.Length(max=5),
        metadata={
            "description": "Default distance in degrees to download or crop data if lat and lon areas are not provided.",
        },
        load_default=[0.75],
    )
    
    lat = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "List of latitude values.",
        },
        load_default=[39, 41],
    )
    
    lon = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "List of longitude values.",
        },
        load_default=[17, 19.5],
    )
    
    define_boundaries = fields.Boolean(
        metadata={
            "description": "Whether to define boundaries for plotting.",
        },
        load_default=False,
    )
    
    plot_lon = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "Longitudinal boundaries for plotting.",
        },
        load_default=[-64.1, -63.5],
    )
    
    plot_lat = fields.List(
        cls_or_instance=fields.Float,
        metadata={
            "description": "Latitudinal boundaries for plotting.",
        },
        load_default=[10.6, 11],
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
