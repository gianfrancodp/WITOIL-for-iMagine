"""Module for defining custom API response parsers and content types.
This module is used by the API server to convert the output of the requested
method into the desired format. 

The module shows simple but efficient example functions. However, you may
need to modify them for your needs.
"""
import io
import logging

from fpdf import FPDF

from . import config

logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)


# EXAMPLE of json_response parser function
# = HAVE TO MODIFY FOR YOUR NEEDS =
def json_response(result, **options):
    """Converts the prediction results into json return format.

    Arguments:
        result -- Result value from call, expected either dict or str
          (see https://docs.deep-hybrid-datacloud.eu/projects/deepaas/en/stable/user/v2-api.html).
        options -- Not used, added for illustration purpose.

    Raises:
        RuntimeError: Unsupported response type.

    Returns:
        Converted result into json dictionary format.
    """
    logger.debug("Response result type: %d", type(result))
    logger.debug("Response result: %d", result)
    logger.debug("Response options: %d", options)
    try:
        if isinstance(result, (dict, list, str)):
            return result
        # if isinstance(result, np.ndarray):
        #     return result.tolist()
        return dict(result)
    except Exception as err:  # TODO: Fix to specific exception
        logger.warning("Error converting result to json: %s", err)
        raise RuntimeError("Unsupported response type") from err


# EXAMPLE of pdf_response parser function
# = HAVE TO MODIFY FOR YOUR NEEDS =
def pdf_response(result, **options):
    """Converts the prediction results into pdf return format.

    Arguments:
        result -- Result value from call, expected either dict or str
          (see https://docs.deep-hybrid-datacloud.eu/projects/deepaas/en/stable/user/v2-api.html).
        options -- Not used, added for illustration purpose.

    Raises:
        RuntimeError: Unsupported response type.

    Returns:
        Converted result into pdf buffer format.
    """
    logger.debug("Response result type: %d", type(result))
    logger.debug("Response result: %d", result)
    logger.debug("Response options: %d", options)
    try:
        # 1. create BytesIO object
        buffer = io.BytesIO()
        buffer.name = "output.pdf"
        # 2. write the output of the method in the buffer
        #    For the proper PDF document, you may use:
        #    * matplotlib for images
        #    * fPDF2 for text documents (pip3 install fPDF2)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        # in this EXAMPLE we also add input parameters
        print_out = {"input": str(options), "predictions": str(result)}
        pdf.multi_cell(w=0, txt=str(print_out).replace(",", ",\n"))
        pdf_output = pdf.output(dest="S")
        buffer.write(pdf_output)
        # 3. rewind buffer to the beginning
        buffer.seek(0)
        return buffer
    except Exception as err:  # TODO: Fix to specific exception
        logger.warning("Error converting result to pdf: %s", err)
        raise RuntimeError("Unsupported response type") from err


def png_response(results, **options):
    logger.debug("Response result type: %d", type(results))
    logger.debug("Response result: %d", results)
    logger.debug("Response options: %d", options)
    try:
        for result in results[0]:
            # this will return a numpy array with the labels
            result = result.plot(
                labels=options["show_labels"],
                conf=options["show_conf"],
                boxes=options["show_boxes"],
                font_size=6.0,
            )
            success, buffer = cv2.imencode(".png", result)
            if not success:
                return "Error encoding image", 500

            # Create a BytesIO object and write the buffer into it
            image_buffer = BytesIO(buffer)

        return image_buffer
    except Exception as err:  # TODO: Fix to specific exception
        logger.warning("Error converting result to png: %s", err)
        raise RuntimeError("Unsupported response type") from err


def mp4_response(results, **options):
    """Converts the prediction or training results into
    mp4 return format.

    Arguments:
        result -- Result value from call, expected either dict or str
        options -- Not used, added for illustration purpose.

    Raises:
        RuntimeError: Unsupported response type.

    Returns:
        Converted result into mp4 buffer format.
    """
    # Process MP4 video response
    logger.debug("Response result type: %d", type(results))
    logger.debug("Response result: %d", results)
    logger.debug("Response options: %d", options)
    new_results = []
    for result in results[0]:
        # this will return a numpy array with the labels
        new_results.append(
            result.plot(
                labels=options["show_labels"],
                conf=options["show_conf"],
                boxes=options["show_boxes"],
            )
        )
    message = create_video_in_buffer(new_results)
    return message

content_types = {
#    "application/json": json_response,
#    "application/pdf": pdf_response,
    "image/png": png_response,
    "video/mp4": mp4_response,
}
