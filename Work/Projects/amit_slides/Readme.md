- Step 1: Have a "source" folder which is a private repo that contains
	- pics
	- private posts
		- remarkjs_public
		- reveal_private
	- public posts
		- remarkjs_public
		- reveal_public
	- inprogress posts
		- remarkjs_inprogress
		- reveal_inprogress
	- templates: How you want to style your webpages
	- password_template.html
	- pysrc/
		- This contains the python code that generates the webpages from the templates
	- direct_links
		- This folder contains .md files with single line that directly points to the html page

We now need to have a destination folder which is a public repo that contains only the static html files that are generated and served. In order to generate the html files etc, you need to make the softlinks to the source folder. 

- Step 2: Create a "destination" folder and
  - Copy the contents of BlankPrj
  - Run "python Main.py ../SourceFolder"
  - Run "python pysrc/newnewsubs.py password"


**Docker**

- docker build -t pelican-base .
- docker run -it --rm -v ~/test/amit_slides:/src -p 5000:80 pelican-base
