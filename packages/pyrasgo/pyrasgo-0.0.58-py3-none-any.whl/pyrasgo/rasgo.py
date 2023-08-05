from datetime import datetime
import pandas as pd
from types import FunctionType
from typing import Union, List, Optional, Dict
import yaml

from pyrasgo.connection import Connection
from pyrasgo.enums import Granularity, ModelType
from pyrasgo.feature import Feature, FeatureList
from pyrasgo.model import Model
from pyrasgo.monitoring import track_usage
from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse
from pyrasgo.utils import dataframe, ingestion
from pyrasgo import schemas as api


class Rasgo(Connection):
    """
    Base connection object to handle interactions with the Rasgo API.
    """
    from pyrasgo.version import __version__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()


# ---------
# Get Calls
# ---------
    @track_usage
    def get_column(self, column_id: int) -> api.Column:
        """
        Returns a Column with the specified id
        """
        try:
            response = self._get(f"/columns/{column_id}", api_version=1).json()
            return api.Column(**response) or None
        except:
            raise ValueError(f"Column {column_id} does not exist or this API key does not have access.")

    @track_usage
    def get_columns_by_featureset(self, feature_set_id: int) -> List[api.Column]:
        """
        Returns all Columns in the specified FeatureSet
        """
        try:
            response = self._get(f"/columns/by-featureset/{feature_set_id}", api_version=1).json()
            return [api.Column(**entry) for entry in response] or None
        except:
            raise ValueError(f"FeatureSet {feature_set_id} does not exist or this API key does not have access.")

    @track_usage
    def get_data_sources(self) -> List[api.DataSource]:
        """
        Returns all DataSources available in your organization or Rasgo Community
        """
        try:
            response = self._get("/data-source", api_version=1).json()
            return [api.DataSource(**entry) for entry in response] or None
        except:
            raise ValueError("Data Sources do not exist or this API key does not have access.")

    @track_usage
    def get_data_source(self, data_source_id: int) -> api.DataSource:
        """
        Returns the DataSource with the specified id
        """
        try:
            response = self._get(f"/data-source/{data_source_id}", api_version=1).json()
            return api.DataSource(**response)
        except:
            raise ValueError(f"Data Source {data_source_id} does not exist or this API key does not have access.")
    
    @track_usage
    def get_dimensionalities(self) -> List[api.Dimensionality]:
        """
        Returns all Dimensionalities available in your organization or Rasgo Community
        """
        try:
            response = self._get("/dimensionalities", api_version=1).json()
            return [api.Dimensionality(**entry) for entry in response] or None
        except:
            raise ValueError("Dimensionalities do not exist or this API key does not have access.")
    
    @track_usage
    def get_feature(self, feature_id: int) -> Feature:
        """
        Returns the Feature with the specified id
        """
        try:
            return Feature(api_object=self._get(f"/features/{feature_id}", api_version=1).json()) or None
        except:
            raise ValueError(f"Feature {feature_id} does not exist or this API key does not have access.")
    
    @track_usage
    def get_feature_frame(self, model_id: int) -> Model:
        """
        Returns a Rasgo Model (set of joined Features) matching the specified id
        """
        return self.get_model(model_id=model_id)

    @track_usage
    def get_feature_frames(self) -> List[Model]:
        """
        Returns all Rasgo Models (set of joined Features) that I have author access to
        """
        return self.get_models()

    @track_usage
    def get_feature_set(self, feature_set_id: int) -> api.v0.FeatureSet:
        """
        Returns the FeatureSet (set of Fetures) with the specified id
        """
        try:
            response = self._get(f"/feature-sets/{feature_set_id}", api_version=1).json()
            return api.v0.FeatureSet(**response) or None
        except:
            raise ValueError(f"FeatureSet {feature_set_id} does not exist or this API key does not have access.")

    @track_usage
    def get_feature_sets(self) -> List[api.v0.FeatureSet]:
        """
        Returns a list of FeatureSets (set of Features) available in your organization or Rasgo Community
        """
        try:
            response = self._get("/feature-sets", api_version=1).json()
            return [api.v0.FeatureSet(**entry) for entry in response] or None
        except:
            raise ValueError("FeatureSets do not exist or this API key does not have access.")

    @track_usage
    def get_feature_stats(self, feature_id: int) -> api.FeatureStats:
        """
        Returns the stats profile for the specified Feature
        """
        try:
            stats_json = self._get(f"/features/{feature_id}/stats", api_version=1).json()
        except:
            raise ValueError("Stats do not exist for this Feature.")
        return api.FeatureStats(**stats_json["featureStats"]) or None
    
    @track_usage
    def get_features(self) -> FeatureList:
        """
        Returns a list of Features available in your organization or Rasgo Community
        """
        try:
            return FeatureList(api_object=self._get("/features", api_version=1).json()) or None
        except:
            raise ValueError("Features do not exist or this API key does not have access.")

    @track_usage
    def get_features_by_featureset(self, feature_set_id) -> FeatureList:
        """
        Returns a list of Features in the specific FeatureSet
        """
        try:
            response = self._get(f"/features/by-featureset/{feature_set_id}", api_version=1)
            return FeatureList(api_object=response.json()) or None
        except:
            raise ValueError(f"FeatureSet {feature_set_id} does not exist or this API key does not have access.")

    @track_usage
    def get_model(self, model_id) -> Model:
        """
        Returns a Rasgo Model (set of joined Features) matching the specified id
        """
        try:
            return Model(api_object=self._get(f"/models/{model_id}", api_version=1).json()) or None
        except:
            raise ValueError(f"Model {model_id} does not exist or this API key does not have access.")

    @track_usage
    def get_models(self) -> List[Model]:
        """
        Returns all Rasgo Models (set of joined Features) that I have author access to
        """
        try:
            return [Model(api_object=entry) for entry in self._get(f"/models", api_version=1).json()] or None
        except:
            raise ValueError("Models do not exist or this API key does not have access.")

    @track_usage
    def get_shared_feature_frames(self) -> List[Model]:
        """
        Returns all Rasgo Models (set of joined Features) shared in my organization or in Rasgo community
        """
        return self.get_shared_models()

    @track_usage
    def get_shared_models(self) -> List[Model]:
        """
        Returns all Rasgo Models (set of joined Features) shared in my organization or in Rasgo community
        """
        try:
            return [Model(api_object=entry) for entry in self._get(f"/models/shared", api_version=1).json()] or None
        except:
            raise ValueError("Shared Models do not exist or this API key does not have access.")

    @track_usage
    def get_source_columns(self) -> pd.DataFrame:
        """
        Returns a DataFrame of columns in Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_columns()

    @track_usage
    def get_source_table(self, table_name: str, record_limit: int) -> pd.DataFrame:
        """
        Returns a DataFrame of top n records in a Snowflake source table
        """
        return self.data_warehouse.get_source_table(table_name=table_name, record_limit=record_limit)

    @track_usage
    def get_source_tables(self) -> pd.DataFrame:
        """
        Return a DataFrame of Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_tables()

    @track_usage
    def match_data_source(self, name: str) -> api.DataSource:
        """
        Returns the first Data Source that matches the specified name
        """
        try:
            response = self._get(f"/data-source", {"name": name}, api_version=1).json()
            return api.DataSource(**response[0]) or None
        except:
            return None

    @track_usage
    def match_dimensionality(self, granularity: str) -> api.Dimensionality:
        """
        Returns the first community or private Dimensionality that matches the specified granularity 
        """
        try:
            response = self._get(f"/dimensionalities/granularity/{granularity}", api_version=1).json()
            return api.Dimensionality(**response) or None
        except:
            return None

    @track_usage
    def match_column(self, name: str, feature_set_id: int) -> api.Column:
        """
        Returns the first Column matching the specidied name in the specified featureset
        """
        try:
            cols = self._get(f"/columns/by-featureset/{feature_set_id}", api_version=1).json()
            for c in cols:
                if name == c["name"]:
                    return api.Column(**c)
            return None
        except:
            return None

    @track_usage
    def match_feature(self, code: str, feature_set_id: int) -> Feature:
        """
        Returns the first Feature matching the specified name in the specified featureset
        """
        try:
            features = self._get(f"/features/by-featureset/{feature_set_id}", api_version=1).json()
            for f in features: 
                if code == f["code"]:
                    return Feature(api_object=f)
            return None
        except:
            return None

    @track_usage
    def match_feature_set(self, table_name: str) -> api.v0.FeatureSet:
        """
        Returns the first FeatureSet matching the specified table name
        """
        try:
            fs = self._get(f"/feature-sets/", {"source_table": table_name}, api_version=1).json()
            # NOTE: This assumes there will be only 1 featureset in an Organization per table
            # At the point this no longer holds true, we will want to update this logic
            return api.v0.FeatureSet(**fs[0]) if fs else None
        except:
            return None


