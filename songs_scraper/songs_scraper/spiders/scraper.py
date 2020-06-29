import scrapy
from songs_scraper.items import SongsItem
from datetime import datetime
import re
from googletrans import Translator
import string

class Scraper(scrapy.Spider):
    name = "my_scraper"

    start_urls = ["https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/"]

    npages = 20

    for i in range(1, npages + 1):
        start_urls.append("https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=" + str(i) + "")

    def parse(self, response):
        for href in response.xpath(
                "//h4[contains(@class, 'pt-cv-title')]/a[contains(@class, '_blank')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        translator = Translator()
        item = SongsItem()

        # Getting the song Title
        title = response.xpath("//h1[contains(@class, 'entry-title')]/descendant::text()").extract()[
            0].strip()
        item['Title'] = title

        # Getting the song lines
        exclude = set(string.punctuation)
        temp = response.xpath("//pre[contains(@style, 'font-weight:bold;')]/descendant::text()").extract()
        temp_2 = ''.join(line for line in temp)
        if(temp_2==''):
            raise Exception('No Body')
        temp_3 = re.sub(r'[A-Za-z0-9]', '', temp_2)
        temp_4 = ''.join(ch for ch in temp_3 if ch not in exclude)
        item['Body'] = temp_4.strip()

        # Getting the Artist name
        artist = response.xpath(
            "//span[contains(@class, 'entry-categories')]/descendant::text()").extract()[1]
        artist_translated = translator.translate(artist, src='en', dest='si')
        item['Artist'] = ''
        if(not re.search(r'[a-zA-Z]', artist_translated.text)):
            item['Artist'] = artist_translated.text

        # Getting the name of lyrics writer
        item['Lyrics'] = ''
        try:
            lyrics = response.xpath(
                "//span[contains(@class, 'lyrics')]/descendant::text()").extract()[1]
            lyrics_translated = translator.translate(lyrics, src='en', dest='si')

            if (not re.search(r'[a-zA-Z]',lyrics_translated.text)):
                item['Lyrics'] = lyrics_translated.text
        except IndexError:
            print('catched')

        # Getting the name of composer
        item['Music'] = ''
        try:
            music = response.xpath(
                "//span[contains(@class, 'music')]/descendant::text()").extract()[1]
            music_translated = translator.translate(music, src='en', dest='si')

            if (not re.search(r'[a-zA-Z]', music_translated.text)):
                item['Music'] = music_translated.text
        except IndexError:
            print('catched')

        # Getting the genre of the song
        item['Genre'] = ''
        try:
            genre = response.xpath(
                "//span[contains(@class, 'entry-tags')]/descendant::text()").extract()[1]
            genre_translated = translator.translate(genre, src='en', dest='si')

            if (not re.search(r'[a-zA-Z]', genre_translated.text)):
                item['Genre'] = genre_translated.text
        except IndexError:
            print('catched')

        # Getting the Beat and Key of the song
        item['Beat'] = ''
        item['Key'] = ''
        try:
            keybeat = response.xpath(
                '//*[@id="genesis-content"]/article/div[3]/h3/descendant::text()').extract()[0]

            key1,beat1=keybeat.split('|')
            key = key1.split(':')[1]
            beat = beat1.split(':')[1]
            item['Beat'] = beat.strip()
            item['Key'] = key.strip()
        except ValueError:
            print('catched')

        # Getting the number of views for the song in the site
        item['Views'] = 0
        try:
            views = response.xpath("//div[contains(@class, 'tptn_counter')]/descendant::text()").extract()[0]
            views = views.replace(',','')
            views = re.findall('\d+', views )
            item['Views'] = int(views[0])
        except ValueError:
            print('catched')
        except IndexError:
            print('catched')

        yield item
