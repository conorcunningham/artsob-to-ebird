# Artsobservasjon to EBird
Are you a Norwegian birder? Are you tired of Artsobservasjon.no? Are you using EBird and are happy as Larry with it? Want to get all of your artsob observations into Ebird? If you answered yes to these questions, then this tool might be for you.

## What it does
artsob-to-ebird converts your artsob records to the [EBird record format](https://support.ebird.org/en/support/solutions/articles/48000907878-upload-spreadsheet-data-to-ebird#anchorRecordFormat). This allows you to import your records into EBird with a single click. The tool uses the scientific species name in the artsob record to find what EBird call the Common Name. EBird [provides a list](data/ebird-species-list.json) of all the world's birds naming data.

## Known Issue(s)
#### Different Scientific Names in datasets
Some scientific names used by Artsob are not the same as the scientic names used by EBird. As an example, the Common Linnet (Tornirisk in Norwegian) has the scientific name *Carduelis cannabina* in the Artsob system. In EBird, it is known as the Eurasian Linnet and has the scientific name *Linaria cannabina*.

This discrepency results in artsob-to-ebird not being able to find the correct *Common Name* as used by EBird. This means that records where an EBird *Common Name* cannot be found, are not converted to an EBird record and hence, will not be imported in EBird.

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

I hope this tool can be of use to the three birders in Norway who want to escape from Artsob to EBird. Feel free to report issues, and I'll do my best to solve them. Contributors absolutely welcome!