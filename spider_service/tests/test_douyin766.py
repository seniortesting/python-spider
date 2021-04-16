from app.api.util.web_request import WebRequest

if __name__ == '__main__':
    '''
    下载都应素材网小视频
    '''
    startUrl = 'https://www.douyin766.com/7580.html'
    downloadSubUrl = 'https://tu.douyin766.com/2020/douyin766_com20200814141350.mp4'

    headers = {
        # ':authority': downloadBaseUrl,
        # ':method': 'GET',
        # ':path': downloadSubUrl,
        # ':scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'identity;q=1, *;q=0',
        'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'Hm_lvt_a526115426c20fe5b47498b19f600f0c=1598151647,1598152192; Hm_lpvt_a526115426c20fe5b47498b19f600f0c=1598152386',
        'dnt': '1',
        'pragma': 'no-cache',
        'range': 'bytes=0-',
        'referer': startUrl,
        'sec-fetch-dest': 'video',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site'
    }
    http = WebRequest()
    r = http.pc().get(downloadSubUrl, headers=headers, allow_redirects=False,
                      stream=True)
    # 解析内容
    downloadSubUrl = downloadSubUrl.replace('https://tu.douyin766.com', '')
    splitSubUrl = downloadSubUrl.split('/')
    fileName = splitSubUrl[-1]
    with open('D:\\Download\\' + fileName, 'wb') as f:
        f.write(r.content)
