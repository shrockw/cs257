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
