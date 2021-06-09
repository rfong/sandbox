// https://tour.golang.org/concurrency/10

package main

import (
	"fmt"
	"sync"
)

type Fetcher interface {
	// Fetch returns the body of URL and
	// a slice of URLs found on that page.
	Fetch(url string) (body string, urls []string, err error)
}

// SafeCache is safe to use concurrently.
type SafeCache struct {
	mu sync.Mutex
	v  map[string]bool
}

// Marks a url as seen.
func (c *SafeCache) MarkSeen(url string) {
	c.mu.Lock()
	// Lock so only one goroutine at a time can access the map c.v.
	c.v[url] = true
	c.mu.Unlock()
}

// Return whether this url has been seen in cache.
// Locked so only one goroutine at a time can access the map.
func (c *SafeCache) IsSeen(url string) bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	_, ok := c.v[url]
	return ok
}

// Crawl uses fetcher to recursively crawl
// pages starting with url, to a maximum of depth.
func Crawl(url string, depth int, fetcher Fetcher, cache *SafeCache, wg *sync.WaitGroup) {
	defer wg.Done()
	if depth <= 0 {
		return
	}
	// Don't fetch the same URL twice.
	if cache.IsSeen(url) {
		//fmt.Printf("Already seen %s; skipping\n", url)
		return
	}
	// Fetch body & sub-urls
	_, urls, err := fetcher.Fetch(url)
	if err != nil {
		fmt.Println(err)
		return
	}
	// Mark as seen
	cache.MarkSeen(url)
	//fmt.Printf("[%d] found: %s %q\n", depth, url, body)

	// Loop through page sub-urls
	var wg2 sync.WaitGroup
	wg2.Add(len(urls))
	for _, u := range urls {
		go Crawl(u, depth-1, fetcher, cache, &wg2)
	}
	wg2.Wait()
}

func main() {
	var wg sync.WaitGroup
	cache := SafeCache{v: make(map[string]bool)}
	wg.Add(1)
	go func() {
		Crawl("https://golang.org/", 4, fetcher, &cache, &wg)
	}()
	wg.Wait()
	fmt.Println("ALL DONE")
	for url, _ := range cache.v {
		fmt.Println(url)
	}
}

// fakeFetcher is Fetcher that returns canned results.
type fakeFetcher map[string]*fakeResult

type fakeResult struct {
	body string
	urls []string
}

func (f fakeFetcher) Fetch(url string) (string, []string, error) {
	if res, ok := f[url]; ok {
		return res.body, res.urls, nil
	}
	return "", nil, fmt.Errorf("not found: %s", url)
}

// fetcher is a populated fakeFetcher.
var fetcher = fakeFetcher{
	"https://golang.org/": &fakeResult{
		"The Go Programming Language",
		[]string{
			"https://golang.org/pkg/",
			"https://golang.org/cmd/",
		},
	},
	"https://golang.org/pkg/": &fakeResult{
		"Packages",
		[]string{
			"https://golang.org/",
			"https://golang.org/cmd/",
			"https://golang.org/pkg/fmt/",
			"https://golang.org/pkg/os/",
		},
	},
	"https://golang.org/pkg/fmt/": &fakeResult{
		"Package fmt",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
	"https://golang.org/pkg/os/": &fakeResult{
		"Package os",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
}