# -------------------
# Post / Create Calls
# -------------------

    @track_usage
    def create_column(self, name: str, data_type: str, feature_set_id: int, dimension_id: int) -> api.Column:
        column = api.ColumnCreate(name=name, dataType=data_type,
                                  featureSetId=feature_set_id,
                                  dimensionId=dimension_id)
        response = self._post("/columns/", column.dict(exclude_unset=True), api_version=1).json()
        return api.Column(**response)

    @track_usage
    def create_data_source(self, organization_id: int, name: str) -> api.DataSource:
        data_source = api.DataSourceCreate(name=name,
                                           abbreviation=name[:10].lower(),
                                           organizationId=organization_id)
        response = self._post("/data-source", data_source.dict(exclude_unset=True), api_version=1).json()
        return api.DataSource(**response)

    @track_usage
    def create_dimensionality(self, organization_id: int, name: str, dimension_type: str, granularity: str) -> api.Dimensionality:
        """
        Creates a dimensionality record in a user's organization with format: DimensionType - Granularity
        """
        dimensionality = api.DimensionalityCreate(name=name,
                                                  dimensionType=dimension_type,
                                                  granularity=granularity,
                                                  organizationId=organization_id)
        response = self._post("/dimensionalities", dimensionality.dict(exclude_unset=True), api_version=1).json()
        return api.Dimensionality(**response)

    @track_usage
    def create_feature(self, organization_id: int, feature_set_id: int, name: str, code: str, description: str, column_id: int,
                       status: str, gitRepo: str, tags: Optional[List[str]] = None) -> Feature:
        feature = api.FeatureCreate(name=name,
                                    code=code,
                                    description=description,
                                    featureSetId=feature_set_id,
                                    columnId=column_id,
                                    organizationId=organization_id,
                                    orchestrationStatus=status,
                                    tags=tags or [],
                                    gitRepo=gitRepo)
        response = self._post("/features/", feature.dict(exclude_unset=True), api_version=1).json()
        return Feature(api_object=response)

    @track_usage
    def create_feature_set(self, name: str, data_source_id: int, table_name: str, organization_id: int, 
                           granularity: Optional[str] = None, rawFilePath: Optional[str] = None) -> api.v0.FeatureSet:
        feature_set = api.v0.FeatureSetCreate(name=name,
                                              snowflakeTable=table_name,
                                              dataSourceId=data_source_id,
                                              granularity=granularity,
                                              rawFilePath=rawFilePath)
        response = self._post("/feature-sets/", feature_set.dict(), api_version=0).json()
        return api.v0.FeatureSet(**response)

    @track_usage
    def create_model(self, name: str,
                     type: Union[str, ModelType],
                     granularity: Union[str, Granularity],
                     description: Optional[str] = None,
                     is_shared: Optional[bool] = False) -> Model:
        """
        Creates model within Rasgo within the account specified by the API key.
        :param name: Model name
        :param model_type: Type of model specified
        :param granularity: Granularity of the data.
        :param is_shared: True = make model shared , False = make model private
        :return: Model object.
        """
        try:
            # If not enum, convert to enum first.
            model_type = type.name
        except AttributeError:
            model_type = ModelType(type)

        try:
            # If not enum, convert to enum first.
            granularity = granularity.name
        except AttributeError:
            granularity = Granularity(granularity)

        content = {"name": name,
                   "type": model_type.value,
                   "granularities": [{"name": granularity.value}],
                   "isShared": is_shared
                   }
        if description:
            content["description"] = description
        response = self._post("/models", _json=content, api_version=1)
        return Model(api_object=response.json())

    @track_usage
    def post_feature_stats(self, feature_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f"/features/{feature_id}/stats", api_version=1).json()

    @track_usage
    def post_feature_set_stats(self, feature_set_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f"/feature-sets/{feature_set_id}/stats", api_version=1).json()


