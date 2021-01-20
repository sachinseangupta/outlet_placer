Outlet Placer is a geometric optimization tool that schematically places electrical outlets in a room according to design constraints and National Electrical Code (NEC) rules. This was a take home test made publicly available by the San Francisco-based housing startup Social Construct for their computational geometry role (which can be found here: https://github.com/SocialConstruct/outlets). I used this test as a technical exercise to develop my software development skills.

![OP_combined](https://user-images.githubusercontent.com/63329231/105243232-c965f600-5b3c-11eb-942c-ae64f509248d.png)

The purpose of this tool is to place the minimum number of electrical outlets required for a NEC-compliant space with rooms of predetermined sizes and with floor supports that had to be avoided. I modeled the 2D room layout, floor supports, and outlets using the Shapely geometry library and utilized the blackbox optimization tool RBFOpt for the actual optimization procedure. A succint explanation of how blackbox optimization and RBFOpt work can be found here: https://developer.ibm.com/technologies/analytics/projects/rbfopt/.




