if __name__ == "__main__" :



    try:
        # my_code_here
        print('Here is where the exception is')

        import time
        import logging

        print("Starting")

        from scrapy import cmdline

        cmdline.execute("scrapy crawl detail_spider".split())

    except Exception as e:
        print('Unexpected error:' + str(e))

        time.sleep(10)

        input()



