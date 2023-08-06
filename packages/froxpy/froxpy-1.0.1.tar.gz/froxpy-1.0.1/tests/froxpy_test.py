import froxpy

if __name__ == '__main__':
    wp, bp, tp = froxpy.test_proxies(proxies=['https://103.240.161.101:6666',
        'https://181.176.161.19:8080', 'https://139.99.105.5:80', 'https://116.254.100.165:46675',
        'https://119.18.152.210:3127', 'https://67.219.116.234:8080', 'https://185.114.218.247'], output=False)

    print(wp)
    print(bp)
    print(tp)
