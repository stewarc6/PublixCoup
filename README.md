# PublixCoup
A Python Script to clip all available Digital Coupons from Publix

## Dependencies
* Python 3.7.6
* Firefox   [Webbrowser of choice]
* selenium  [Automated webbrowser control]
* psutil    [Process killing hammer]

## Usage
python3 publixCoup.py [-h] [-d] [-v] [-H] [-u USERNAME] [-p PASSWORD]

### optional arguments
* -h, --help            show this help message and exit
* -d, --debug           does not execute coupon clipping
* -v, --verbose         outputs logfile contents to console
* -H, --headless        Run Firefox Headless
* -u USERNAME, --username USERNAME
** Publix Username
* -p PASSWORD, --password PASSWORD
** Publix Password
