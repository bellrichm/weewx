!!! Warning
    Running WeeWX during a `wee_import` session can lead to abnormal 
    termination of the import. If WeeWX must remain running (e.g., so that 
    live data is not lost) run the `wee_import` session on another machine or 
    to a second database and merge the in-use and second database once the 
    import is complete.

`wee_import` can import observational data from the one or more Weather 
Display monthly log files. Weather Display records observational data on a 
monthly basis in a number of either space delimited (.txt) and/or comma 
separated (.csv) text files. `wee_import` can import observational data 
from the following Weather Display log files:

* MMYYYYlg.txt
* MMYYYYlgcsv.csv (csv format version of MMYYYYlg.txt)
* MMYYYYvantagelog.txt
* MMYYYYvantagelogcsv.csv (csv format version of MMYYYYvantagelog.txt)
* MMYYYYvantageextrasensorslog.csv

where MM is a one or two-digit month and YYYY is a four digit year

The Weather Display monthly log files record observational data using a 
nominal one-minute interval with each file recording various observations 
for the month and year designated by the MM and YYYY components of the 
file name. These files are accumulated over time and can be considered 
analogous to the WeeWX archive table. When `wee_import` imports data from 
the Weather Display monthly log files each set of log files for a given 
month and year is considered a 'period'. `wee_import` processes one period 
at a time in chronological order (oldest to newest) and provides import 
summary data on a per period basis.

## Mapping data to archive fields

The WeeWX archive fields populated during the import of Weather Display 
data depends on the field mapping specified in `[[FieldMap]]` stanza in 
the import configuration file. A given WeeWX field will be populated if:

* a valid field mapping exists,

* the WeeWX field exists in the WeeWX archive table schema, and

* the mapped Weather Display field contains valid data.

The following WeeWX archive fields will be populated from other settings 
or configuration options and need not be included in the field map:

* `interval`

* `usUnits`

The following WeeWX archive fields will be populated with values derived 
from the imported data provided `calc_missing = True` is included in the `
[WD]` section of the import configuration file being used and the field 
exists in the in-use WeeWX archive table schema:

* `altimeter`
 
* `pressure`
 
* `rainRate`

* `windchill`

!!! Note
    If `calc_missing = False` is included in the `[WD]` section of the 
    import configuration file being used then all of the above fields will be 
    set to `None/null`. The `calc_missing` option default is `True`.


## Step-by-step instructions

To import observations from one or more Weather Display monthly log files:

1. Ensure the Weather Display monthly log file(s) to be used for the 
   import are located in a directory accessible by the machine that will 
   run `wee_import`. For the purposes of the following examples, there are 
   five months of logs files covering the period September 2018 to January 
   2019 inclusive located in the `/var/tmp/wd` directory.

1. Make a backup of the WeeWX database in case the import should go awry.

1. Create an import configuration file, this is easily done by making a 
   copy of the example Weather Display import configuration file located 
   in the `/home/weewx/util/import` or `/etc/weewx/import` directory as 
   applicable. In this case we will make a copy of the example Weather 
   Display import configuration file and save it as `wd.conf` in the 
   `/var/tmp` directory:

    ```
    $ cp /home/weewx/util/import/wd-example.conf /var/tmp/wd.conf
    ```

