from cmath import nan
from io import BytesIO
from typing import Dict, List

import PIL.Image as Image
from pandas import DataFrame
from rpy2.robjects import NULL as r_NULL
from rpy2.robjects import conversion, default_converter, packages, pandas2ri
from rpy2.robjects.vectors import StrVector


def climatic_summary(
    data: DataFrame,
    date_time: str,
    station: str = None,
    elements: List = [],
    year=None,
    month=None,
    dekad=None,
    pentad=None,
    to: str = "hourly",
    by=None,
    doy=None,
    doy_first=1,
    doy_last=366,
    summaries: Dict = {"n": "dplyr::n"},
    na_rm=False,
    na_prop=None,
    na_n=None,
    na_consec=None,
    na_n_non=None,
    first_date=False,
    n_dates=False,
    last_date=False,
    summaries_params: List = [],
    names="{.fn}_{.col}",
) -> DataFrame:
    """'to' parameter must be one of ("hourly", "daily", "pentad", "dekadal", 
                                    "monthly", "annual-within-year", 
                                    "annual", "longterm-monthly", 
                                    "longterm-within-year", "station",
                                    "overall")"""

    #  convert Python objects to R objects:
    with conversion.localconverter(default_converter + pandas2ri.converter):
        r_data = conversion.py2rpy(data)

    r_summaries = StrVector(list(summaries.values()))
    r_summaries.names = list(summaries.keys())

    station = r_NULL if station is None else station
    na_prop = r_NULL if na_prop is None else na_prop

    # execute R function
    r_cdms_products = packages.importr("cdms.products")
    r_data_returned = r_cdms_products.climatic_summary(
        data=r_data,
        date_time=date_time,
        station=station,
        elements=StrVector(elements),
        to=to,
        summaries=r_summaries,
        na_rm=na_rm,
        na_prop=na_prop,
    )

    # convert R data frame to pandas data frame
    with conversion.localconverter(default_converter + pandas2ri.converter):
        data_returned = conversion.rpy2py(r_data_returned)

    return data_returned


def timeseries_plot(
    path: str,
    file_name: str,
    data: DataFrame,
    date_time: str,
    elements: str,
    station: str = None,
    facet_by: str = "stations",
    type: str = "line",
    add_points: bool = False,
    add_line_of_best_fit: bool = False,
    se: bool = True,
    add_path: bool = False,
    add_step: bool = False,
    na_rm: bool = False,
    show_legend: bool = nan,
    title: str = "Timeseries Plot", 
    x_title:str = None, y_title:str = None
):
    # TODO ensure show_legend nan converted to R NA
    # TODO this function returns a ggplot2 object. How can we convert this into a type that is useful in Python and JS?
    # TODO `facet_by` must be one of ("stations", "elements", "stations-elements", "elements-stations", "none")
    # TODO `type` must be one of ("line", "bar")

    station = r_NULL if station is None else station
    x_title = r_NULL if x_title is None else x_title
    y_title = r_NULL if y_title is None else y_title
    with conversion.localconverter(default_converter + pandas2ri.converter):
        r_data = conversion.py2rpy(data)

    r_cdms_products = packages.importr("cdms.products")
    r_plot = r_cdms_products.timeseries_plot(
        data=r_data,
        date_time=date_time,
        elements=elements,
        station=station,
        facet_by=facet_by,
    )

    r_ggplot2 = packages.importr("ggplot2")
    r_ggplot2.ggsave(filename=file_name, plot=r_plot, device="jpeg", path=path)


def export_geoclim_month(
    data: DataFrame,
    year,
    month,
    element: str,
    station_id,
    latitude,
    longitude,
    metadata=None,
    join_by=None,
    add_cols=None,
    file_path: str = None,
    **kwargs
) -> str:
    # TODO if file_path is None then set it to "GEOCLIM-" + element + ".csv"
    # TODO convert `kwargs`` to R parameters
    pass
