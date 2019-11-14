# YARN Log Splitter
A utility that splits huge yarn application logs and groups them in a structure that is very easy to analyze like below.
```
output-dir/
|--- containers/
     |--- container_e140_1527921028874_0033_01_000001/
          |--- syslog
          |--- stdout
     |--- container_e140_1527921028874_0033_01_000002/
          |--- syslog
          |--- stdout
|--- hosts/
     |--- nodemanager-1.example.com:45454
          |--- container_e140_1527921028874_0033_01_000001 -> output-dir/containers/container_e140_1527921028874_0033_01_000001
     |--- nodemanager-2.example.com:45454
          |--- container_e140_1527921028874_0033_01_000002 -> output-dir/containers/container_e140_1527921028874_0033_01_000002
```

- Inputs: Yarn application logs fetched using `yarn logs -applicationId <appId>`
- Output: Will create separate directories for containers, groups the logs per NodeManager and splits into separate files like stdout, stderr, syslog etc.

- Usage: ```python yarn-log-splitter.py <application log file> <output dir>```
- Example: ```python yarn-log-splitter.py application_1527921028874_0033.log output-dir/```
