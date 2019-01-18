# vivian

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0d43ebb0ce5e4276b308132eec2644d9)](https://app.codacy.com/app/wizardbyron/vivian?utm_source=github.com&utm_medium=referral&utm_content=wizardbyron/vivian&utm_campaign=Badge_Grade_Dashboard)

vivian is a multi thread CLI for veirfying a large number of URLs redirection. It's easy to integrated with CI in smoke or regression test.

## Installation

```shell
pip3 install vivian
```

or

```shell
pipenv install vivian
```

## Usage

You can load a large number or URLs redirection pair from a `.csv` file. Like this `example.csv`:

```csv
http://www.github.com, https://www.github.com
http://www.google.com, https://www.google.com.hk
```

Then you can virify the url pairs via vivian:

```shell
vivian -f example.csv
```

And you will get these output:
```
load test case from example.csv
2 cases loaded running in 2 threads
verifying http://www.github.com
verifying http://www.google.com
FAIL:{'status_code': 200, 'origin_url': 'http://www.google.com', 'expect_url': 'https://www.google.com.hk', 'dist_url': '', 'redirect_count': 0, 'is_match': True, 'is_pass': False, 'auth': {}, 'err_msg': ConnectionError(MaxRetryError('None: Max retries exceeded with url: / (Caused by None)',),)}
1/2 PASS in 75.46944499015808 seconds
```

here is the explaination for the output：

**status_code**: the http status code of last request. 
**origin_url**: the url you request in the file.
**expect_url**: the url you expect in the file.
**actual_url**: the destination url you get when you made a url request.
**redirect_count**: how many redirection happened when you request from origin url.
**is_match**: if `expect_url` is same as `dist_url`, this value would be True, else it will be False.
**is_pass**: if the last request http status code between `200` to `399` and `is_match` is Ture, this value would be True, else it will be False.

## Best Practices

### TDD for Redirection

Before you write url rewrite rules in `nginx.conf` or `.htaccess`, you can write the rules as test cases in the `.csv`. The flow will be like `Green-Red-Green` in a TDD style. It is a good way to protect your exsisting http server configure and you can refactor the configure with fully confidence.

### Integrated with CI Server

You can keep the test case file as in your codebase as regression test or smoke test after deploy or changed http server congiuration.

## License

[MIT License](./LICENSE)