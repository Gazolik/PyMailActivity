import sys
import xlsxwriter

from EmailActivity import Manager

date_format = '%Y-%m'


def xlsx_write(filename, dic, detailed = False):
    print('Writing to ' + filename + '.xlsx')
    wb = xlsxwriter.Workbook(filename + '.xlsx')
    ws = wb.add_worksheet()
    row = 2
    ws.write(0,1, 'TOTAL')
    for key_1 in sorted(dic.keys()):
        ws.write(row, 0, key_1)
        ws.write(row, 1, dic[key_1]['tot'])
        col = 2
        if detailed:
            for key_2 in sorted(dic[key_1].keys()):
                if key_2 == 'tot':
                    continue
                ws.write(row-1, col, key_2)
                ws.write(row, col, dic[key_1][key_2])
                col += 1
            row += 3
        else:
            row += 1
    wb.close()


if __name__ == '__main__':
    m = Manager(sys.argv[1], date_format)
    m.process_all()
    xlsx_write('date_sender', m.sender_dates)
    xlsx_write('senders', m.senders)
    xlsx_write('receivers', m.receivers)
