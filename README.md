# barcode-levenshtein-search
Boone Lab collaboration to locate, identify, link, and summarize DNA barcodes found in fastq files

This is an experiment with Thuy Nguyen to leverage the multiprocessed Levenshtein algorithm to find sequences in 68 ~1GB fastq files.

## Summary
* We are expecing around 1600 template reads (reference)
* Each fastq file name is assigned an experiment ID
* Each fastq file has at max ~8m reads (worst case total of ~544m reads)
* Each fastq file has the experiment ID embedded in the filename
* Every experiment ID will have a name (ref. Thuy's excel file)
* Every sequence will have the U1 sequence (use Levenshtein alg of max error 2)
* The barcode will lie AFTER the U1 sequence. Use this sequence for analysis

## Complexity
* Time
    * 2 Levenshtein reads per sequence: 1 for U1 ID, 1 for barcode ID.

## Input data type:
* Seq: fastq
* Experiment name: csv
* Reference seq: csv
* U1 seq: txt

## Workflow
* 68 fastq files (experiments):
	* Multiprocess operations for 1 file:
		* Export as summary CSV file for each file.

## Caveats
* If the reference barcode has '-' or 'N', keep those as wildcards and don't add to the Levenshtein number.
    * Furthermore, jot these gene's down as wildcards in    the excel file provided by Thuy.
* To add to the '-' rule...
    * E.g. ACGG--TTG
    * This should be interpreted exhaustively:
        * ACGGNNTTG
        * ACGGNTTG
        * ACGGTTG
    * Each of these sequences are still under ACGG--TTG
    * We ignore N and do NOT add to the point score (rather treat as a match)
