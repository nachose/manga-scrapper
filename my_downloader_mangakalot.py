import os
import cfscrape
import zipfile
from BeautifulSoup import *
import shutil

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    print ("######################################################")
    print ("Welcome, introduce the url, take care of all the parts (include the http or https)")
    print ("url example: https://manganelo.com/manga/jojo_no_kimyou_na_bouken")
    print ("Leave blank for exit")
    print ("######################################################")

    url = raw_input('-------------------\nEnter manga url: ')
    #if len(url) < 1: break

    serie_scraper = cfscrape.create_scraper()
    serie_html = serie_scraper.get(url).content
    serie_soup = BeautifulSoup(serie_html)

    chapter_div = serie_soup.findAll('div', attrs={"class":"chapter-list"})

    for a in chapter_div:
        print str(a)






def download_url(url):
    http, empty, page, string, serie, chapter = url.split("/")

    while True:

        sep = "/"

        my_url = sep.join((http, empty, page, string, serie, chapter))
        print "chapter is " + chapter 
        print "My new url is " + my_url

        #Download and scrape url.
        scrape = cfscrape.create_scraper()
        html = scrape.get(my_url).content
        soup = BeautifulSoup(html)

        image_list = [tag.findAll('img') for tag in soup.findAll('div', id="vungdoc")]

        def download_image(image_response, image_number):
            path_directory = "{}/Downloads/{}/{}/".format(SCRIPT_DIR, serie, chapter)
            file_name = "{}.png".format("img-" + "%03d" % (image_number,))
            if image_response.status_code == 200:
                if not os.path.exists(path_directory):
                    os.makedirs(path_directory)
                with open(path_directory + file_name, 'wb') as out_file:
                    for data in image_response:
                        out_file.write(data)
                    print path_directory
                    print file_name
            else:
                print image_response.status_code

        counter = 0;
        for img in image_list[0]:
            download_image(scrape.get(img['src']), counter)
            counter += 1
        
        ch_str, num = chapter.split("_")

        #Chapter name is filled with two zeros, just in case
        chapter_str = ch_str + "_" + num.zfill(3)
        
        #Zip my file.
        zip_name="./" + "Downloads/" + serie + "/" + serie + "_" + chapter_str + ".cbz"
        print 'creating archive'
        zf = zipfile.ZipFile(zip_name, mode='w')

        list_files = os.listdir("./Downloads/"+ serie + "/" + chapter)

        try:
            for image in list_files:
                print 'adding ' + image
                zf.write("./Downloads/" + serie + "/" + chapter + "/" + image)
        finally:
            print 'closing'
            zf.close()

        #Delete the folder
        print 'deleting the images'
        shutil.rmtree("./Downloads" + "/" + serie + "/" + chapter)
        

        #Add 1 to the chapter number
        chapter = ch_str + "_" + str( int( num ) + 1 )
        print "New chapter is " + chapter


if __name__ == "__main__":
    main()