# --------------------
# Patch / Update Calls
# --------------------

    @track_usage
    def update_column(self, column_id: int, name: Optional[str] = None, data_type: Optional[str] = None, 
                      feature_set_id: Optional[int] = None, dimension_id: Optional[int] = None
                      ) -> api.Column:
        column = api.ColumnUpdate(id=column_id,
                                  name=name, dataType=data_type,
                                  featureSetId=feature_set_id,
                                  dimensionId=dimension_id)
        response = self._patch(f"/columns/{column_id}", column.dict(exclude_unset=True), api_version=1).json()
        return api.Column(**response)

    @track_usage
    def update_feature(self, feature_id: int, organization_id: Optional[int] = None, feature_set_id: Optional[int] = None, 
                       name: Optional[str] = None, code: Optional[str] = None, description: Optional[str] = None,
                       column_id: Optional[int] = None, status: Optional[str] = None, tags: Optional[List[str]] = None, 
                       gitRepo: Optional[str] = None
                       ) -> Feature:
        feature = api.FeatureUpdate(id=feature_id,
                                    name=name,
                                    code=code,
                                    description=description,
                                    featureSetId=feature_set_id,
                                    columnId=column_id,
                                    organizationId=organization_id,
                                    orchestrationStatus=status,
                                    tags=tags,
                                    gitRepo=gitRepo)
        response = self._patch(f"/features/{feature_id}", feature.dict(exclude_unset=True), api_version=1).json()
        return Feature(api_object=response)

    @track_usage
    def update_feature_set(self, feature_set_id: int, name: Optional[str] = None, data_source_id: Optional[int] = None, 
                           table_name: Optional[str] = None, granularity: Optional[str] = None, rawFilePath: Optional[str] = None
                           ) -> api.v0.FeatureSet:
        feature_set = api.v0.FeatureSetUpdate(id=feature_set_id,
                                              name=name,
                                              snowflakeTable=table_name,
                                              dataSourceId=data_source_id,
                                              granularity=granularity,
                                              rawFilePath=rawFilePath)
        response = self._patch(f"/feature-sets/{feature_set_id}", feature_set.dict(exclude_unset=True), api_version=0).json()
        return api.v0.FeatureSet(**response)


