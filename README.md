# EdgeCollectionsEditor
Python Utilities and GUI for managing Edge Collections

# Package Deprication
While developing this package I came to the conclusion that Microsoft is currently hosting all recent Collections data exclusively in the cloud. There are a few indcators that led me to this conclusion:
  1. `collections_prism` is the only Table that has been updated in my Collections Database over the past 3-4 months (all the other tables are severly out of date).
     * *I will also note that prism id's are different from the original GUID's*
  2. At the bottom of Collections Sidebar there is a link labeled "Enabled by Microsoft Bing"; clicking on it will open a webview of your Collections located on bing.com 
  3. I tried manually resyncing my Edge profile/data but this did not update the Database

Unfortunately, I didn't figured all this out until I had a good amount of the infrastructure implemented. In hopes that it might some day be useful again I'm leaving this up on GitHub. If you can find a use for it, you're welcome to it. Likewise, if I find out that Microsoft has gone back to storing Collections locally, I'll resume work on this Package.

## Resources
Beyond the functions, utilities, and enums available, the package also provides the following:

#### CLI
`python -m EdgeCollectionsEditor` invokes a CLI tool which also you to perform simple queries and sampling of a Collections Database.

#### GUI
There is a partial gui available at `python -m EdgeCollectionsEditor.gui`. It was intended to be more comprehensive, but development was stopped due to the Package being Depricated.

#### Obsidian Notebook
An Obsidian-Flavored Markdown Notebook is included documenting the Database's Schema. The Table Index includes the most recent date the Schema was queried.