import sys,pathlib


BASE_URL = "https://www.terabox.app/share/list?app_id=250528&web=1&channel=0&jsToken={token}&dp-logid={log_id}&page=1&num=20&by=name&order=asc&site_referer=&shorturl={short_url}&root=1"

TERABOX_URL = [
        "1024terabox.com",
        "www.mirrobox.com",
        "www.nephobox.com",
        "freeterabox.com",
        "www.freeterabox.com",
        "1024tera.com",
        "4funbox.co",
        "www.4funbox.com",
        "mirrobox.com",
        "nephobox.com",
        "terabox.app",
        "terabox.com",
        "www.terabox.ap",
        "www.terabox.com",
        "www.1024tera.co",
        "www.momerybox.com",
        "teraboxapp.com",
        "momerybox.com",
        "tibibox.com",
        "www.tibibox.com",
        "www.teraboxapp.com",
    ]


TOKEN_PATTERN = r"fn%28%22(.*?)%22%29"
DP_PATTERN = r"dp-logid=(.*?)&"



PARENT_DIR = pathlib.Path(sys.argv[0]).parent