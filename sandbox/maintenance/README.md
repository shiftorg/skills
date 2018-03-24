
# maintenance

This section of the sandbox holds miscellaneous files used to perform maintenance on the data used in this project.

`SkillBucket.py` contains a class used to interact with the S3 bucket used for development in this project. You can instantiate this class as follows:

```
from SkillsBucket import SkillsBucket
bucket = SkillsBucket()
```

`convert_salaries.py` was used to read salary data in the old format and transform it to ndjson.

old format:

```
[
    {...},
    {...},
    {...},
]
```

new format:

```
{...}
{...}
{...}
```

It expects to read data from the `salaries/` prefix in the S3 bucket and write it to `salaries_ndjson/`. If you need to re-run this for any reason, use:

```
python convert_salaries.py
```

Note that the script expects you to have placed your AWS creds in an [AWS credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html).
