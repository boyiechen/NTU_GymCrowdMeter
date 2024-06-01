# NTU_GymCrowdMeter
This is a project that tries to webscrape the instant crowd meter of NTU Gym, and perform visualized analysis

To run the cronjob
```shell
*/5 * * * * /usr/bin/python3 /home/boyie/repo/BerkeleyRSF_CrowdMeter/main.py
*/5 * * * * /usr/bin/python3 /home/boyie/repo/NTU_GymCrowdMeter/main.py
*/23 * * * * /usr/bin/Rscript /home/boyie/repo/BerkeleyRSF_CrowdMeter/rshinyapp/cleanData.R
*/29 * * * * /usr/bin/Rscript /home/boyie/repo/BerkeleyRSF_CrowdMeter/rshinyapp/modelData.R
*/23 * * * * /usr/bin/Rscript /home/byoie/repo/NTU_GymCrowdMeter/rshinyapp/cleanData.R
*/29 * * * * /usr/bin/Rscript /home/boyie/repo/NTU_GymCrowdMeter/rshinyapp/modelData.R
*/30 * * * * /bin/bash /home/boyie/repo/gitpush.sh
```
