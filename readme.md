# NTU_GymCrowdMeter
This is a project that tries to webscrape the instant crowd meter of NTU Gym, and perform visualized analysis

To run the cronjob
```shell
*/5 * * * * /usr/bin/python3 /home/pi/repo/BerkeleyRSF_CrowdMeter/main.py
*/5 * * * * /usr/bin/python3 /home/pi/repo/NTU_GymCrowdMeter/main.py
*/23 * * * * /usr/local/bin/Rscript /home/pi/repo/BerkeleyRSF_CrowdMeter/rshinyapp/cleanData.R
*/29 * * * * /usr/local/bin/Rscript /home/pi/repo/BerkeleyRSF_CrowdMeter/rshinyapp/modelData.R
*/23 * * * * /usr/local/bin/Rscript /home/pi/repo/NTU_GymCrowdMeter/rshinyapp/cleanData.R
*/29 * * * * /usr/local/bin/Rscript /home/pi/repo/NTU_GymCrowdMeter/rshinyapp/modelData.R
*/30 * * * * /bin/bash /home/pi/repo/gitpush.sh
```
