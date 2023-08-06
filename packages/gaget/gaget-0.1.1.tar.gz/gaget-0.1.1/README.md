# Gaget

Download customer files from Google or Amazon storage. 

## Installation

Install and update from the Git repo using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
 pip install git+https://github.com/ConductorTechnologies/gaget.git
```

## Requirements
You must have credentials that allow you to read from both Google Cloud and Amazon S3.

[Set up authentication for Google](https://cloud.google.com/datastore/docs/reference/libraries#setting_up_authentication)
[Set up authentication for Amazon](https://console.aws.amazon.com/iam/home#/home)

## Usage

Gaget is a wizard. There are currently no command-line arguments. 

To download a customer's files, open a shell and type:

```bash
 gaget
```

Then follow the prompts.

### A typical session

1. Customer's job was run on GCP

```bash
(gaget) julian@papaya:~/dev/conductor > gaget
Enter the account name or number: Marte
Found account. Name:Marte, ID:5706504271298560
Enter the job ID:00671
Found job. with jid:00671, ID:4624804851482624
Hit return to use the default destination directory : /Users/julian/dev/conductor/Marte/00671
Enter a relative path to add subdirectories. For example: Enter my_sub_dir to use /Users/julian/dev/conductor/Marte/00671/my_sub_dir
Enter an absolute path if you want to ignore the default altogether. For example: /path/to/downloads/my_project.
: /Users/julian/foo
Found GCS Files Blob:/atomic-light-001/accounts/5706504271298560/blobstore/746ff273f45c46f78b528a494a3c59bf. Extracting files list JSON
Downloading files from GCP...
  0.0%       1/1566    96.5 Kb accounts/5706504271298560/hashstore/678e33169e734adee0c1b11a3634a505 -> /Users/julian/foo/msettings/OCCIO/aces_1.0.3/luts/V-Log_to_linear.spi1d
  0.0%       2/1566   797.3 Kb accounts/5706504271298560/hashstore/82cd6734f09ddf680b8d95a5dde95322 -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/data/GEO_CACHE/Rama_Tucan/Ramita_06_hojasFrame73.mcx
  0.0%       3/1566   650.2 Kb accounts/5706504271298560/hashstore/3cdc65cd55fe4141be7543d7447b552d -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/data/GEO_CACHE/Rama_Perezoso/HojasFrame97.mcx
  0.0%       4/1566     7.1 Kb accounts/5706504271298560/hashstore/f9b85e7695905b98689f20863a0d72e6 -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/data/GEO_CACHE/Rama_Tucan/polySurface2_HojasFrame77.mcx
  0.0%       5/1566     9.2 Mb accounts/5706504271298560/hashstore/2832f1461cf8e851ab59db94023bc108 -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/workspace/Herman/textures/Sloth_TeethDiff.tx
  0.0%       6/1566   650.2 Kb accounts/5706504271298560/hashstore/26eacbe33b6eb233ddf8f81a736de833 -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/data/GEO_CACHE/Rama_Perezoso/HojasFrame137.mcx
  0.0%       7/1566    12.1 Kb accounts/5706504271298560/hashstore/f0960286bb916422d991a92b041e4eb4 -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/data/GEO_CACHE/Rama_Tucan/polySurface19_HojasFrame25.mcx
  0.0%       8/1566     1.1 Mb accounts/5706504271298560/hashstore/739610d99d3efb64d8d3c7a5f79af126 -> /Users/julian/foo/Projects/LIZANO_2020/Maya_Project/data/GEO_CACHE/Rama_Fondo_Top/HojasFrame15.mcx
^CKilled by user
```

2. Customer's job was run on AWS

```bash
(gaget) julian@papaya:~/dev/conductor > gaget
Enter the account name or number: AM_Design_and_Rendering
Found account. Name:AM_Design_and_Rendering, ID:5767635104169984
Enter the job ID:00054
Found job. with jid:00054, ID:6193411666477056
Hit return to use the default destination directory : /Users/julian/dev/conductor/AM_Design_and_Rendering/00054
Enter a relative path to add subdirectories. For example: Enter my_sub_dir to use /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/my_sub_dir
Enter an absolute path if you want to ignore the default altogether. For example: /path/to/downloads/my_project.
:
Found GCS Files Blob:/atomic-light-001/accounts/5767635104169984/blobstore/bf02dc879788406c820eb91680e6ec90. Extracting files list JSON
Couldn't fetch files from Google for account/job: 5767635104169984/6193411666477056, Checking Amazon...
Downloading files from AWS...
  0.0%         1/11    26.2 Mb 5767635104169984/data/d1c533015850697753952875b7681ef3 -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/3D Design Elements/3D/IBLs/small_cathedral_02_4k.tx
 37.2%         2/11   283.0 Kb 5767635104169984/data/7d39331064b9aa5ea4d43ea0ce698feb -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Cleveland Holmes/Liquor Bottle Renders 0720/Textures/Bottle_Label_navy_silver.png
 37.6%         3/11   315.4 Kb 5767635104169984/data/d2f80d6e79a822181595e9de0719679e -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Cleveland Holmes/Liquor Bottle Renders 0720/Textures/Bottle_Label_ALPHA.tx
 38.1%         4/11     1.8 Mb 5767635104169984/data/e19ab9600333e3a684b4b437f4a71aad -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Nimblejack Partners/Flyer1_061120/Images/Cork_BUMP.tx
 40.6%         5/11     8.1 Mb 5767635104169984/data/ebade7ed3d302ae9866847ac5a987749 -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Cleveland Holmes/Liquor Bottle Renders 0720/Maya Files/scenes/Openly_Liquor_Bottle_071420.ma
 52.2%         6/11   288.3 Kb 5767635104169984/data/adde9d4cf2900582ac31f3e398074aff -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Nimblejack Partners/Flyer1_061120/Images/Cork_BUMP.jpg
 52.6%         7/11     1.3 Mb 5767635104169984/data/d290bb19587ae507951f2b638e1875e0 -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Nimblejack Partners/Flyer1_061120/Images/Cork.jpg
 54.5%         8/11   100.2 Kb 5767635104169984/data/93be8f8bf266d9074200e95c37a229ae -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Cleveland Holmes/Liquor Bottle Renders 0720/Textures/Bottle_Label_ALPHA.png
 54.6%         9/11    23.6 Mb 5767635104169984/data/d6df9c09542b198a98d9d9e461dfb053 -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/3D Design Elements/3D/IBLs/small_cathedral_02_4k.hdr
 88.2%        10/11     7.5 Mb 5767635104169984/data/f9373ed8cbdb5724b7a27963db7893ad -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Nimblejack Partners/Flyer1_061120/Images/Cork.tx
 98.9%        11/11   794.0 Kb 5767635104169984/data/62b66e7f15b1b72b73b44787f06b37f9 -> /Users/julian/dev/conductor/AM_Design_and_Rendering/00054/AM Design/02 Freelance/Clients/Cleveland Holmes/Liquor Bottle Renders 0720/Textures/Bottle_Label_navy_silver.tx
Done downloading 11 files from Amazon
```


### Contributing.