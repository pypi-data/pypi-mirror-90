# ufes-tess-validator
The repository for performing automatic validation for tess upgrades of UFES clusters
 
## jenkins_validate 
The package is used to trigger a validator job in jenkins(http://10.148.183.183:8080/  may be other server IP), after building finished,it can also download artifacts and
calculate the passed rules percentage, if the percentage is bigger than 95, it shows validate successful, else it shows validate failed.

## how to use it
### install packages
```
   pip install jenkinsapi
   pip install jenkins-validate==0.0.12
```
### put the follow commands into a python script:
```import jenkins_validate
   from jenkins_validate import auto_validator
   auto_validator.jenkins_validate(param1,param2,param3,...)   

   #input the parameters,"clustername","web_type","jenkins_server" and "localpath_to_artifact_dir" are the Required parameters
   #when the parameter of pull_method = "LBMS", then the parameter "token" must be upload, it is your keystone token saved in a file.
```
### the way to get keystone token which can be used to get rules from LBMS
https://wiki.vip.corp.ebay.com/display/CLOUD/LBMS+User+Documentation+for+REST+APIs#LBMSUserDocumentationforRESTAPIs-Keystone-Based
### then run the python script.

