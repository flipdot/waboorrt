module gitserver

go 1.16

require (
	github.com/davecgh/go-spew v1.1.1 // indirect
	github.com/sosedoff/gitkit v0.3.0
	golang.org/x/sys v0.0.0-20210423082822-04245dca01da // indirect
)

// replace github.com/sosedoff/gitkit v0.3.0 => github.com/phlmn/gitkit v0.3.0
replace github.com/sosedoff/gitkit v0.3.0 => ../../gitkit
