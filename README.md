# Puddy For Poetry Writing
#### Video Demo:  <https://youtu.be/0Kd6iLgwf84>

#### Website URL: <https://puddy-poetry.onrender.com/> 
**_Disclaimer:_** Site may take upwards of 30 seconds to load. This version of the website uses the latest commit called **render.com version commit 1** with the SHA **4499a3f** since [render.com](https://render.com/) the service I used to host the server doesn't work with [Prosodic](https://pypi.org/project/prosodic/) which I use for meter checking so unfortunatley I was not able to roll out that feature the **full version** commit with the SHA **380657f** is the complete website 
#### Description:


## What this project is about:
This is a website that helps poets or anyone interested in writing poetry to write more efficiently. It tries to group all the tools needed to make writing easier such as rhyme checkers, syllable checkers all possible with  [**The CMU Pronouncing Dictionary**](http://www.speech.cs.cmu.edu/cgi-bin/cmudict), a huge database of poems to get inspired by which is provided by [**PoetryDB's API**](https://poetrydb.org/index.html) as well as a plethora of rhyming words, synonyms, antonyms and their meanings all in one place provided but the [**Datamuse API**](https://www.datamuse.com/api/).

## How to use?
I have worked hard to make sure the website is as straight forward as possible but here's a quick tutorial for you:

#### **1.Register/Sign in(optional but recommended)**
![](README_imgs\puddy_tutorial_1.jpg)

#### **2.Create Your Poem**
![](README_imgs\puddy_tutorial_2.jpg)

#### **3.1.Setup your poem**
![](README_imgs\puddy_tutorial_3.jpg)
The options highlighted in yellow have the edit mode feature which is explained if you choose the rhyme scheme and scroll down where everything is explained with examples when possible.

#### **3.2.Customize Your Setup**
![](README_imgs\puddy_tutorial_4.jpg)
The rhyme repetition field may seem confusing at first but if you scroll down and look at the description provided you can see that there are examples that explain how it works for every rhyme scheme taking monorhyme as an example:
* If you keep it at 0 your poem will be one line long with 
* At 1 your poem will be two lines long since we are repeating the rhyme scheme (A) once.

This varies with each rhyme scheme just make sure to scroll down for more info after choosing your rhyme scheme.

#### **4.Writing Your Poem**
![](README_imgs\puddy_tutorial_5.jpg)
This is pretty straightforward to the top right is your utility box with all your tools and at the bottom is where you can save your poem as a draft or a final poem. 

What's the difference?

* Draft:
One same poem can have multiple drafts this encourages exploring multiple avenues and through trial and error creating the perfect poem.(Your notepad is saved with each draft or poem)

* Poem:
whereas a poem is final and can only be edited, it is the final product.

#### **5.Viewing Your Work**
![](README_imgs\puddy_tutorial_6.jpg)
Simply click the account button and browse your drafts and poems that you have created, this is also where you can view, edit and delete them.

Tip: Checkout the settings to customize your writing experience even further and discover shortcuts!

## Breakdown of all the files

**The static folder** contains:
* The *Icons folder* which holds all icons
* The *js folder* which holds all the javascript needed for each page
* All the *pictures* used in the background of the website
* *Styles.css*

**The templates folder** contains all the templates of each page aswell as *macro.html* which is used in some templates.

**app.py**  is where the bulk of the application is present.

**database.db** is where my database resides

**database.py** is where I setup my ORM with all the objects I use throughout my application. The table names are self explanatory.

**forms.py** is where everything WTForms related resides to make the forms in my website easier to setup and safer to use.

**helpers.py** is where I have all of my rhyme checking and syllable checking functions in addition to the classes used for the rhyme schemes before they are saved in the *CurrentUnsavedPoem* table.

**requirements.txt** is where all the depencies of my application are.