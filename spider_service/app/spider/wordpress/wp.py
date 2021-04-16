import base64
import datetime

import xlrd

from app.api.util.web_request import WebRequest

WORDPRESS_SITE_URL = 'https://blog.pingbook.top'


def readExcel(filename, index_title, index_content, index_date, category_ids, tags_ids):
    '''
    从后羿采集器导出的excel中读取对应的数据
    :param filename:
    :param index_title:
    :param index_content:
    :param index_date:
    :return:
    '''
    with xlrd.open_workbook(filename) as wb:
        sheet = wb.sheet_by_index(0)
        rows = sheet.nrows
        # cols = sheet.ncols
        for row_index in range(1, rows):
            # for col_index in range(0, cols):
            cell_title = sheet.cell(row_index, index_title).value
            cell_content = sheet.cell(row_index, index_content).value
            # 针对stackoverflow的结果
            cell_content_detail = sheet.cell(row_index, index_content + 1).value
            cell_content = '<h2>Question</h2> \n ' + cell_content_detail + '\n\n<h2>Answer</h2> \n' + cell_content

            if index_date:
                cell_date = sheet.cell(row_index, index_date).value
                cell_date = cell_date + ':00'
            else:
                cell_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 遍历行数据填充到对应的wordpress的接口数据中
            newPost(cell_date, cell_title, cell_content, category_ids, tags_ids)


def newPost(date, title, content, categories, tags):
    '''
     参考接口文档: https://developer.wordpress.org/rest-api/reference/posts/#arguments-2
    :param title:
    :param content:
    :param category:
    :param date:
    :return:
    '''
    url = '{}/wp-json/wp/v2/posts'.format(WORDPRESS_SITE_URL)
    headers = {
        # 'Authorization': 'Basic YWx0ZXJodTIwMjA6TDBuZ2gpMTAyNkE='
        'Authorization': 'Basic YWx0ZXJodTIwMjA6SFFENHJsZzkxZFIybmV3NGFieTMwQlBlIA=='
    }
    data = {
        # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        'date': date,
        'date_gmt': date,
        'title': title,
        # 是否发布
        'status': 'publish',
        'content': content,
        'author': 1,
        'categories': categories,
        'tags': tags,
        'ping_status': 'closed',
        'format': 'standard'
    }
    r = WebRequest()
    try:
        res_content = r.pc().post(url=url, headers=headers, data=data).json()
        print(res_content)
    except Exception as e:
        print('异常请求: {}'.format(str(e)))


if __name__ == '__main__':
    # base64 username
    userName = 'alterhu2020'
    password = 'qaerR)&nrt*Rv&^EFpEMEorkA5yI|C1S>AK6fc'
    userAndPass = base64.b64encode(b('%s:%s' % (userName, password)), 'ascii')
    base64str = 'Basic %s' % (userAndPass)
    print('base64 is: ', )
    filename = "D:\\2019-10-30-11-9-22-57807598167899-Posts containing 'python flask-采集的数据-后羿采集器.xlsx"
    index_title = 0
    index_content = 12
    index_publish_date = None
    category_ids = [2]  # vue =7, java=2
    tags_ids = [22]  # vue=11, spring=22
    readExcel(filename, index_title, index_content, index_publish_date, category_ids, tags_ids)
