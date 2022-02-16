![CCIVR_LOGO](/Users/ohata/Dropbox/02 cisNATs in EMT/94 CCIVR logo/CCIVR_logo_ver3.png)


# CCIVR

## Overview
**CCIVR** (**C**omprehensive **C**is-NATs **I**dentifier **V**ia **R**NA-seq data) is a Python package tool, which facilitates the identification of entire cis-NATs (cis natural antisense transcripts) from gene datasets. CCIVR requires a CSV formatted input file that contains gene datasets with their locational information including chromosome number where the genes are on, their direction of strand, their transcription start site (TSS), and their transcription termination site (TTS), with or without expression profiling data including TPM, FPKM, fold-change, and padj (q-value) from RNA-seq. Then, CCIVR generates two CSV formatted output files: the table file contains entire extracted cis-NATs list accompanied by their structural characteristics including embedded (EB), fully-overlapped (FO), head-to-head (HH), and tail-to-tail (TT); the summary file contains the absolute number of each type of extracted cis-NATs with its percentages to the total genes. For more details, please see Ohhata T *et al*., *submitted*.

## Requirement

* Python 3.8+

## Installation

You can install CCIVR via a package manager "pip" by typing the commands as follows:  

```
pip install git+https://github.com/CCIVR/ccivr.git
```  

For checking whether CCIVR is correctly installed, please type the commands as follows:

```
ccivr --help
```
If this does not work, please check the setting of `$PATH` environment. 


The location of CCIVR installation can be found by typing the commands as follows:

```
pip show ccivr
``` 

## Input file preparation
For the CCIVR analysis, a CSV formatted file is required as an input file. The input file must contain five different gene annotations listed on their independent columns, as follows: 

- **id**: gene id of each gene. Example: ENSMUSG00000085715   
- **Chr**: chromosome number where the gene is on. Example: X
- **Strand**: the direction of strand. Example: +
- **Start**: the minimum number of the gene location. Example: 103431517
- **End**: the maximum number of the gene location. Example: 103484957

(The example above is the murine *Tsix* gene, from Ensembl GRCm39)  

The order of these five columns is changeable since CCIVR recognizes their characters but not their order.

These gene annotations can be obtained from the Ensembl database. 

Attaching other gene annotations is available during the CCIVR processing by adding extra columns including “GeneSymbol”, “gene source”, “gene biotype”, “GO analysis”, and so on in the input file.

Attaching information for expression profiling obtained from RNA-seq analysis is also available during the CCIVR processing by adding extra columns including “TPM”, “FPKM”, “fold-change”, “padj”, and so on in the input file. 

Please see [the test file] (https://github.com/CCIVR/ccivr/blob/main/data/TGF_test-data_ver2.csv) for an example of the input file. 
(The test file contains human gene datasets accompanied by expression profiling of Huh-7 cells with TGFß
stimulation, which is consistent with the input file used for the CCIVR analysis in figure 4 of our paper, Ohhata T *et al*., *submitted*)


## Usage

For running "CCIVR", please specify the absolute or relative path of the input file```[path of input CSV]``` and type the commands as follows:

```
ccivr [path of input CSV] 
```

By default, output files will be saved in the same directory of the input file. For saving the output files to the different directory, please add the optional argument and specify the absolute or relative path of the directory```[path of saving directory]``` and type the commands as follows:

```
ccivr [path of input CSV] --output [path of saving directory]
```

If it runs successfully, processing status will be displayed as follows (this is an example from running with [the test file] (https://github.com/CCIVR/ccivr/blob/main/data/TGF_test-data_ver2.csv)):

```
Reading [path of input CSV]
EB
Plus-to-minus extracting
Minus-to-plus extracting
FO
Plus-to-minus extracting
Minus-to-plus extracting
HH
Plus-to-minus extracting
Minus-to-plus extracting
TT
Plus-to-minus extracting
Minus-to-plus extracting
< Result >
total genes : 65065
genes with cisNats : 27351 [42.04%]
     EB : 8112 [12.47%]
     FO : 12194 [18.74%]
     HH : 5992 [9.21%]
     TT : 6097 [9.37%]
Writing the table to [absolute path of the file, ending with "Table.csv"]
Writing the summary to [absolute path of the file, ending with "Summary.csv"]
```

Two CSV formatted output files "Table.csv" and "Summary.csv" will be generated and saved in a new directory named "ccivr_output".  

**Table.csv**: it contains a list of all extracted cis-NATs pairs accompanied by their structural characteristics.  
**Summary.csv**: it contains the absolute number of each type of extracted cis-NATs with its percentages to the total genes. 

An example of "Table.csv" from [https://github.com/CCIVR/ccivr/blob/main/data/ccivr_output/Table.csv] (absolute path of the test tile), you can find [here](absolute path of Table.csv).

An example of "Summary.csv" from [https://github.com/CCIVR/ccivr/blob/main/data/ccivr_output/Summary.csv] (absolute path of the test tile), you can find [here](absolute path of Summary.csv).



To complete the whole process of CCIVR with [the test file] (absolute path of the test tile), it may take from a few to dozens of minutes by a standard-powered computer. (For example, it takes 6 minutes 34 seconds by iMac 2017, equipped with 3.4 GHz Intel Core i5)

## Uninstallation
When you no longer use the package, you can uninstall it from the computer by typing the commands as follows:

```
pip uninstall ccivr
```

## Authors
Tatsuya Ohhata conceptualized CCIVR. Maya Suzuki and Tatsuya Ohhata designed the CCIVR algorithm. Maya Suzuki implemented the CCIVR software.

## License
CCIVR is licensed under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).

## Reference
Ohhata T *et al*., *submitted*
