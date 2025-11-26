# Data Generation

Generate data in Cortex data Foundation for a set of demo scenarios.

## Configuration Parameters

|Parameter|Definition / Comment|Allowed Values|
|---------|--------------------|--------------|
|`project`|Google Cloud Project ID. Target project into which data will be generated.| Any existing Google Cloud project.|
|`scenarios`|A demo scenario involving Cortex Data Foundation datasets in BigQuery.||
|`scenarios[i].name`|Name of the demo scenario.|`alphanumeric`|
|`scenarios[i].solutions`|A enterprise data source required for the demo scenario.  There can be multiple solutions for a given scenario.  Hint: Typically in Cortex Data Foundation, a solution will have its own set of `RAW`, `CDC` & `REPORTING` datasets.||
|`scenarios[i].solutions[j].type`|Type of a solution.| `['sap', 'salesforce', 'other']`|
|`scenarios[i].solutions[j].client`|SAP Client under which data will be generated.  Applicable only if `scenarios[i].solutions[j].type == 'sap'`||
|`scenarios[i].solutions[j].dataset`|BigQuery dataset in which the data should be generated.|Must exist in the specified project.|
|`scenarios[i].solutions[j].tables`|List of tables for which data should be generated.|Must exist in the specified `scenarios[i].solutions[j].dataset`|
|`scenarios[i].solutions[j].tables[k].name`|Name of the table in the `scenarios[i].solutions[j].dataset`.| Must exist.|
|`scenarios[i].solutions[j].tables[k].spec`|Name of the field-level specifications for data generation (A `.json` file which should exist in teh source path `metadata/table-specs`| Should comply with `metadata/table-specs/table-spec.schema.json`|
|`scenarios[i].solutions[j].tables[k].recordsFromSeedFile`|Specifies whether the data is generated from a pre-defined set of values as a `'json` file.  Typically master data for a demo scenario can be specified as a set of `.json` files. e.g., Material Numbers (SAP), Plants (SAP) etc. |Boolean.|
|`scenarios[i].solutions[j].tables[k].series`||OPTIONAL|
|`scenarios[i].solutions[j].tables[k].series.takt`|Frequency at which data should be generated (year / month, week, day)||
|`scenarios[i].solutions[j].tables[k].series.range`|Number of takts backwards from current date (e.g., `24` => last 24 months - if `takt = month` )|integer|
|`scenarios[i].solutions[j].tables[k].write`|Write Disposition for BigQuery Job Configuration. `TRUNCATE` = delete existing table content before writing newly generated data.  `APPEND` = add newly generated data to existing set of records in the table.|`TRUNCATE`, `APPEND`|
|`scenarios[i].solutions[j].tables[k].strategy`|Custom data generation strategy.  Each table into which data is generated could require custom tweaks in addition to mostly auto generated content. ||
|`scenarios[i].solutions[j].tables[k].strategy.module`|Python module under which the custom implementation python class is located|Module should exist in source path `data/gen/strategies`.|
|`scenarios[i].solutions[j].tables[k].strategy.module`|Python class in which the custom implementation python is implemented|Class should exist in source path `data/gen/strategies` under the `scenarios[i].solutions[j].tables[k].strategy.module` name.|

## Changing credentials to a different Google target project

* Recommended to create a new `gcloud init` and following the instructions there.
* Create service account or pick a service account that has `BigQuery Admin` permission.
* Create or use key for this service account.
* Copy to `config/keys` folder in this project
* Change the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to point to the new file. For example:

    ```shell
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
    ```

* If you have a python virtual environment setup and are running the generator from that virtual environment, also check if the environment variable is also updated in the corresponding activate file (if you added it previously).  For example in case of `venv`, check the file `~/.virtualenvs/<your env name>/bin/activate` for the following statement and update it.

    ```shell
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/new/key.json
    ```

    Do not forget to activate!

    ```shell
    source venv/bin/activate
    ```
