# Artsobservasjon to eBird
Are you a Norwegian birder? Want to get all of your artsob observations into eBird? If you answered yes to these questions, then this tool might be for you.

This tool is very much in development, so you can expect some changes in the future. I will try to only make them improvements, and not breaking feature changes. Have a read of the known issues and error handling sections to become aware of some of the limitations.

## What it does
artsob-to-ebird converts your artsob records to the [eBird record format](https://support.ebird.org/en/support/solutions/articles/48000907878-upload-spreadsheet-data-to-ebird#anchorRecordFormat). This allows you to import your records into eBird with a single click. The tool uses the scientific species name in the artsob record to find what eBird call the Common Name. eBird [provides a list](data/ebird-species-list.json) of all the world's birds naming data.

## Known Issue(s)
#### Different Scientific Names in datasets
Some scientific names used by Artsob are not the same as the scientic names used by eBird. As an example, the Common Linnet (Tornirisk in Norwegian) has the scientific name *Carduelis cannabina* in the Artsob system. In eBird, it is known as the Eurasian Linnet and has the scientific name *Linaria cannabina*.

This discrepency results in artsob-to-ebird not being able to find the correct *Common Name* as used by eBird. This means that records where an eBird *Common Name* cannot be found, are not converted to an eBird record and hence, will not be imported in eBird.

### Different Spelling between eBird web interface and eBird API

This issue caused me some grief after I had imported my data into eBird. eBird said that it didn't recognise 20 or so of the species I had imported. I find this very strange as it is the eBird API I have used to get the names of the birds that I imported.

As an example, my Artsob data had a record for *Lanius excubitor*, which in English is a Great Grey Shrike. I asked eBird for the *common name* for the species *Lanius excubitor* and eBird returned the name *Great Gray Shrike* (note the "a" in gray).

When the eBird importer had finished it told me that it did not recognise *Great Gray Shrike* (with an "a" in gray) and made me find the correct species. So I found the correct species, which the eBird web client calls, *Great Grey Shrike* (with an "e" in gray.)

If you don't believe me (I don't blame you), click on the [eBird species list](data/ebird-species-list.json) and search for *Lanius excubitor*. 

## How it works
This tool reads either a Microsoft Excel or CSV (Comma Serpated Value) file of your artsob records. This part you will have to do yourself, but you can search for your own records on artsob and export them as an Excel file. You can also search for records where you are not the reporter, but an observer.

**Important**: The CSV file should in fact be serpareted using **;**. This is because Artsob exports a list of observers separated by **,** in the column named **Observatører**. As an example, your CSV data would look like this:

```
;VU;stjertand;Anas acuta;Linnaeus, 1758;Nei;1;;Adult;Hunn; ;;Østensjøvannet;Østensjøvannet Syd;602483;6639796;0;Ø266747,
```

Gather all the records you wish to import into an Excel or CSV file and place this file in the root of this software's directory. Run the program with:
```bash
 python artsob-to-ebird.py my-artobs-excel-file.xlsx
```
where `my-artobs-excel-file.xlsx` is the name of the file you created containing your Artsob records. The tool will then create a two files, one Excel file and one CSV file called *ebird_observations* but will have different file extensions.

### Example from my Mac
```bash
(.env) conor at flatline in artsob-to-ebird on master [+!?]
$ ls
README.md                   artsob-my-obs-complete.xlsx artsob-to-ebird.py          data                        results.log                 src
(.env) conor at flatline in artsob-to-ebird on master [+!?]

$ python artsob-to-ebird.py artsob-my-obs-complete.xlsx 

Successfully created ebird_observations.xlsx from artsob-my-obs-complete.xlsx

$ ls
README.md                   artsob-my-obs-complete.xlsx artsob-to-ebird.py          data                        ebird_observations.xlsx     results.log                 src

```

### CSV

If you want to import from CSV, use the `--format csv` option:

`python artsob-to-ebird.py artsob-my-obs-complete.xlsx --format csv`

## Logging
The program will log to `results.log` in the root directory containing the code.

## Error Handling

This program is very much in beta, but I've implemented some error handling

### Files
The program should detect
- File not found
- Incorrect format, i.e. not an excel file or not a CSV file
- Incorrect data in file, i.e. not the expected columns from an Artsob export

### Duplicate Entries
If for whatever reason, and this happened to me, end up with lots of duplicate entries in your Artsob file, the program will detect them and report this to you.

`ERROR - 2021-04-14 19:04:15,185 - Duplicate Artsob record ID already imported: 15788899. Ignoring this entry`

### Can't find species name
As mentioned above in the Know Issues section, there is an issue finding some species names. If a record's *Common Name* cannot be determined, the program will report it and ignore that particular record. This should allow you to manually enter these records. I hope to have a workaround for this soon.

`ERROR - 2021-04-14 19:04:15,192 - No species found in lookup table for Carduelis cannabina`

I hope this tool can be of use to the three birders in Norway who want to escape from Artsob to eBird. Feel free to report issues, and I'll do my best to solve them. Contributors absolutely welcome!