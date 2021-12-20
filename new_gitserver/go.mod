module gitserver

go 1.16

require (
	github.com/sosedoff/gitkit v0.3.0
	golang.org/x/crypto v0.0.0-20210513164829-c07d793c2f9a
)

// replace github.com/sosedoff/gitkit v0.3.0 => github.com/phlmn/gitkit v0.3.0
replace github.com/sosedoff/gitkit v0.3.0 => ../../gitkit
