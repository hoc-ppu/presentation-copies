# presentation-copies

Automates the process of creating a presentation copy of a speech made in the commons.
An MP either asks the [Vote Office PET team](https://parlinet.parliament.uk/teams/house-of-commons/chamber-participation-team/vote-office/publications-enquiries-team/) or [Hansard](https://guidetoprocedure.parliament.uk/articles/v6wxttYz/how-to-make-a-maiden-speech) for a copy of their maiden speech.
Or on occassion MPs or other external organisations/people request presentation copies of speeches for other reasons such as ceremonial or memorial reasons.

## What the project does
Creates an XML file of a MPs speech using a link either from the hansard website or using the commons library index.
The XML file can then be imported into an indesign template which will then create a front presentation page followed by a copy of the speech from Hansard.


### How it works
* Insert Link into presentations-copies-script
* Link helps to find content from two Hansard APIs
* The end of the URL has FindDebateByContributionId
* [Hansard Search FindDebateByContributionId](https://hansard-api.parliament.uk/swagger/ui/index#!/Search/Search_FindDebateByContributionId)
* The data returned has a DebateSectionExtId, which the script uses to find the full details of the debate
* This is in the [Hansard Debate](https://hansard-api.parliament.uk/swagger/ui/index#!/Debates/Debates_GetDebate)
* The speech itself can then be found by using the contribution ID that is collected from the URL earlier

## Why the project is useful
There are currently 335 new MPs since the July 2024 general election. Between July and September over 230 MPs have made their maiden speeches and so far (Oct 24) the PET team have processed 70 requests.
The PET team were using word to create these which is not a print layout software and it is very time consuming.
This takes a 30+ min process into a process which takes a few minutes.

## How the production team can use the program
* create an executable by running the "create_exe.bat" file
* look at the documentation in [click u]p (https://doc.clickup.com/2530356/p/h/2d71m-2252/f6e5d6a432c411d?_gl=1*l12icp*_gcl_au*MjA4OTI5MjYwNS4xNzMzNzU5NDQw)

## How to use this program without the executable
### Users will need
* A code editor - Our team uses VSCode
* Indesign Template
* The [Hansard website](https://hansard.parliament.uk/) or the [library index spreadsheet](https://commonslibrary.parliament.uk/research-briefings/sn04588/)
* Member name, date of speech or debate
* a virtual environment
* install the packages (please see scripts - I will update this part of the readme)

### Create XML - With GUI
* Run the production-gui python file
* Opens a GUI, which asks for the website URL and for a folder location
* Saves the XML for the speech in the shared folder

### Create XML - Without GUI
* insert link into the presentation-copies-script python file
* Run the script
* the file will save in this project folder

### Steps for using the data in indesign
#### For producing one PDF at a time
* Indesign template can be found in PPU sharepoint under Technology Team / projects / Current Production
* Open template
* File > Import XML > Use browse function to go to where data was saved
* Click OK when window prompt offers some options/ default is fine

#### For producing lots of documents at once (both pdf and indesign files)
* all the data needs to be ready in one file
* follow steps for ensuring your indesign has access to the team scripts folder called PPU ID Scripts - update this step
* open indesign > windows > utilities > scripts
* click on scrip called batch import xml to indd pdf
* select the appropriate output and input folders and files
* export as high quality print
* the documents will save in the selected folders

## Where users can get help with your project
Nikki in the Tech team in PPU

## Who maintains and contributes to the project
The Tech team in PPU