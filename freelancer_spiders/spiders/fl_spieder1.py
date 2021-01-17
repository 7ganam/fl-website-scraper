# -*- coding: utf-8 -*-
import json
import scrapy
import re
from currency_converter import CurrencyConverter
import json
import time

epoch_time = int(time.time())
f = open('currency_data.json',)
currency_data = json.load(f)


class TweetsSpider(scrapy.Spider):
    def __init__(self):
        self.spider_init_time = int(time.time())
        print("spider started at:",  self.spider_init_time)

    name = 'fl_spider1'
    allowed_domains = ['freelancer.com']
    start_urls = [
        'https://www.freelancer.com/u/IvanCoder204'
    ]

    def parse(self, response):
        self.profile_arrived_time = int(time.time())
        print("profile page arrived at:",  self.profile_arrived_time)

        data = response.xpath("//script[contains(., 'userId')]/text()").get()
        pattern = "UserId==(.*?)&"
        userID = re.search(pattern, data).group(1)

        print('-------')
        print("userd_id:", userID)
        print('-------')

        self.profile_parsed_time = int(time.time())
        print("profile parsed for id at:",  self.profile_parsed_time)

        url = 'https://www.freelancer.com/api/projects/0.1/reviews/?limit=5000&role=freelancer&to_users%5B%5D={}&project_details=true&contest_details=true&project_job_details=true&contest_job_details=true&review_types%5B%5D=contest&review_types%5B%5D=project&webapp=1&compact=true&new_errors=true&new_pools=true'.format(
            userID)

        yield scrapy.Request(url=url, callback=self.parse_url)
        self.user_api_request_time = int(time.time())
        print("api request sent at:",  self.user_api_request_time)

    def parse_url(self, response):
        print("views arrived",  int(time.time()))
        self.user_api_request_arrived_time = int(time.time())
        print("api request arrived at:",  self.user_api_request_arrived_time)

        jsonresponse = json.loads(response.body)
        reviews_reversed = jsonresponse['result']['reviews']
        reviews = reviews_reversed[::-1]
        money = 0
        for index, review in enumerate(reviews):
            if "paid_amount" in review:
                review_currency = review['currency']['code']
                inverseRate = currency_data[review_currency.lower(
                )]['inverseRate']

                start_time = review['time_submitted']
                if index != 0:
                    task_time_in_days = (
                        start_time - reviews[index-1]['time_submitted'])/60/60/24
                else:
                    task_time_in_days = 0

                ouput_currency = "EGP"
                task_price = review['paid_amount']*inverseRate * \
                    (currency_data[ouput_currency.lower()]['rate'])
                print(
                    '{:4.0f}-'.format(
                        index), '(price):', "{:6.0f}".format(task_price),
                    ouput_currency,
                    '(days since last task):',
                    "{:6.2f}".format(float(task_time_in_days)))
                money = money+review['paid_amount']*inverseRate
            else:
                print('???')
                # print(review)
                # print('tw777777777777777777777777777777777777777eet')
            yield (review)

        self.user_reviews_parsed_time = int(time.time())
        print("api request parsed at:",  self.user_reviews_parsed_time)

        months_from_start = (
            reviews[-1]['time_submitted'] - reviews[0]['time_submitted'])/60/60/24/30
        ouput_currency = "EGP"
        total_money = money * (currency_data[ouput_currency.lower()]['rate'])

        print("summery------------------------")
        print('total profit: ', "{:,}".format(total_money), ouput_currency)
        print('total years: ', months_from_start/12)
        print('salary per month: ', "{:,}".format(
            total_money / months_from_start))
