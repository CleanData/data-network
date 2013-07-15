# App Roadmap

The Clean.Data. app highlights:

* quality data sets
* issues with existing data sets
* connections between datasets

In a first version it does not:

* require user login
* provide hosting

### Tech Stack

* backend - mySQL or postgres
* middleware - python, using the Django framework (powers Pinterest and many other large scale sites)
* frontend - Django templating, using twitter-bootstrap for responsive grid based layout, and D3.js for graph visualisation. Also expose API endpoints to allow dynamic updates of elements of the site (quering the connections of a node for example)
* currently running on Dreamhost - using Jon's personal server. But we'll move this to an AWS instance very shortly using the ACRE perk of free startup hosting.



## Minimum - store, search and display connections between datasets

The bare minimum functionality is to show a map of the connections between datasets. An example view:

![image](https://dl.dropboxusercontent.com/u/70519/datawebOutline.png)
Fig 1. Example inter-related data view

Here the Electricity Normalized by Zipcodes is the focal dataset. The map shows all the datasets that feed in, and the datasets that feed into that, as well as a subset of other sets that use the same resources. For example, the NYC Zipcode JSON is also used in VisioNYC and Mapping the Spread of the West Nile Virus.

### Underlying Model

We're storing meta-data about datasets, those that create and manage them, and those that collaborate on them. The network of connections between data sets for a directed acyclic graph (DAG). Each dataset has an asymmetric connection to other datasets (one is the source, the other is a derivative). One dataset can have many sources, and also many derivatives. To store this data, we use the model:

![image](https://dl.dropboxusercontent.com/u/70519/SuggestedDataStructure.png)
Fig. 2 - minimal underlying data structure

We cover the use of each of these in turn:

#### Dataset and data_relation

The DAG structure is encoded by the many-to-many relationship through the data_relation table. The plan is to store as much information about that connection as possible - so the how_it_was_processed field is a placeholder for now.

The fields in the Dataset class are a subset of the fields in the [Dataset](http://schema.org/Dataset) object on [Schema.org](http://schema.org).

Dataset and data_relation encode all the information shown in Fig. 1

Note that datasets with no sources are a special subset - they are the raw datasets, and should be highlighted/easily searchable.

#### Data catalogs

Data catalog allows for collections of data. It has a one-to-many relation with datasets (a dataset can only be part of one catalog)

#### Format

Each dataset has a format, whether it's an API that returns JSON, or a pdf, or an excel spreadsheet. **We need to compile a list of all data types, and links to the definition of those data types.** Functionality - we should allow users to add a data format if it doesn't exist. Extra functionality - we should scrape the data source and check that the listed format matches the actual data format.

#### Licence

Each dataset has one licence associated with it. **We need to compile a list of the possible licences and links to the relevant definitions. Sue's taking this on.** Functionality - do we need the ability for a user to add a new license, or just to flag a missing license definition?

#### User Profile

The UserProfile class is mapped to users through a one-to-one relationship. This allows for the extension of the Django User class, which allows us to leverage all the power of the authorization libraries, logins, sessions, without having to write any code. The details of the UserProfile class just encode relationships at this stage. Every dataset has one manager, so that there's one point of contact for the dataset. Every dataset can have many collaborators - encoded through the contributors_to_contributions many-to-many relationship.

Two users who have relationships to the same dataset are related through the collaborators relationship. This is a symmetric many-to-many. **Note that we need to make sure this relationship is auto-populated when a new interaction with a dataset is introduced**

#### contributors_to_contributions

This many-to-many relationship encodes interactions between a collaborator and a dataset. At the moment this is just a single involvement, but could (and perhaps should) be extended to encode each interaction, to allow for a living history of interactions with a dataset. On the plus side, that provides a lot of useful data. On the downside, that's unlikely to ever be even close to complete and accurate.

#### Organization

Many datasets are maintained by organizations. Hence we need a structure to define those, and their relationship with data. The data/catalog to organization relationship can be null.

#### **Categories and tags

We need category and tag functionaltiy for a rich taxonomy.

### Functionality

#### Viewing connections between datasets

* construct a dynamic view like Fig.1, from a JSON of the links between datasets, and a JSON of the nodes.
* clicking a node brings up more information, and the option to focus the graph on that node.
* This centered view should have a unique url, so that people can link to the data-graph of a dataset
* needs an interactive element on the joins that allows access to the 'how this was processed' information.
* should be able to toggle different metrics, like licence/date-last-edited/date-created to change colour/size/etc.

#### Search for a dataset

* anyone must be able to search for a dataset
* to start with let's stick with name/url as search fields
* need a search box that runs a query\
* **Need to optimise, and probably do something like a DAG module to allow for efficient querying of relationships**

#### View a user network

* just as there's a many-to-many relationship between datasets, there's a many-to-many relationship between collaborators
* click a user node to bring up info
* need a means to edit/update information - but only if the editor is logged in, and possibly approved?
* clicking a link between users will reveal the dataset they worked on together.

#### Enter a dataset manually

* we need a form view to enter a dataset. This needs to closely mimic (but reskin) the admin structure, allowing for the creation of related objects like users and licenses inside the dataset definitions.

#### Bulk add a dataset

* we're going to generate a lot of sub-data sets that we want to feed in. We're not going to do this one-by-one by hand. One (efficient) option is to have this run on the command line server side via a script. Another is to provide a bulk-add UI widget.

### Required Resources

* Hosting - AWS, provided by ACRE perks - **sorted**
* overall project architecture - server set-up, interface with Github repository - allowing code to be pushed to the server automatically, responsibility for managing dependencies. Jon can take ownership of this, but **a professional web developer is a better bet.** Should be a minimal jo after the set-up.
* data model - DAG specialists. Definitely something Google has a lot of experience with. **A consultant on this would be suepr helpful.**
* Optimising db calls. This should be easy enough to start with. **A data architect to consult on database structuring would be really helpful**
* Controller coding - ESF devs and Jon. Two(+1) developers already assigned (minimal views) - **sorted**
* Front end functionality - JSON interface with D3 and twitter bootstrap. Jon can do this, but would be better if this were someone else. **We're short a UI developer. Riggs offered help from HB?**
* Front end design - logo, branding, UI design. **We need a talented designer, I know one, and there's also Adam who was on the EW board and might be able to help out.**

## Minimal Content

Once the platform exists in minimal form, the challenge is to get content onto the site.

There are two ways to get data into a database:
* using the live web-app to enter data sets one by one.
* automating the retrieval of data using scripts.

The first case is easy, but labor intensive. It needs a person to add sets one by one. The second case will be much faster (potentially), but needs people with coding experience.

### Workflow for scraping a new dataset

* set up a new folder in the github repository
* write a scraping algorithm in whatever language is most familiar to the coder
* generate a file with the structured data

Then this structured data can be added into the test-app database, and re-added if there are any database problems. By keeping this workflow distinct we can utilize a much broader base of coding experience than just python.

### Datasets

We need to identify the first data sets to add in. I'd argue that https://data.cityofnewyork.us/ is a good place to start as there's a lot if interconnected data, and can be hooked into Pediacities data.

### Required Resources

* Subject matter experts - to create a comprehensive list of available datasets. **As many as we can get**
* Data entry - need people to volunteer to take responsibility for different data sources. Some will be entered one by one - no code background required. Other datasets will be scraped (like the NYC data portal) - which requires some coding in whatever language people are happiest with. **as many coders as we can get, CUSP researchers to add their data, any data analyst from the Data Jam willing to put in time**
* Example code for scraping - Jon

## Extensions

Once the minimal model is complete, it's straightforward to start adding new elements into the site. There are two types - new views for the existing data, and new Django modules that extend the data model.

### User login

We want users to login and take ownership of their datasets. This is a prerequisite for much of the other extensions. Django has a rich user interface built in. We are unlikely to need to do much work to get this up and running. Minimal data-model adjustments. Mostly front end view coding.

### Extended data view

Add view functionality to plot data, summarise the structure of the data (number of lines/columns) etc. Very similar to what is offered by CKAN. Lots of front end coding (D3), and some backend work to pull in the dataset from the remote repository when required. No adjustment to the data model

### Graph-view of data scientist relations

A new view that shows the relationship between data-scientists via the collaborator relationship. Parallels the graph view of interconnected datasets. 

### Rating sets and flagging problems

Add a new module to the application that allows other users to rate datasets. Provide fucntionality to flag issues with a dataset - if some percentage of the lines are NaN for example, or if the set is incomplete.

Should also allow for the capacity to ask/answer questions.

### Reputation points

Implement a Stackoverflow credit system for work done on datasets. Allow users to provide points when answering questions or solving problems. Provides the ability for the site to be used by companies looking for data scientists.

### Interface with GitHub

GitHub has an API that allows for applications to much of GitHub's functionality. This would allow users to create a GitHub repository for their dataset, with the data-view provided by Clean.Data. site.

### Hosting

Offer the option to host data sets. This is a hard problem, as the site needs the facility to cope with large data-sets, guarrantee integrity, and insure against loss of data-sets during any down time. The plus-side is that we get much more fine grained and direct access to the meta-data about datasets (when they are updated, by whom, and what was done)














