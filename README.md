# Outlet Placer

Thank you for taking the time to do our coding challenge. Below you'll find instructions and info you need to complete this exercise.

One of the things we do at Social Construct is to [programmatically create building details](https://techcrunch.com/2020/07/14/social-constructs-computer-optimized-buildings-could-shake-construction-industrys-foundations/) based on floor plans. In the following problem, you'll place outlets in a sample studio apartment according to rules of the 2017 National Electric Code on outlet spacing.

## Some Background
All of Social Construct's cables, pipes, and assorted in-wall infrastructure live under the floor as part of our raised-floor system. Floorboards sit on top of support structures called "pucks", which come in 3 sizes: 4"x4", 4"x2", and 2"x2".

![Raised-floor system](https://techcrunch.com/wp-content/uploads/2020/07/floor-wiring.jpg)

## Files and Folders
The [/json](https://github.com/SocialConstruct/outlets/tree/master/json) folder contains all the data files you need to get this project started.

* [json/studio_info.json](https://github.com/SocialConstruct/outlets/blob/master/json/studio_info.json) contains the coordinates in WCS for all the rooms, windows, and doors of this sample studio apartment. The coordinates are based on a [simplified floor plan](https://github.com/SocialConstruct/outlets/blob/master/png/studio_simple.png?raw=true). You can see the detailed floor plan [here](https://github.com/SocialConstruct/outlets/blob/master/png/studio_detailed.png?raw=true).
* [json/floor_info.json](https://github.com/SocialConstruct/outlets/blob/master/json/floor_info.json) contains the coordinates in WCS for all floors and pucks of the SoCo flooring system for this sample studio apartment.

Both files store coordinates in WCS and as **decimal inches** in the format of `(x,y)`.

The [/png](https://github.com/SocialConstruct/outlets/tree/master/png) folder contains reference images for this studio apartment, including a [possible final solution of outlet locations](https://github.com/SocialConstruct/outlets/blob/master/png/studio_with_outlets.png?raw=true). You can see the sample final solution including floors, supports, and outlet locations [here](https://github.com/SocialConstruct/outlets/blob/master/png/studio_final.png?raw=true)

If you're familiar with the DXF file format, you can find the relevant files inside the [DXF folder](https://github.com/SocialConstruct/outlets/tree/master/dxf)

## Rules of Outlet Placement
Here are basic rules of electrical outlet placement per the NEC rules:
* The maximum distance to a receptacle (outlet) along a wall is 6 feet (72 inches)
* A wall is defined as any space longer than 2 feet (24 inches)
    * Wall space includes the space measured around corners
    * The wall space continues unless broken by a doorway (aka, doors **do not** count towards the length of a wall segment)
    * The space occupied by windows counts as wall space (aka, windows **do** count towards the length of a wall segment)
* The following illustration may be helpful in visualizing the above rules:

![Another Rules Summary](https://www.naffainc.com/x/CB2/Elect/EImages/outletsneeded.gif)

### Other Rules
* For this example problem, kitchens do not count as wall space (they have their own set of rules, which we'll ignore for simplicity's sake)
* You can ignore bathrooms and closets
* All windows in this floor plan have floor-to-ceiling glass. Therefore, outlets cannot be placed in front of them (even though they count as wall space)
* SoCo outlets are 2" deep and 4" wide
* Outlets must go in-between pucks (the feet / supports of the SoCo raised floor system)
![Allowable Configuration](https://raw.githubusercontent.com/SocialConstruct/outlets/master/png/allowable_configuration.png)

## Submittal
Your solution should use the minimum number of outlets while satisfying all the rules above outlined above. Please submit a {your_name}.zip file and make sure the following are part of your submission:
* **outlets.json** - a file containing the coordinates in WCS for outlet locations. You do not need to include the full geometry of the outlets, though you are welcome to.
* **outlet_placer.py** - with your solution
* **solution.md** - a brief explanation of what you did and why. There are some questions in there that are meant to act as guides rather than a "lab report"
* any other supporting files

We mainly want to see your code, and strongly prefer Python. If you have a strong preference for another language, you may submit your solution that way, but please include an explanation as to why.

## Helpful Resources
You can use whatever open source libraries you think might be helpful in solving the problem. Some of our favorites include:

* [Shapely](https://pypi.org/project/Shapely/) is a helpful Python library for manipulation and analysis of planar geometric objects
* [PuLP](https://pypi.org/project/PuLP/) and [Google OR Tools](https://developers.google.com/optimization) include powerful optimization tools
* Autodesk provides easy [online viewers](https://viewer.autodesk.com/) for various CAD files
* Receptacle [spacing requirements](https://www.ecmag.com/section/codes-standards/article-210-branch-circuits-6) per the 2017 NEC, if you're curious about the rules. The relevant sections are 210.52(A)(1) and 210.52(A)(2)

## Other
We provided an illustration of one sample solution, though there are many others that satisfy the constraints given. We don't expect you to arrive at this exact solution. Do not worry about symmetry or aesthetics of your final solution. We want to see how you think, and how you approach problems. We're looking for functional, readable code rather than perfection.
