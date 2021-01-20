Outlet Placer is a geometric optimization tool that schematically places electrical outlets in a room according to design constraints and National Electrical Code (NEC) rules. This was a take home test (which can be found here: https://github.com/SocialConstruct/outlets) made publicly available by the San Francisco-based company Social Construct for their computational geometry role. I used this test as a technical exercise to develop my software development skills.

The purpose of this tool is to place the minimum number of electrical outlets required for a NEC-compliant space with rooms of predetermined sizes and shapes and with floor supports that needed to be avoided. I modeled the 2D room layout, floor supports, using the Shapely library and the blackbox optimization tool RBFOpt for the actual optimization procedure. A succient explanation of how RBFOpt works can be found here: https://developer.ibm.com/technologies/analytics/projects/rbfopt/.