1. Confirm that the [`source`](../wee_import-config#import_config_source) option is set to WD:

    ```
    source = WD
    ```

1. Confirm that the following options in the `[WD]` section are correctly set:

    * [directory](../wee_import-config#wd_directory). The full path to the 
      directory containing the Weather Display monthly log files to be 
      used as the source of the imported data.

    * [logs_to_process](../wee_import-config#wd_logs_to_process). 
      Specifies the Weather Display monthly log files to be used to import 
      data.

    * [interval](../wee_import-config#wd_interval). Determines how the 
      WeeWX interval field is derived.

    * [qc](../wee_import-config#wd_qc). Determines whether quality control 
      checks are performed on the imported data.

    * [calc_missing](../wee_import-config#wd_calc_missing). Determines 
      whether missing derived observations will be calculated from the 
      imported data.

    * [txt_delimiter](../wee_import-config#wd_txt_delimiter). The field 
      delimiter used in the Weather Display space delimited (*.txt) 
      monthly log files.

    * [csv_delimiter](../wee_import-config#wd_csv_delimiter). The field 
      delimiter used in the Weather Display monthly comma separated values 
      (*.csv) monthly log files.

    * [decimal](../wee_import-config#wd_decimal). The decimal point 
      character used in the Weather Display monthly log files.

    * [ignore_missing_log](../wee_import-config#wd_ignore_missing_log). 
      Determines whether missing log files are to be ignored or the import 
      aborted.

    * [ignore_invalid_data](../wee_import-config#wd_ignore_invalid_data). 
      Determines whether invalid data in a source field is ignored or the 
      import aborted.

    * [tranche](../wee_import-config#wd_tranche). The number of records 
      written to the WeeWX database in each transaction.

    * [UV_sensor](../wee_import-config#wd_UV). Whether a UV sensor was 
      installed when the source data was produced.

    * [solar_sensor](../wee_import-config#wd_solar). Whether a solar 
      radiation sensor was installed when the source data was produced.

    * [ignore_extreme_temp_hum](..
      /wee_import-config#wd_ignore_extreme_temp_hum). Determines whether 
      temperature and humidity values of 255 will be ignored.

    * [[[Units]]](../wee_import-config#wd_units). Defines the units used 
      in the Weather Display monthly log files.

    * [[[FieldMap]]](../wee_import-config#wd_fieldmap). Defines the 
      mapping between imported data fields and WeeWX archive fields.

1. When first importing data it is prudent to do a dry run import before 
   any data is actually imported. A dry run import will perform all steps 
   of the import without actually writing imported data to the WeeWX 
   database. In addition, consideration should be given to any additional 
   options to be used such as `--date`.

    !!! Note
        Due to some peculiarities of the Weather Display log structure it 
        may be prudent to use the `--suppress-warnings` option during the 
        initial dry run so the overall progress of the import can be observed.

    To perform a dry run enter the following command:

    ```
    wee_import --import-config=/var/tmp/wd.conf --dry-run --suppress-warnings
    ```

    This will result in a short preamble with details on the data source, 
   the destination of the imported data and some other details on how the 
   data will be processed. The import will then be performed but no data 
   will be written to the WeeWX database.

    The output should be similar to:

    ```
    Using WeeWX configuration file /home/weewx/weewx.conf
    Starting wee_import...
    Weather Display monthly log files in the '/var/tmp/WD' directory will 
   be imported
    Using database binding 'wx_binding', which is bound to database 'weewx.
   sdb'
    Destination table 'archive' unit system is '0x01' (US).
    Missing derived observations will be calculated.
    This is a dry run, imported data will not be saved to archive.
    Starting dry run import ...
    Records covering multiple periods have been identified for import.
    Period 1 ...
    Unique records processed: 43183; Last timestamp: 2018-09-30 23:59:00 
   AEST (1538315940)
    Period 2 ...
    Unique records processed: 44620; Last timestamp: 2018-10-31 23:59:00 
   AEST (1540994340)
    Period 3 ...
    Unique records processed: 43136; Last timestamp: 2018-11-30 23:59:00 
   AEST (1543586340)
    Period 4 ...
    Unique records processed: 44633; Last timestamp: 2018-12-31 23:59:00 
   AEST (1546264740)
    Period 5 ...
    Unique records processed: 8977; Last timestamp: 2019-01-07 05:43:00 
   AEST (1546803780)
    Finished dry run import
    184765 records were processed and 184549 unique records would have 
   been imported.
    216 duplicate records were ignored.
    ```

    !!! Note
        The five periods correspond to the five months of log files used 
        for this import.
    
    !!! Note
        Any periods for which no data could be obtained will be skipped. 
        The lack of data may be due to a missing Weather Display log file. A 
        short explanatory note to this effect will be displayed against the 
        period concerned and an entry included in the log.

1. If the `--suppress-warnings` option was used it may be prudent to do a 
   second dry run this time without the `--suppress-warnings` option. This 
   will allow any warnings generated by the dry run import to be observed:

    ```
    wee_import --import-config=/var/tmp/wd.conf --dry-run
    ```

    This will result in a short preamble with details on the data source, 
   the destination of the imported data and some other details on how the 
   data will be processed. The import will then be performed but no data 
   will be written to the WeeWX database.

    The output should be similar to:

    ```
    Using WeeWX configuration file /home/weewx/weewx.conf
    Starting wee_import...
    Weather Display monthly log files in the '/var/tmp/WD' directory will 
   be imported
    Using database binding 'wx_binding', which is bound to database 'weewx.
   sdb'
    Destination table 'archive' unit system is '0x01' (US).
    Missing derived observations will be calculated.
    This is a dry run, imported data will not be saved to archive.
    Starting dry run import ...
    Records covering multiple periods have been identified for import.
    Period 1 ...
    Warning: Import field 'radiation' is mapped to WeeWX field 'radiation' 
   but the
    import field 'radiation' could not be found in one or more records.
    WeeWX field 'radiation' will be set to 'None' in these records.
    Warning: Import field 'soiltemp' is mapped to WeeWX field 'soilTemp1' 
   but the
    import field 'soiltemp' could not be found in one or more records.
    WeeWX field 'soilTemp1' will be set to 'None' in these records.
    Warning: Import field 'soilmoist' is mapped to WeeWX field 
   'soilMoist1' but the
    import field 'soilmoist' could not be found in one or more records.
    WeeWX field 'soilMoist1' will be set to 'None' in these records.
    Warning: Import field 'humidity' is mapped to WeeWX field 
   'outHumidity' but the
    import field 'humidity' could not be found in one or more records.
    WeeWX field 'outHumidity' will be set to 'None' in these records.
    Warning: Import field 'heatindex' is mapped to WeeWX field 'heatindex' 
   but the
    import field 'heatindex' could not be found in one or more records.
    WeeWX field 'heatindex' will be set to 'None' in these records.
    Warning: Import field 'windspeed' is mapped to WeeWX field 'windSpeed' 
   but the
    import field 'windspeed' could not be found in one or more records.
    WeeWX field 'windSpeed' will be set to 'None' in these records.
    Warning: Import field 'barometer' is mapped to WeeWX field 'barometer' 
   but the
    import field 'barometer' could not be found in one or more records.
    WeeWX field 'barometer' will be set to 'None' in these records.
    Warning: Import field 'dewpoint' is mapped to WeeWX field 'dewpoint' 
   but the
    import field 'dewpoint' could not be found in one or more records.
    WeeWX field 'dewpoint' will be set to 'None' in these records.
    Warning: Import field 'rainlastmin' is mapped to WeeWX field 'rain' 
   but the
    import field 'rainlastmin' could not be found in one or more records.
    WeeWX field 'rain' will be set to 'None' in these records.
    Warning: Import field 'direction' is mapped to WeeWX field 'windDir' 
   but the
    import field 'direction' could not be found in one or more records.
    WeeWX field 'windDir' will be set to 'None' in these records.
    Warning: Import field 'temperature' is mapped to WeeWX field 'outTemp' 
   but the
    import field 'temperature' could not be found in one or more records.
    WeeWX field 'outTemp' will be set to 'None' in these records.
    Warning: Import field 'gustspeed' is mapped to WeeWX field 'windGust' 
   but the
    import field 'gustspeed' could not be found in one or more records.
    WeeWX field 'windGust' will be set to 'None' in these records.
    Unique records processed: 43183; Last timestamp: 2018-09-30 23:59:00 
   AEST (1538315940)
    Period 2 ...
    Unique records processed: 44620; Last timestamp: 2018-10-31 23:59:00 
   AEST (1540994340)
    Period 3 ...
    Unique records processed: 43136; Last timestamp: 2018-11-30 23:59:00 
   AEST (1543586340)
    Period 4 ...
    Unique records processed: 44633; Last timestamp: 2018-12-31 23:59:00 
   AEST (1546264740)
    Period 5 ...
    Unique records processed: 8977; Last timestamp: 2019-01-07 05:43:00 
   AEST (1546803780)
    6 duplicate records were identified in period 5:
    2019-01-04 10:31:00 AEST (1546561860)
    2019-01-04 10:32:00 AEST (1546561920)
    2019-01-04 10:33:00 AEST (1546561980)
    2019-01-04 10:34:00 AEST (1546562040)
    2019-01-04 10:35:00 AEST (1546562100)
    2019-01-04 10:36:00 AEST (1546562160)
    Finished dry run import
    184555 records were processed and 184549 unique records would have 
   been imported.
    6 duplicate records were ignored.
    ```

    In this case the following warnings are evident:

    * Period one had 12 warnings for import fields that were mapped to 
      WeeWX data fields but for which no data was found. This could be a 
      sign that a complete month of data or a significant portion of the 
      month could be missing, or it could be a case of just the first 
      record of the month is missing (a significant number of Weather 
      Display monthly log files have been found to be missing the first 
      record of the month). In most cases this warning can be ignored.

    * Period five shows warnings for six entries in the period that have 
      duplicate timestamps. This could be a sign that there is a problem 
      in one or more of the Weather Display monthly log files for that 
      month. However, anecdotally it has been found that duplicate entries 
      often exist in one or more Weather Display monthly log files. If the 
      duplicates are to be ignored then such warnings can be ignored 
      otherwise the incorrect data should be removed from the affected log 
      files before import.

1. Once the dry run results are satisfactory the data can be imported 
   using the following command:

    ```
    wee_import --import-config=/var/tmp/wd.conf --suppress-warnings
    ```
    
    !!! Note
        The `--suppress-warnings` option has been used to suppress the 
        previously encountered warnings.
    
    This will result in a preamble similar to that of a dry run. At the 
   end of the preamble there will be a prompt:

    ```
    Using WeeWX configuration file /home/weewx/weewx.conf
    Starting wee_import...
    Weather Display monthly log files in the '/var/tmp/WD' directory will 
   be imported
    Using database binding 'wx_binding', which is bound to database 'weewx.
   sdb'
    Destination table 'archive' unit system is '0x01' (US).
    Missing derived observations will be calculated.
    Starting import ...
    Records covering multiple periods have been identified for import.
    Period 1 ...
    Proceeding will save all imported records in the WeeWX archive.
    Are you sure you want to proceed (y/n)?
    ```

    If there is more than one month of Weather Display monthly log files 
   then `wee_import` will provide summary information on a per period 
   basis during the import. In addition, if the `--date` option is used 
   then source data that falls outside the date or date range specified 
   with the `--date` option is ignored. In such cases the preamble may 
   look similar to:
    
    ```
    Using WeeWX configuration file /home/weewx/weewx.conf
    Starting wee_import...
    Weather Display monthly log files in the '/var/tmp/WD' directory will 
   be imported
    Using database binding 'wx_binding', which is bound to database 'weewx.
   sdb'
    Destination table 'archive' unit system is '0x01' (US).
    Missing derived observations will be calculated.
    Observations timestamped after 2018-10-12 00:00:00 AEST (1539266400) 
   and up to and
    including 2018-10-13 00:00:00 AEST (1539352800) will be imported.
    Starting import ...
    Records covering multiple periods have been identified for import.
    Period 1 ...
    Period 1 - no records identified for import.
    Period 2 ...
    Proceeding will save all imported records in the WeeWX archive.
    Are you sure you want to proceed (y/n)?
    ```

1. If the import parameters are acceptable enter `y` to proceed with the 
   import or `n` to abort the import. If the import is confirmed, the 
   source data will be imported, processed and saved in the WeeWX database.
   Information on the progress of the import will be displayed similar to 
   the following:

    ```
    Unique records processed: 1250; Last timestamp: 2018-12-01 20:49:00 
   AEST (1543661340)
    ```

    Again if there is more than one month of Weather Display monthly log 
   files and if the `--date` option is used the progress information may 
   instead look similar to:

    ```
    Period 2 ...
    Unique records processed: 44620; Last timestamp: 2018-10-31 23:59:00 
   AEST (1540994340)
    Period 3 ...
    Unique records processed: 43136; Last timestamp: 2018-11-30 23:59:00 
   AEST (1543586340)
    Period 4 ...
    Unique records processed: 12000; Last timestamp: 2018-12-09 07:59:00 
   AEST (1544306340)
    ```
    
    !!! Note
        Any periods for which no data could be obtained will be skipped. 
        The lack of data may be due to a missing Weather Display log file. A 
        short explanatory note to this effect will be displayed against the 
        period concerned and an entry included in the log.

    The line commencing with `Unique records processed` should update as 
   records are imported with progress information on number of unique 
   records processed and the date time of the latest record processed. If 
   the import spans multiple months then a new `Period` line is created 
   for each month.

    Once the initial import is complete `wee_import` will, if requested, 
   calculate any missing derived observations and rebuild the daily 
   summaries. A brief summary should be displayed similar to the following:

    ```
    Calculating missing derived observations ...
    Processing record: 184549; Last record: 2019-01-08 00:00:00 AEST 
   (1546869600)
    Recalculating daily summaries...
    Records processed: 184000; Last date: 2019-01-06 20:34:00 AEST 
   (1546770840)
    Finished recalculating daily summaries
    Finished calculating missing derived observations
    ```

    When the import is complete a brief summary is displayed similar to 
   the following:

    ```
    Finished import
    184765 records were processed and 184549 unique records imported in 
   699.27 seconds.
    216 duplicate records were ignored.
    Those records with a timestamp already in the archive will not have been
    imported. Confirm successful import in the WeeWX log file.
    ```

1. Whilst `wee_import` will advise of the number of unique records 
   imported, `wee_import` does know how many, if any, of the imported 
   records were successfully saved to the database. You should look 
   carefully through the WeeWX log file covering the `wee_import` session 
   and take note of any records that were not imported. The most common 
   reason for imported records not being saved to the database is because 
   a record with that timestamp already exists in the database, in such 
   cases something similar to the following will be found in the log:

    ```
    Aug 22 14:38:28 stretch12 weewx[863]: manager: unable to add record 
   2018-09-04 04:20:00 AEST (1535998800) to database 'weewx.sdb': UNIQUE 
   constraint failed: archive.dateTime
    ```

    In such cases take note of the timestamp of the record(s) concerned 
   and make a decision about whether to delete the pre-existing record and 
   re-import the record or retain the pre-existing record.