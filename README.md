# CS257-F23-TeamTemplate
Template for long-term team projects
Team E: Marc, Willan, Allison, Anika 

**Command Line Usage Statments:**  

_Search for a recipe using include/omit filters_  
\<ingredients> should be a comma-separated list of ingredients enclosed in quotes  
Usage: python cl.py --search --include_ingredients \<ingredients> --omit_ingredients \<ingredients>  
Example: python cl.py --search --include_ingredients "chicken, rice" --omit_ingredients "onion, garlic"  
Alias: --search or -s  

_Get a random recipe by specifying how many to return_  
Usage: python cl.py --random \<number>  
Example: python cl.py --random 5  
Alias: --random or -r


_Get usage information/help_  
Usage: python cl.py --help or -h  
Alias: --help or --h  
Example: python cl.py --help  

**Flask Usage Statements:**

_Search for a recipe using include/omit filters_  
Usage: URL/search/\<str:include_ingredients>  
Example: /search/include/ingredient1,ingredient2/omit/ingredient3  

_Get a random recipe by specifying how many to return_  
Usage: URL/random/\<int:number>  
Example: URL/random/3  

The main form of navigation is a nav bar that you can use to go to the random page where the user can input a 
number of random recipes that they want and then click generate which will take the user to the display 
page where x amount of random recipes with be displayed.

## Scanability
- There is a large title the is consistent for each page and then a smaller header for each page
- The nav bar allows users to scan the things you can do with the website
- There is also a description of what you can do and where to navigate to on the home page
## Satisficing
- The navigation bar is large and at the top of the page where the user can find something similar to what they
are looking for
- There are labels on the input to tell the user to put a number and a generate button right next to it
## Muddling through
- The navigation bar stays with you on every page which allows the user to backtrack if they went somewhere they did not want to
- Buttons are intuitive with single word pages on the nav bar
- Inputs are labeled and clear what you are supposed to do