# ------------
# Delete Calls
# ------------

    def delete_dimension(self):
        raise NotImplementedError('Not available yet.')

    def delete_feature(self):
        raise NotImplementedError('Not available yet.')

    def delete_feature_set(self):
        raise NotImplementedError('Not available yet.')


# ------------------
# Workflow Functions
# ------------------

    @track_usage
    def build_feature_frame(self, model_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame for the specified model

        :param model_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        model = self.get_model(model_id)
        table_metadata = model.snowflake_table_metadata(self.data_warehouse.user_credentials)
        query, values = self._make_select_statement(table_metadata, filters, limit)
        result_set = self.data_warehouse.execute_query(query, values)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def prepare_feature_set(self, source_table: str, name: Optional[str] = None, *,
                            dimensions_in: List[str], features_in: List[str] = None, df: Optional[pd.DataFrame] = None,
                            granularity: Optional[str] = None, function: FunctionType = None,
                            overwrite: bool = False, directory: Optional[str] = None) -> tuple:
        """
        Assembles required files for feature set creation and orchestration

        :param source_table: Table feature set will be built off of.
        :param name: Name of the feature set (defaults to the source table name)
        :param dimensions_in: List of column names identified as dimensions for the feature set
        :param features_in: List of column names identified as features within the feature set
                            (defaults to all non-dimension columns)
        :param df: Dataframe containing data from the source table, defaults to the first 10 entries of the source table.
                   This can be provided if its already available locally.
        :param granularity: Name of the granularity of the dimension
        :param function: Function to be optionally performed on dataframe during feature generation
        :param overwrite: Boolean flag whether to overwrite any existing files within the specified directory
                          (defaults to False)
        :param directory: Optionally specify the location of the newly created files
                          (defaults to the present working directory)
        :return: description of the featureset created
        """
        if df is None:
            df = self.get_source_table(table_name=source_table, record_limit=10)

        schema = dataframe.build_schema(df)
        dimensions = [api.v1.Dimension(name=schema[dimension]["name"],
                                       data_type=api.v1.DataType(schema[dimension]["type"]))
                      for dimension in dimensions_in]

        if features_in is None:
            features = [api.v1.Feature(name=schema[column]["name"],
                                       data_type=api.v1.DataType(schema[column]["type"]))
                        for column in schema.keys() if schema[column]["name"] not in dimensions_in]
        else:
            features = [api.v1.Feature(name=schema[feature]["name"],
                                       data_type=api.v1.DataType(schema[feature]["type"]))
                        for feature in features_in]

        feature_set = api.v1.FeatureSet(name=name, script=f"{function.__name__}.py" if function else None,
                                        dimensions=dimensions, features=features,
                                        table=source_table, granularity=granularity)

        return ingestion.generate_feature_set_files(source_table=source_table, name=name, feature_set=feature_set,
                                                    function=function, directory=directory, overwrite=overwrite)

    @track_usage
    def publish_features_from_df(self, df: pd.DataFrame, dimensions: List[str], features: List[str],
                                 granularity: str = None, tags: List[str] = None):
        """
        Creates a Feature Set from a pandas dataframe

        :dataframe: Pandas DataFrame containing all columns that will be registered with Rasgo
        :param dimensions: List of columns in df that should be used for joins to other featursets
        :param features: List of columns in df that should be registered as features in Rasgo
        :param granularity: Datetime grain to be added to all features in the df
        :param tags: List of tags to be added to all features in the df
        :return: description of the featureset created
        """
        # todo: Optionally generate list of feature columns from the dataframe columns, ie - all non-dimensions are features
        # todo: Add option to specify a featureset name + add check that it exists.
        # Type checking
        if not isinstance(dimensions, list) and all([isinstance(dimension, str) for dimension in dimensions]):
            raise TypeError('Dimensions must be provided as a list of strings, naming the columns within the dataframe')
        if not isinstance(features, list) and all([isinstance(feature, str) for feature in features]):
            raise TypeError('Features must be provided as a list of strings, naming the columns within the dataframe')

        tags = tags or []
        if not isinstance(tags, list):
            raise TypeError('Tags must be provided as a list of strings')

        org_id = self._profile.get('organizationId', None)
        self._grant_publisher(user_id=self._profile.get('id', None))
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M")
        data_source = self._publish_data_source(organization_id=org_id, name="PANDAS")

        # Convert all strings to work with Snowflake
        # Confirm each named dimension and feature exists in the dataframe.
        self._confirm_df_columns(df, dimensions, features)

        # Generate featureset name.
        featureset_name = f"pandas_by_{'-'.join(dimensions)}_{timestamp}"

        # Create a table in the data warehouse with the subset of columns we want, name table after featureset.
        all_columns = dimensions + features
        exportable_df = df[all_columns]
        self.data_warehouse.write_dataframe_to_table(exportable_df, table_name=featureset_name)

        # Add a reference to the FeatureSet
        featureset = self.create_feature_set(name=featureset_name, data_source_id=data_source.id,
                                             table_name=featureset_name, organization_id=org_id, granularity=granularity,
                                             rawFilePath=None)
        schema = dataframe.build_schema(df)

        return_featureset = {}
        return_featureset["id"] = featureset.id
        return_featureset["name"] = featureset.name
        return_featureset["granularity"] = featureset.granularity
        return_featureset["snowflakeTable"] = featureset.snowflakeTable
        if featureset.dataSource:
            return_featureset["dataSource"] = featureset.dataSource.name
        return_featureset["organizationId"] = featureset.organizationId

        # Add references to all the dimensions
        return_dimensions = {}
        for d in dimensions:
            column = schema[d]
            data_type = column["type"]
            dimension_name = column["name"]
            dimension = self._publish_dimension(organization_id=org_id, feature_set_id=featureset.id, name=dimension_name, data_type=data_type, dimension_type=None, granularity=granularity)
            return_dimensions.update({dimension.id: {"name": dimension.name}})
        return_featureset["dimensions"] = return_dimensions

        # Add references to all the features
        return_features = {}
        for f in features:
            column = schema[f]
            data_type = column["type"]
            code = column["name"]
            feature_name = f"PANDAS_{code}_{timestamp}"
            status = "Sandboxed"
            tags.append("Pandas")
            feature = self._publish_feature(organization_id=org_id, feature_set_id=featureset.id, name=feature_name, data_type=data_type, code=code, description=None, granularity=granularity, status=status, tags=tags, gitRepo=None)
            self.post_feature_stats(feature.id)
            return_features.update({feature.id:
                                        {"id": feature.id,
                                         "name": feature.name,
                                         "column": feature.code
                                         }})
        return_featureset["features"] = return_features
        return return_featureset

    @track_usage
    def publish_featureset_from_yml(self, yml_file: str, orchestrationStatus: Optional[str] = "Sandboxed", 
                                    gitRepo: Optional[str] = None) -> dict:
        """
        Publishes metadata about a FeatureSet to Pyrasgo

        :param yml_file: Rasgo compliant yml file that describes the featureset(s) being created
        :param orchestrationStatus: Sandboxed or Productionized
        :return: description of the featureset created
        """
        with open(yml_file) as fobj:
            featuresets = yaml.load(fobj, Loader=yaml.SafeLoader)
        for fs in featuresets:
            # publish featureset
            org_id = self._profile.get('organizationId', None)
            data_source = self._publish_data_source(organization_id=org_id, name=fs["datasource"])
            featureset_name = fs.get("name", fs["table"])
            snowflake_table = fs["table"]
            if not snowflake_table:
                raise Exception("A valid table name is required")
            granularity = fs.get("granularity")
            tags = list()
            if fs.get("tags"):
                for t in fs.get("tags"):
                    tags.append(t)
            featureset = self._publish_feature_set(name=featureset_name, data_source_id=data_source.id, table_name=snowflake_table, organization_id=org_id, granularity=granularity, rawFilePath=gitRepo)

            return_featureset = {}
            return_featureset["id"] = featureset.id
            return_featureset["name"] = featureset.name
            return_featureset["granularity"] = featureset.granularity
            return_featureset["snowflakeTable"] = featureset.snowflakeTable
            if featureset.dataSource:
                return_featureset["dataSource"] = featureset.dataSource.name
            return_featureset["organizationId"] = featureset.organizationId
            
            # publish dimensions
            return_dimensions = {}
            for dim in fs["dimensions"]:
                name = dim.get("name")
                data_type = dim.get("data_type")
                # allow granularity on a dimension to override the featureset granularity
                dim_granularity = dim.get("granularity", granularity)
                d = self._publish_dimension(organization_id=org_id, feature_set_id=featureset.id, name=name, data_type=data_type, dimension_type=None, granularity=dim_granularity)
                return_dimensions.update({d.id: {"name": d.name}})
            return_featureset["dimensions"] = return_dimensions

            # publish features
            return_features = {}
            #Note: gitRepo will be passed in from Orchestrator as a github/ or bitbucket/ path
            #      we'll want to pick up the sql/py file from the featureset yml
            gitUrl = gitRepo+fs.get("script", "") if gitRepo else fs.get("script", "")
            for feature in fs["features"]:
                name = feature["display_name"]
                code = feature.get("name", name)
                data_type = feature.get("data_type")
                description = feature.get("description", f"Feature that contains {name} data")
                # apply featureset tags to all features...
                feature_tags = list()
                feature_tags += tags
                # ...and add feature-specific tags
                if feature.get("tags"):
                    for t in feature.get("tags"):
                        feature_tags.append(t)
                f = self._publish_feature(organization_id=org_id, feature_set_id=featureset.id, name=name, data_type=data_type, code=code, description=description, granularity=granularity, status=orchestrationStatus, tags=feature_tags, gitRepo=gitUrl)
                return_features.update({f.id:
                                            {"id": f.id,
                                             "name": f.name,
                                             "column": f.code
                                             }})
            return_featureset["features"] = return_features
        return return_featureset


# ---------------------
# Awkward Model Methods
# ---------------------

    @track_usage
    def add_feature_to(self, model: Model, feature: Feature):
        model.add_feature(feature)

    @track_usage
    def add_features_to(self, model: Model, features: FeatureList):
        model.add_features(features)

    @track_usage
    def generate_training_data_for(self, model: Model):
        model.generate_training_data()

    @track_usage
    def get_feature_data(self, model_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        return self.build_feature_frame(model_id=model_id, filters=filters, limit=limit)


# -------------------------------
# Undocumented / Helper Functions
# -------------------------------

    def _confirm_df_columns(self, dataframe: pd.DataFrame, dimensions: List[str], features: List[str]):
        df_columns = list(dataframe.columns)
        missing_dims = []
        missing_features = []
        for dim in dimensions:
            if dim not in df_columns:
                missing_dims.append(dim)
        for ft in features:
            if ft not in df_columns:
                missing_features.append(ft)
        if missing_dims or missing_features:
            raise Exception(f"Specified columns do not exist in dataframe: "
                            f"Dimensions({missing_dims}) Features({missing_features})")

    def _grant_publisher(self, user_id: int):
        """
        Grants the org publisher role to a user in Snowflake
        """
        return self._patch(f"/admin/users/{user_id}/grant-publish-access", api_version=1).json()

    def _get_user(self):
        return self._get("/users/me", api_version=1).json()

    @staticmethod
    def _make_select_statement(table_metadata: dict, filters: dict, limit: Optional[int] = None) -> tuple:
        """
        Constructs select * query for table
        """
        query = "SELECT * FROM {database}.{schema}.{table}".format(**table_metadata)
        values = []
        if filters:
            comparisons = []
            for k, v in filters.items():
                if isinstance(v, list):
                    comparisons.append(f"{k} IN ({', '.join(['%s'] * len(v))})")
                    values += v
                elif v[:1] in ['>', '<', '='] \
                        or v[:2] in ['>=', '<=', '<>', '!='] \
                        or v[:4] == 'IN (' \
                        or v[:8] == 'BETWEEN ':
                    comparisons.append(f'{k} {v}')
                else:
                    comparisons.append(f"{k}=%s")
                    values.append(v)
            query += " WHERE " + " and ".join(comparisons)
        if limit:
            query += " LIMIT {}".format(limit)
        return query, values

    def _publish_data_source(self, organization_id: int, name: str) -> api.DataSource:
        """
        Creates or returns a DataSource depending on of the defined parameters
        """
        # Check for a 'dimensionality' record that corresponds to the the dimensions
        # datatype and granularity.
        return self.match_data_source(name=name) or self.create_data_source(organization_id=organization_id, name=name)

    def _publish_dimension(self, organization_id: int, feature_set_id: int, name: str, data_type: str,
                          dimension_type: Optional[str] = None, granularity: Optional[str] = None) ->api.Column:
        """
        Creates or updates a dimension depending on existence of the defined parameters
        """
        dimensionality = self._publish_dimensionality(organization_id=organization_id, dimension_type=dimension_type, granularity=granularity)
        dimensionality_id = dimensionality.id
        dim = self.match_column(name=name, feature_set_id=feature_set_id)
        return self.update_column(column_id=dim.id, name=name, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimensionality_id) if dim else \
            self.create_column(name=name, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimensionality_id)

    def _publish_dimensionality(self, organization_id: int, dimension_type: Optional[str] = None,
                               granularity: Optional[str] = None) -> api.Dimensionality:
        """
        Creates or returns a dimensionality depending on existence of the defined parameters

        Dimensionality is a named pairing of a datatype and a granularity. Note in some cases the
        granularity is actually a data type.
        """
        # TODO: We should move this mapping to the Granularity enum class or behind an API
        if dimension_type is None:
            if granularity.lower() in ["second", "minute", "hour", "day", "week", "month", "quarter", "year"]:
                dimension_type = "DateTime"
            elif granularity.lower() in ["latlong", "zipcode", "fips", "dma", "city", "cbg", "county", "state",
                                         "country"]:
                dimension_type = "Geolocation"
            else:
                dimension_type = "Custom"
        elif dimension_type.lower() == "datetime":
            dimension_type = "DateTime"
        elif dimension_type.lower() in ["geo", "geoloc", "geolocation"]:
            dimension_type = "Geolocation"
        else:
            dimension_type = dimension_type.title()
        dimensionality_name = "{} - {}".format(dimension_type, str(granularity).title())

        # Check for a 'dimensionality' record that corresponds to the the dimensions
        # datatype and granularity.
        return self.match_dimensionality(granularity) or \
               self.create_dimensionality(organization_id=organization_id, name=dimensionality_name, dimension_type=dimension_type, granularity=granularity)

    def _publish_feature(self, organization_id: int, feature_set_id: int, name: str, data_type: str, code: Optional[str] = None,
                        description: Optional[str] = None, granularity: Optional[str] = None,
                        status: Optional[str] = None, tags: Optional[List[str]] = None, gitRepo: Optional[str] = None) -> Feature:
        """
        Creates or updates a feature depending on existence of the defined parameters
        """
        code = code or name
        description = description or f"Feature that contains {name} data"
        status = status or "Sandboxed"
        dimension_id = None if granularity is None else self._publish_dimensionality(organization_id=organization_id, dimension_type=None, granularity=granularity).id

        ft = self.match_feature(code, feature_set_id)
        if ft:
            self.update_column(column_id=ft.columnId, name=code, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimension_id)
            feature = self.update_feature(feature_id=ft.id, organization_id=organization_id, feature_set_id=feature_set_id, name=name, code=code, description=description, column_id=ft.columnId,
                                          status=status, tags=tags or [], gitRepo=gitRepo)
        else:
            column = self.create_column(name=code, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimension_id)
            feature = self.create_feature(organization_id=organization_id, feature_set_id=feature_set_id, name=name, code=code, description=description, column_id=column.id, status=status, gitRepo=gitRepo,
                                          tags=tags or [])

        return feature

    def _publish_feature_set(self, name: str, data_source_id: int, table_name: str, organization_id: int, granularity: Optional[str] = None, rawFilePath: Optional[str]=None) -> api.v0.FeatureSet:
        """
        Creates or updates a featureset depending on existence of the defined parameters
        """
        fs = self.match_feature_set(table_name=table_name)
        return self.update_feature_set(feature_set_id=fs.id, name=name, data_source_id=data_source_id, table_name=table_name, granularity=granularity, rawFilePath=rawFilePath) if fs else \
            self.create_feature_set(name=name, data_source_id=data_source_id, table_name=table_name, organization_id=organization_id, granularity=granularity, rawFilePath=rawFilePath)
