import re

iosxr_log_pattern = r"%(\w|\w_)+-(\w|\w_)+-\d-(\w|\w_)+" 

print(re.match(iosxr_log_pattern, "RP/0/RP0/CPU0:Nov 21 16:38:47.134 KST: SSHD_[65584]: %SECURITY-SSHD-6-INFO_SUCCESS : Successfully authenticated user 'skbdnms' from '211.117.39.100' on "))