Outlet Placer is a geometric optimization tool that schematically places electrical outlets in a room according to design constraints and National Electrical Code (NEC) rules. This was a take home test made publicly available by the San Francisco-based housing startup Social Construct for their computational geometry role (which can be found here: https://github.com/SocialConstruct/outlets). I used this test as a technical exercise to hone my software development skills.
![OP_combined](https://user-images.githubusercontent.com/63329231/105243355-f31f1d00-5b3c-11eb-98f1-407ecbd3d520.png)
*Figure: (Left) Provided space layout with walls on which outlets must be placed. (Right) Visualization of floor support locations and outlets.*



The purpose of this tool is to place the minimum number of electrical outlets required for a NEC-compliant space with rooms of predetermined sizes and with floor supports that had to be avoided. I modeled the 2D room layout, floor supports, and outlets using the Shapely geometry library and utilized the blackbox optimization tool RBFOpt for the actual optimization procedure. A succint explanation of how blackbox optimization and RBFOpt work can be found here: https://developer.ibm.com/technologies/analytics/projects/rbfopt/.




