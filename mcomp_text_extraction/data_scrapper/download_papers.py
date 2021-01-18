import wget

def download_files(urls_file, download_location):
    with open(urls_file, "r") as f:
        urls = f.readlines()
    
    counter = 0
    for paper_url in urls:
        try:
            if counter % 20 == 0:
                print("Finished downloading %d" % counter, flush=True)
            paper_url = paper_url.strip()
            wget.download(paper_url, download_location)
            counter += 1
        except Exception as ex:
            print("Error for purl: %s" %(paper_url), flush=True)
            print(ex, flush=True)
    return

if __name__ == "__main__":
    download_files("cvpr_paper_urls_updated.txt", "/home/singh_shruti/data/cvpr/pdfs/")
